package com.zhide.worth.admin;

public record JobImportResult(int rowsRead, int inserted, int duplicates, int skipped) {
}
