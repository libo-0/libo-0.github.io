---
title: API-网关-Gateway
tags:
  - API-Gateway
  - API-网关
categories:
  - API-Gateway
  - API-网关
img: >-
  https://docs.microsoft.com/en-us/azure/architecture/microservices/images/gateway.png
date: 2020-03-07 15:04:08
---


在一个微服务架构，一个客户端必须与不止一个的前端服务交互，鉴于此，客户端如何知道改调用哪个端点呢？新的服务被引入后会发生什么，已存在的服务需要重构吗？服务如何处理 SSL termination，认证和其他关注点呢？一个 API 网关能够处理这些挑战。

<!-- more -->

![gateway][1]

## API 网关是什么？

一个 API 网关在客户端和服务之间。它起到一个反向代理的作用，路由客户端的请求到服务。它能够执行各种跨切的任务，例如认证、SSL termination，速率限制。如果你没有部署一个网关，客户端必须直接发送请求到前端服务。然而，这样直接暴露服务给客户端有潜在的问题：

* 它将导致复杂的客户端代码。客户端必须追踪多个 endpoints，处理失败不统一。
* 它创建了客户端和后端的耦合。客户端必须知道单个服务是怎样分解的。这让客户端更难维持，同样更难重构服务。
* 单次操作可能需要调用多次服务。这会导致多个网络 round trip 在客户端和服务之间，添加了很大的延迟。
* 每个公共面对的服务必须处理例如认证，SSL，和客户端速率限制。
* 服务必须暴露客户端友好的协议，例如 HTTP 或者 WebSocket。这限制了[沟通协议][2]的选择。
* 公共端点的服务面临潜在的攻击风险，必须被加强。

一个网关帮忙处理这些问题，功过解耦客户端与服务端。网关可能执行很多不同的功能，你可能不需要所有的，这些功能可能被分类为下列的设计模式：

[网关路由][3]： 使用网关作为反向代理来路由请求到一个或多个后端服务，使用第 7 层路由。网关给客户端提供了一个单一端点，帮助客户端与服务解耦。

[网关聚集][4]：使用网关来聚集多个请求到单个请求。这个模式应用，当单次操作需要调用多个后端服务时。客户端发送一个请求到网关。网关分发请求到各种后端服务，然后聚集结果，把它们发送回给客户端。这减少了客户端和后端的沟通。

[网关 Offloading][5]：使用网关来卸载功能，从单个服务到网关，尤其是跨-切的关注点。这非常有用，将这些功能在一个地方加固，而不是让每个服务都实现它们。这对于需要特定技巧来实现的特点相当有用，例如认证和授权。

这里是一些功能能够卸载到网关的：

* SSL termination
* 认证
* IP 白名单
* 客户端速率限制
* 日志和监控
* 响应缓存
* Web 应用防火墙
* GZIP 压缩
* 服务静态内容

## 选择一种网关技术

这里是一些在你的应用中实现 API 网关的一些选项。

* 反向代理服务器. Nginx 和 HAProxy 是流行的反向代理服务器，其实负载均衡，SSL，第 7 层路由。它们都是免费，开源的产品，支付版本提供额外的特点。Nginx 和 HAProxy 都是成熟的产品，提供丰富的特点和高性能。你可以扩展第三方的模块，或者写 Lua 自定义脚本。

* 服务网进入控制器。如果你使用服务网例如 linkerd 或者 Istio，考虑相应的服务网对应的进入控制特点。例如 Istio 进入控制提供第 7 层路由，HTTP 重定向，重试和其他特点。

* [Azure Application Gateway][6]. 应用网关是一个管理负载均衡服务，可以执行第7层路由和 SSL termination。它同样提供了应用防火墙。

* [Azure API Management][7]. API 管理是一个完整并立刻可用的解决方法来出版 API 到外部或内部客户端。它提供了有用的特点来管理公共 API，包括速率限制，IP 白名单，使用 Azure Active Directory 来认证和其他身份提供商。API 管理不提供任何负载均衡，所以它应该结合负载均衡器例如应用网关或反向代理。

## 参考

Microsoft Azure [Using API gateways in microservices][0]

[0]: https://docs.microsoft.com/en-us/azure/architecture/microservices/design/gateway
[1]: https://docs.microsoft.com/en-us/azure/architecture/microservices/images/gateway.png
[2]: https://docs.microsoft.com/en-us/azure/architecture/microservices/design/interservice-communication
[3]: https://docs.microsoft.com/en-us/azure/architecture/patterns/gateway-routing
[4]: https://docs.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation
[5]: https://docs.microsoft.com/en-us/azure/architecture/patterns/gateway-offloading
[6]: https://docs.microsoft.com/en-us/azure/application-gateway/
[7]: https://docs.microsoft.com/en-us/azure/api-management/