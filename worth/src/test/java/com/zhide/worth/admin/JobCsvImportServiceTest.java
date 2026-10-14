package com.zhide.worth.admin;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class JobCsvImportServiceTest {

    @Test
    void parsesQuotedCommasEscapedQuotesAndMultilineDescriptions() {
        String csv = "source,title,org,description\r\n"
                + "site,\"Java工程师\",\"示例公司\",\"要求熟悉Java, Spring\r\n"
                + "并能处理\"\"复杂数据\"\"\"\r\n";

        List<List<String>> rows = JobCsvImportService.parseCsv(csv);

        assertEquals(2, rows.size());
        assertEquals(List.of("source", "title", "org", "description"), rows.get(0));
        assertEquals("要求熟悉Java, Spring\r\n并能处理\"复杂数据\"", rows.get(1).get(3));
    }
}
