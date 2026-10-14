package com.zhide.worth.job;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record JobUpsertRequest(
        @NotBlank @Size(max = 40) String source,
        @NotBlank @Size(max = 255) String title,
        @NotBlank @Size(max = 200) String org,
        @Size(max = 100) String category,
        @Size(max = 350) String location,
        @Size(max = 100) String salary,
        @Size(max = 100) String degree,
        @Size(max = 40) String postedDate,
        String description,
        @NotBlank @Size(max = 500) String url
) {
}
