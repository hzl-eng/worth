package com.zhide.worth.job;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

import java.time.Instant;

@Entity
@Table(
        name = "jobs",
        uniqueConstraints = @UniqueConstraint(
                name = "uk_jobs_source_url",
                columnNames = {"source", "url"}
        ),
        indexes = {
                @Index(name = "idx_jobs_location", columnList = "location"),
                @Index(name = "idx_jobs_category", columnList = "category"),
                @Index(name = "idx_jobs_degree", columnList = "degree"),
                @Index(name = "idx_jobs_updated_at", columnList = "updated_at")
        }
)
public class Job {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 40)
    private String source;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(nullable = false, length = 200)
    private String org;

    @Column(length = 100)
    private String category;

    @Column(length = 350)
    private String location;

    @Column(length = 100)
    private String salary;

    @Column(length = 100)
    private String degree;

    // Keep the source value as text because sources use different date formats.
    @Column(name = "posted_date", length = 40)
    private String postedDate;

    @Column(columnDefinition = "MEDIUMTEXT")
    private String description;

    @Column(nullable = false, length = 500)
    private String url;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected Job() {
    }

    public Job(String source, String title, String org, String category,
               String location, String salary, String degree, String postedDate,
               String description, String url) {
        update(source, title, org, category, location, salary, degree, postedDate, description, url);
    }

    public void update(String source, String title, String org, String category,
                       String location, String salary, String degree, String postedDate,
                       String description, String url) {
        this.source = source;
        this.title = title;
        this.org = org;
        this.category = category;
        this.location = location;
        this.salary = salary;
        this.degree = degree;
        this.postedDate = postedDate;
        this.description = description;
        this.url = url;
    }

    @PrePersist
    void beforeInsert() {
        Instant now = Instant.now();
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    void beforeUpdate() {
        updatedAt = Instant.now();
    }

    public Long getId() { return id; }
    public String getSource() { return source; }
    public String getTitle() { return title; }
    public String getOrg() { return org; }
    public String getCategory() { return category; }
    public String getLocation() { return location; }
    public String getSalary() { return salary; }
    public String getDegree() { return degree; }
    public String getPostedDate() { return postedDate; }
    public String getDescription() { return description; }
    public String getUrl() { return url; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
}
