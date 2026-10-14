package com.zhide.worth.admin;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class JobCsvImportService {

    private static final int BATCH_SIZE = 500;
    private static final String INSERT_SQL = """
            INSERT IGNORE INTO jobs
                (source, title, org, category, location, salary, degree, posted_date, description, url,
                 created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6))
            """;

    private final JdbcTemplate jdbcTemplate;

    public JobCsvImportService(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public JobImportResult importCsv(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "请选择非空CSV文件");
        }
        if (file.getSize() > 20L * 1024 * 1024) {
            throw new ResponseStatusException(HttpStatus.PAYLOAD_TOO_LARGE, "CSV文件不能超过20MB");
        }

        final String content;
        try {
            content = new String(file.getBytes(), StandardCharsets.UTF_8);
        } catch (IOException exception) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "读取CSV文件失败");
        }

        List<List<String>> rows = parseCsv(content);
        if (rows.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "CSV文件没有表头");
        }

        Map<String, Integer> columns = new HashMap<>();
        List<String> headers = rows.get(0);
        for (int i = 0; i < headers.size(); i++) {
            String name = headers.get(i).replace("\uFEFF", "").trim().toLowerCase();
            columns.put(name, i);
        }
        for (String required : List.of("source", "title", "org", "category", "location",
                "salary", "degree", "date", "description", "url")) {
            if (!columns.containsKey(required)) {
                throw new ResponseStatusException(
                        HttpStatus.BAD_REQUEST, "CSV缺少必需列：" + required
                );
            }
        }

        int read = 0;
        int skipped = 0;
        int inserted = 0;
        List<Object[]> batch = new ArrayList<>(BATCH_SIZE);

        for (int rowIndex = 1; rowIndex < rows.size(); rowIndex++) {
            List<String> row = rows.get(rowIndex);
            if (row.size() == 1 && row.get(0).isBlank()) {
                continue;
            }
            read++;
            String source = field(row, columns, "source").trim();
            String title = field(row, columns, "title").trim();
            String org = field(row, columns, "org").trim();
            String url = field(row, columns, "url").trim();
            String location = field(row, columns, "location").trim();

            if (source.isBlank() || title.isBlank() || org.isBlank() || url.isBlank()
                    || source.length() > 40 || title.length() > 255 || org.length() > 200
                    || location.length() > 350 || url.length() > 500) {
                skipped++;
                continue;
            }

            batch.add(new Object[]{
                    source, title, org,
                    nullable(field(row, columns, "category")),
                    nullable(location),
                    nullable(field(row, columns, "salary")),
                    nullable(field(row, columns, "degree")),
                    nullable(field(row, columns, "date")),
                    field(row, columns, "description"),
                    url
            });

            if (batch.size() == BATCH_SIZE) {
                inserted += insertBatch(batch);
                batch.clear();
            }
        }
        if (!batch.isEmpty()) {
            inserted += insertBatch(batch);
        }

        return new JobImportResult(read, inserted, read - skipped - inserted, skipped);
    }

    private int insertBatch(List<Object[]> batch) {
        int inserted = 0;
        for (int count : jdbcTemplate.batchUpdate(INSERT_SQL, batch)) {
            if (count > 0) {
                inserted += count;
            }
        }
        return inserted;
    }

    private static String field(List<String> row, Map<String, Integer> columns, String name) {
        int index = columns.get(name);
        return index < row.size() ? row.get(index) : "";
    }

    private static String nullable(String value) {
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

    static List<List<String>> parseCsv(String content) {
        List<List<String>> rows = new ArrayList<>();
        List<String> row = new ArrayList<>();
        StringBuilder field = new StringBuilder();
        boolean quoted = false;

        for (int i = 0; i < content.length(); i++) {
            char current = content.charAt(i);
            if (quoted) {
                if (current == '"') {
                    if (i + 1 < content.length() && content.charAt(i + 1) == '"') {
                        field.append('"');
                        i++;
                    } else {
                        quoted = false;
                    }
                } else {
                    field.append(current);
                }
            } else if (current == '"' && field.isEmpty()) {
                quoted = true;
            } else if (current == ',') {
                row.add(field.toString());
                field.setLength(0);
            } else if (current == '\n' || current == '\r') {
                if (current == '\r' && i + 1 < content.length() && content.charAt(i + 1) == '\n') {
                    i++;
                }
                row.add(field.toString());
                field.setLength(0);
                rows.add(row);
                row = new ArrayList<>();
            } else {
                field.append(current);
            }
        }

        if (quoted) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "CSV存在未闭合的引号");
        }
        if (!row.isEmpty() || !field.isEmpty()) {
            row.add(field.toString());
            rows.add(row);
        }
        return rows;
    }
}
