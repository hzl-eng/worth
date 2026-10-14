package com.zhide.worth.job;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Service
@Transactional(readOnly = true)
public class JobService {

    private final JobRepository repository;

    public JobService(JobRepository repository) {
        this.repository = repository;
    }

    public Page<JobSummaryResponse> search(String keyword, String location, String category,
                                           String degree, int page, int size) {
        int safePage = Math.max(page, 0);
        int safeSize = Math.min(Math.max(size, 1), 100);
        Specification<Job> specification = (root, query, builder) -> {
            List<jakarta.persistence.criteria.Predicate> predicates = new ArrayList<>();

            addContains(predicates, root, builder, "location", location);
            addContains(predicates, root, builder, "category", category);
            addContains(predicates, root, builder, "degree", degree);

            if (hasText(keyword)) {
                String pattern = likePattern(keyword);
                predicates.add(builder.or(
                        builder.like(builder.lower(root.get("title")), pattern, '\\'),
                        builder.like(builder.lower(root.get("org")), pattern, '\\'),
                        builder.like(builder.lower(root.get("description")), pattern, '\\')
                ));
            }

            return builder.and(predicates.toArray(jakarta.persistence.criteria.Predicate[]::new));
        };

        return repository.findAll(
                specification,
                PageRequest.of(safePage, safeSize, Sort.by(Sort.Direction.DESC, "updatedAt"))
        ).map(JobSummaryResponse::from);
    }

    public JobResponse get(long id) {
        return JobResponse.from(findJob(id));
    }

    @Transactional
    public JobResponse create(JobUpsertRequest request) {
        if (repository.existsBySourceAndUrl(request.source().trim(), request.url().trim())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "该来源的职位链接已存在");
        }
        Job job = toJob(request);
        return JobResponse.from(repository.save(job));
    }

    @Transactional
    public JobResponse update(long id, JobUpsertRequest request) {
        Job job = findJob(id);
        if (repository.existsBySourceAndUrlAndIdNot(
                request.source().trim(), request.url().trim(), id)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "该来源的职位链接已存在");
        }
        job.update(
                request.source().trim(), request.title().trim(), request.org().trim(),
                clean(request.category()), clean(request.location()), clean(request.salary()),
                clean(request.degree()), clean(request.postedDate()), request.description(),
                request.url().trim()
        );
        return JobResponse.from(repository.save(job));
    }

    @Transactional
    public void delete(long id) {
        repository.delete(findJob(id));
    }

    private Job findJob(long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "职位不存在"));
    }

    private Job toJob(JobUpsertRequest request) {
        return new Job(
                request.source().trim(), request.title().trim(), request.org().trim(),
                clean(request.category()), clean(request.location()), clean(request.salary()),
                clean(request.degree()), clean(request.postedDate()), request.description(),
                request.url().trim()
        );
    }

    private static void addContains(List<jakarta.persistence.criteria.Predicate> predicates,
                                    jakarta.persistence.criteria.Root<Job> root,
                                    jakarta.persistence.criteria.CriteriaBuilder builder,
                                    String field, String value) {
        if (hasText(value)) {
            predicates.add(builder.like(
                    builder.lower(root.get(field)), likePattern(value), '\\'
            ));
        }
    }

    private static String likePattern(String value) {
        String escaped = value.trim().toLowerCase(Locale.ROOT)
                .replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_");
        return "%" + escaped + "%";
    }

    private static boolean hasText(String value) {
        return value != null && !value.isBlank();
    }

    private static String clean(String value) {
        return hasText(value) ? value.trim() : null;
    }
}
