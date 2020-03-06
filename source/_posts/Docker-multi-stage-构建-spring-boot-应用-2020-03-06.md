---
title: Docker-multi-stage-构建-spring-boot-应用
tags:
  - Docker
  - multi-stage
  - spring-boot-in-docker
categories:
  - Docker
img: /images/docker.jpg
date: 2020-03-06 11:26:02
---


Docker 支持多阶段构建，下一个阶段可以拷贝上一个阶段的输出。阶段一 FROM 语句作为分隔。FROM 代表从那个镜像衍生，即从 docker hub 拉取改镜像。

<!-- more -->

Docker 镜像类似于面向对象编程的类，Docker 容器类似面向对象编程的对象。Docker 容器是 Docker 镜像的运行实例。

## Multi-stage

```bash
# 第一阶段
ARG MAVEN_VERSION=3.6.3-jdk-8-slim
FROM maven:${MAVEN_VERSION} AS build-stage
ENV PORT=9000
ENV WORK_DIR=/app
# 设置工作目录根目录
WORKDIR ${WORK_DIR}
# 复制代码 到工作目录
COPY . .
# 运行命令，设置 npm 注册仓库为 taobao 仓库
RUN mvn package

# 第二阶段
FROM openjdk:8u242-jre-slim
# 暴露 Spring Boot 应用 9000 端口
EXPOSE ${PORT}
# 运行命令
COPY --from=build-stage /app/target/Star-1.0.0-SNAPSHOT.jar ./app.jar
CMD java -jar app.jar
```

第一个构建阶段，使用 maven 容器来构建 spring boot 应用，将 spring boot 应用打包。在第二个阶段，将 jar 包拷贝过来，在 openjdk 环境下运行 jar 包。

每个阶段可以被命名，`FROM maven:${MAVEN_VERSION} AS build-stage` 将这一阶段命名为 `build-stage`， 然后通过 `COPY --from=build-stage /app/target/Star-1.0.0-SNAPSHOT.jar ./app.jar` 命令根据阶段名复制上一阶段的数据。
