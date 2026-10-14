package com.zhide.worth.job;

public record JobSummaryResponse(
        Long id,
        String source,
        String title,
        String org,
        String category,
        String location,
        String salary,
        String degree,
        String postedDate,
        String url
) {
    static JobSummaryResponse from(Job job) {
        return new JobSummaryResponse(
                job.getId(), job.getSource(), job.getTitle(), job.getOrg(),
                job.getCategory(), job.getLocation(), job.getSalary(), job.getDegree(),
                job.getPostedDate(), job.getUrl()
        );
    }
}
