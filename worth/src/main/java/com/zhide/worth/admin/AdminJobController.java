package com.zhide.worth.admin;

import com.zhide.worth.job.JobResponse;
import com.zhide.worth.job.JobService;
import com.zhide.worth.job.JobUpsertRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/v1/admin/jobs")
public class AdminJobController {

    private final AdminKeyGuard adminKeyGuard;
    private final JobService jobService;
    private final JobCsvImportService importService;

    public AdminJobController(AdminKeyGuard adminKeyGuard, JobService jobService,
                              JobCsvImportService importService) {
        this.adminKeyGuard = adminKeyGuard;
        this.jobService = jobService;
        this.importService = importService;
    }

    @PostMapping
    public ResponseEntity<JobResponse> create(
            @RequestHeader(value = "X-Admin-Key", required = false) String adminKey,
            @Valid @RequestBody JobUpsertRequest request) {
        adminKeyGuard.check(adminKey);
        return ResponseEntity.status(HttpStatus.CREATED).body(jobService.create(request));
    }

    @PutMapping("/{id}")
    public JobResponse update(
            @RequestHeader(value = "X-Admin-Key", required = false) String adminKey,
            @PathVariable long id,
            @Valid @RequestBody JobUpsertRequest request) {
        adminKeyGuard.check(adminKey);
        return jobService.update(id, request);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @RequestHeader(value = "X-Admin-Key", required = false) String adminKey,
            @PathVariable long id) {
        adminKeyGuard.check(adminKey);
        jobService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping(value = "/import-csv", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public JobImportResult importCsv(
            @RequestHeader(value = "X-Admin-Key", required = false) String adminKey,
            @RequestPart("file") MultipartFile file) {
        adminKeyGuard.check(adminKey);
        return importService.importCsv(file);
    }
}
