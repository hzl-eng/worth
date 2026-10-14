package com.zhide.worth.job;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface JobRepository extends JpaRepository<Job, Long>, JpaSpecificationExecutor<Job> {
    boolean existsBySourceAndUrl(String source, String url);
    boolean existsBySourceAndUrlAndIdNot(String source, String url, Long id);
}
