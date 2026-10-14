# 职得 WORTH

连接人才能力与真实机会。

## 项目结构

- `index.html`：品牌首页与岗位浏览界面
- `worth/`：Spring Boot、Spring Data JPA、MySQL 后端
- `zhide-spider/`：职位数据采集源码

本仓库不包含本地数据库密码、环境变量、职位采集结果、个人文档或构建产物。

## 运行后端

需要 Java 17 和 MySQL。创建名为 `worth` 的数据库后，将
`worth/src/main/resources/application-example.properties` 复制为
`application.properties`，并设置数据库环境变量：

- `DB_USERNAME`
- `DB_PASSWORD`
- 管理接口密钥（如需使用）：`WORTH_ADMIN_KEY`

在 `worth` 目录运行 `mvnw.cmd spring-boot:run`。首页默认地址为
`http://localhost:8080/`，职位接口为 `http://localhost:8080/api/v1/jobs`。

## 爬虫

采集脚本位于 `zhide-spider`。依赖见该目录的 `requirements.txt`。
采集结果文件被忽略，不会上传到仓库。

## 注意

登录与岗位访问控制目前是前端演示状态，尚未接入真实账号认证。
