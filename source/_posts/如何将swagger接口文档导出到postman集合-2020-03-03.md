---
title: 如何将swagger接口文档导出到postman集合
tags:
  - swagger
  - open-api2.0
  - postman
categories:
  - api
  - postman
  - swagger
img: /images/swagger.jpg
date: 2020-03-03 17:50:16
---


`Swagger` 是强大的面向接口定义、自动生成接口文档的工具，支持导出 `open-api2.0` 格式接口文档。Postman 是强大的接口测试工具，这两种工具的结合将摩擦出怎样的火花？

<!-- more -->

在 spring boot 项目中导入 Swagger 的 maven 依赖，通过在 controller 中添加标记，便可在 swagger-ui 中生成接口文档。在 swagger-ui 页面，打开浏览器开发者工具，刷新页面，发现 swagger-ui 的生成的 `open-api2.0` 文档在 [http://localhost:9031/v2/api-docs][1] 接口，是符合 `open-api2.0` 定义的 json 数据。

![postman import open-api2.0][2]

打开 `postman`, 选择导入->从链接导入，粘贴 [http://localhost:9031/v2/api-docs][1] 即可导入到 postman 集合中。

[0]: https://swagger.io/
[1]: http://localhost:9031/v2/api-docs
[2]: /images/postman-import-open-api2.jpg