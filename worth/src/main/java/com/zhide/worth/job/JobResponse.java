package com.zhide.worth.job;

import java.time.Instant;

public record JobResponse(
        Long id,
        String source,
        String title,
        String org,
        String category,
        String location,
        String salary,
        String degree,
        String postedDate,
        String description,
        String url,
        Instant createdAt,
        Instant updatedAt
) {
    static JobResponse from(Job job) {
        return new JobResponse(
                job.getId(), job.getSource(), job.getTitle(), job.getOrg(),
                job.getCategory(), job.getLocation(), job.getSalary(), job.getDegree(),
                job.getPostedDate(), job.getDescription(), job.getUrl(),
                job.getCreatedAt(), job.getUpdatedAt()
        );
    }
}
