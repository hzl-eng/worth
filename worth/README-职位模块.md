# 职得职位模块

本模块基于 Java 17、Spring Boot、Spring Data JPA 和 MySQL，提供职位检索、详情、管理及已有 CSV 导入接口。应用启动后，开发环境中的 `spring.jpa.hibernate.ddl-auto=update` 会按实体创建或更新 `jobs` 表；不要在生产环境依赖该设置。

## 启动

确认 MySQL 正在运行，`src/main/resources/application.properties` 中的数据库地址、用户名和密码指向本机 `worth` 数据库，然后在 IntelliJ IDEA 运行 `WorthApplication`。成功启动后访问 `http://localhost:8080/api/v1/jobs`，职位为空时会返回空列表和分页信息。

列表默认每页 20 条，最多 100 条。支持 `keyword`、`location`、`category`、`degree`、`page`、`size` 参数，例如：

```text
GET http://localhost:8080/api/v1/jobs?keyword=工程师&location=北京&page=0&size=20
GET http://localhost:8080/api/v1/jobs/1
```

列表响应包含 `content`、`totalElements`、`totalPages` 等分页字段；列表只返回职位摘要，详情接口返回完整描述。

## 导入已有爬虫 CSV

在 IntelliJ 的运行配置中设置环境变量 `WORTH_ADMIN_KEY`，其值使用你自己设定的本地密钥。管理接口要求在请求头中携带同一个 `X-Admin-Key`。不要把密钥提交到 Git，也不要把管理接口暴露到公网。

在 PowerShell 执行以下命令，将已有的 `jobs_all_in_one.csv` 导入数据库：

```powershell
curl.exe -X POST "http://localhost:8080/api/v1/admin/jobs/import-csv" `
  -H "X-Admin-Key: 你的本地密钥" `
  -F "file=@D:\HZL\works\worth\zhide-spider\jobs_all_in_one.csv"
```

CSV 表头应包含 `source,title,org,category,location,salary,degree,date,description,url`。导入按 500 条一批处理，以来源和职位链接去重；响应会给出读取、写入、重复和跳过数量。重复执行不会重复插入相同来源和链接的记录。

## API

| 方法 | 地址 | 说明 |
|---|---|---|
| GET | `/api/v1/jobs` | 职位分页、关键词及条件检索 |
| GET | `/api/v1/jobs/{id}` | 职位详情 |
| POST | `/api/v1/admin/jobs` | 新增职位，需管理密钥 |
| PUT | `/api/v1/admin/jobs/{id}` | 更新职位，需管理密钥 |
| DELETE | `/api/v1/admin/jobs/{id}` | 删除职位，需管理密钥 |
| POST | `/api/v1/admin/jobs/import-csv` | 导入 CSV，需管理密钥，表单字段名为 `file` |

管理接口的请求头格式为 `X-Admin-Key: 你的本地密钥`。新建和更新接口使用 JSON，字段为 `source`、`title`、`org`、`category`、`location`、`salary`、`degree`、`postedDate`、`description`、`url`。职位日期暂按文本保存，以保留不同来源的原始格式。
