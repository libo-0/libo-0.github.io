---
title: Spring-WebSocket
tags:
  - Spring
  - WebSocket
categories:
  - Spring
  - WebSocket
---

WebSocket 协议 [RFC 455][0] 定义了 web 应用的新能力：全双工的客户端和服务器之间的沟通。

<!-- more -->

HTTP 只被用来初次握手，依赖于 HTTP 的一个方法来请求协议升级（或者协议交换），如果服务器同意，它会返回和一个 HTTP 状态 101。如果握手成功，HTTP 升级请求下的 TCP socket 会保持打开，client 和 server 都可以用它相互发送消息。

REST 如今广泛使用。这个架构的特点：有很多 URL；有用的 HTTP 方法，无状态；

WebSocket 对比 REST，它只用一个 URL 做为初始的 HTTP 握手。所有之后的消息共享相同的 TCP 连接。这是一个完全不同的，异步的，事件驱动的，消息架构。

WebSocket 确实暗示一个消息架构，但没有强制使用那种消息协议。它是 TCP 上非常简单的层，传输字节流到消息，仅仅如此。有应用来解释消息的意思。

不像 HTTP，是一个应用层协议，在 WebSocket 中，对于任何框架或容器来说，没有足够的信息表明一个进来的消息该怎么路由或处理。因此，WebSocket 被争论为太底层，是一个微不足道的应用。它能够完成，但是它更倾向于在上面创建一个框架。这是有参考的，毕竟如今的大多数 web 应用使用一个 web 框架而不是一个 Servlet API。

因为这个原因，WebSocket RFC 定义了[子协议][1]的使用。在握手中，客户端和服务器能够使用 Sec-WebSocket-Protocol 来同意子协议。例如，一个更高层的，可以使用应用层的协议。子协议的使用不是必须的，但是即使没有使用，应用仍然需要选择一个消息格式来是 client 和 server 都能懂。这种格式是自定义的、框架独立的、标准的消息协议。

Spring Framework 提供了支持来使用 [STOMP][2]。一个简单的消息协议最初被创建为用 frame 在脚本语言中使用，受 HTTP 鼓舞。STOMP 受到广泛支持，适合在 WebSocket 和 Web 上使用。

## 为什么该用 WebSocket ？

在 web 应用中，最适合使用 WebSocket 的情况是客户端和服务器需要频繁和低延迟交换数据是。首要情况包含，但不限于金融、游戏、协作和其他。这样的应用都是对时间延迟很敏感的，需要高频交换很多消息。

对于其他应用类型，则不是这种情况。例如，一个新闻或社交 feed，当突发性新闻可获得时，简单的每几分钟轮询一次就行了。这里延迟很重要，但是新闻延迟几分钟显示也是可以接受的。

即使在延迟很严格要求的情况下，消息的体积很小（例如监控网络失败），使用长轮询（ Long Polling）应该被认为是一个相对简单并且可靠的替代，相比较于效率而言。

低延迟和高频率的消息能够充分利用 Websocket 协议。即使在这样的应用中，我们依然要决定是否所有的 client-server 沟通都要通过 WebSocket 而不是 HTTP 和 REST。将 WebSocket 和 REST API 同时暴露给客户端也是有可能的。



## 参考

[WebSocket Support][4]
[Spring MVC 3.2 Preview: Introducing Servlet 3, Async Support][3]
[Spring MVC 3.2 Preview: Techniques for Real-time Updates][5]

[0]: https://tools.ietf.org/html/rfc6455
[1]: https://tools.ietf.org/html/rfc6455#section-1.9
[2]: https://stomp.github.io/stomp-specification-1.2.html#Abstract
[3]: https://spring.io/blog/2012/05/07/spring-mvc-3-2-preview-introducing-servlet-3-async-support/
[4]: https://docs.spring.io/spring-framework/docs/5.0.0.BUILD-SNAPSHOT/spring-framework-reference/html/websocket.html
[5]: https://spring.io/blog/2012/05/08/spring-mvc-3-2-preview-techniques-for-real-time-updates