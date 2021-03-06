---
title: Designing-interservice-communication-for-microservices-微服务之间沟通的设计
tags:
  - 微服务
  - microservice
categories:
  - 微服务
  - microservice
date: 2020-03-07 15:03:35
---


微服务之间的沟通必须是有效和健壮的。在单个事务中有很多小服务的交互，这可能是一个挑战。在这片文章，我们将看看异步消息与同步 API 之间的妥协。然后我们看看设计弹性服务间沟通的挑战。

<!-- more -->

## 挑战

这里是 service-to-service 沟通的主要挑战。服务网，Service meshes，稍后描述，将被设计来处理很多挑战。

**Resiliency**. 给的微服务示例可能有几十个或者上百个。一个实例可能由于各种原因失败。可能是节点级的失败，例如硬件失败或者 VM 重启。一个实例可能崩溃，或者被请求吞没，不能处理任何新的请求。这些事件的任何一个会造成失败。有两个设计模式能够帮助 service-to-service 网络调用更有弹性：

* [Retry][1]. 一个网络可能会失败由于系统运行的一个短暂的错误。不是完全失败，调用者典型的重试指定次数。然而，如果一个操作不是冥等的，重试会造成意想不到的负效应。最初的调用可能成功，但是调用者无法获得相应。如果调用重试，这个操作可能调用两次。通常，重试 POST 或者 PATCH 方法是不安全的，因为这些不保证是冥等的。

* [Circuit Breaker][2]. 太多的失败请求可能造成瓶颈，如队列中的请求累积。这些请求可能会占用重要的系统资源例如内存，线程，数据库连接，等等，可能会造成级联的失败。

**负载均衡**. 当服务 A 调用服务 B，这个请求必须到达运行服务 B 的实例。在 Kubernetes，这个服务资源类型提供一个稳定的 IP 地址给一组 pods。到服务 IP 的网络交通被前向到一个 pod 通过各种路由表。默认，一个随机的 pod 被选择。一个服务网可以提供更智能的负载均衡算法，基于观察的延迟和其他 metrics。

**Distributed tracing**. 单个事务可能跨越多个服务。这使它更难监控总体的性能和系统健康。即使每个服务生成日志和 metrics，没有通过某种方式将它们联系，它们的用处有限。

**服务版本**. 当一个团队部署它们的新版本服务，它们必须避免破坏其它服务或者依赖它的外部客户端。除此之外，你可能想同时运行多个版本的服务，并且路由请求到特定的版本。查看 [API Versioning][3]的更多问题讨论。

**TLS 加密和相互地 TLS 认证**. 因为安全原因，你可能想要加密服务间的沟通使用 TLS，并且相互使用 TLS 认证 来认证调用者。

## 同步与异步消息

微服务与微服务的沟通有两种基础的消息模式。

1. 同步沟通。这种方式，一个服务调用另一个服务暴露的 API，使用 HTTP 或者 gRPC。这个选项是同步消息模式，因为调用者等待接受者被调用者的响应。

2. 异步消息传递。这种模式，一个服务发送消息而不等待，一个或多个服务异步处理消息。

区分异步 I/O 和异步协议是很重要的。异步 I/O 意味着当 I/O 完成，调用者线程不会被阻塞。这对性能来说是很重要的，但是相对架构而言是一个实现细节。一个异步协议意味着发送者不必等待响应。HTTP 是一个同步协议，即使一个 HTTP 客户端在发送请求的时候使用异步 I/O。

每个模式都有权衡。请求/响应是一个易于理解的范式，所以设计一个 API 比设计一个消息系统感觉更自然。然而，异步消息有一些有点可以用在微服务架构：

* **降低耦合**. 消息发送不需要直到消费者
* **多订阅者**. 使用出版/订阅模型，多个消费者可以订阅来接收事件。查看 [事件驱动的架构风格][4].
* **失败孤立**. 如果消费者失败，发送者仍然可以发送消息。当消费者恢复时，消息依然可以被接收。这种能力在微服务架构中相当有用，因为每个服务都有自己的生活周期。一个服务可能变得不可获得或者随时会被新的版本替代。异步消息能够应付断续的停机事件。同步 API，另一方面，需要下流服务可获得或者操作失败。

* **响应性** 一个上流服务能够快速响应，如果它不等下流服务。这在微服务应用中相当有用。如果有一个服务依赖链（A 调用 B， B 调用 C， 等等），等待同步调用可能增加无法接收的延迟。

* **负载分级** 一个队列可以作为工作负载的分级缓冲，因此被调用者能够按照它们自己的速率处理消息。

* **工作流**. 队列可以被用来管理工作流，通过检查工作流中每一步的消息。

然而，使用异步消息有一些挑战.

* **与消息基础耦合** 使用一个特定的消息基础可能造成与基础的耦合。后期很难转换的另一个消息基础件。
* **延迟**. 高吞吐量时，在消息基础件上的金钱花费可能很重要。
* **复杂性**. 处理异步消息不是一个微不足道的任务。例如，你必须处理相同的消息，去除重复或者是让操作冥等。同样很难用异步消息实现请求-响应语意。为了发送一个响应，你需要另外一个队列，添加一种方式来关联请求与响应。
* **吞吐量**. 如果消息需要队列语意，这个队列可能成为系统的瓶颈。每个消息至少去要入队操作和弹出操作。不仅如此，队列语意通常在消息基础件中需要某种锁。如果这个队列是一个可管理的服务，可能会有附加的延迟，因为这个队列相对于簇虚拟网络是外部的。你可能想减轻这些问题通过批量消息，但是这使代码更复杂。如果这个消息不需要队列语意，你也许能够使用事件流代替队列。更多信息，参考 [事件驱动的架构风格][5]

## 消息分发：选择消息模式

后续略，想要了解更多，参考 [Designing interservice communication for microservices][0]

## 参考

[Designing interservice communication for microservices][0]

[0]: https://docs.microsoft.com/en-us/azure/architecture/microservices/design/interservice-communication
[1]: https://docs.microsoft.com/en-us/azure/architecture/patterns/retry
[2]: https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
[3]: https://docs.microsoft.com/en-us/azure/architecture/microservices/design/api-design#api-versioning
[4]: https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven
[5]: https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven