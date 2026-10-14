package com.zhide.worth.admin;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

@Component
public class AdminKeyGuard {

    private final String configuredKey;

    public AdminKeyGuard(@Value("${worth.admin-key:}") String configuredKey) {
        this.configuredKey = configuredKey;
    }

    public void check(String suppliedKey) {
        if (configuredKey.isBlank()) {
            throw new ResponseStatusException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "请先在本机配置 worth.admin-key，再调用管理接口"
            );
        }
        if (suppliedKey == null || !MessageDigest.isEqual(
                configuredKey.getBytes(StandardCharsets.UTF_8),
                suppliedKey.getBytes(StandardCharsets.UTF_8))) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "管理密钥无效");
        }
    }
}
