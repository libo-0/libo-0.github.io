---
title: Spring-Actuator
tags:
  - Spring-Actuator
categories:
  - Spring-Actuator
---

Spring Boot Actuator 提供了安全的端点来监控和管理你的 Spring Boot 应用。默认，所有的 actuator 端点都是安全的。

<!-- more -->

Spring Boot Actuator 有以下 endpoints:

* /metrics 查看应用 metrics 例如内存使用，空闲，线程，类，系统上线时间
* /env 查看应用中环境变量
* /beans 查看 Spring Beans 和它的变量，范围，依赖
* /health 查看应用健康情况
* /info Spring Boot 应用信息
* /trace 查看 rest endpoints traces 列表