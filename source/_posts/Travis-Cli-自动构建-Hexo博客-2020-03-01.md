---
title: Travis-Cli-自动构建-Hexo博客
date: 2020-03-01 23:23:09
tags:
  - CI
  - Travis-CI
  - 持续集成
categories:
  - CI
  - Travis-CI
  - 工具
img: /images/travis-ci.jpg
---

Travis-Cli 是一种持续集成构建部署服务，支持自动化构建测试部署。我们可以用它来自动编译发布部署我们的 hexo github page 博客。

<!-- more -->

使用 Travis-Cli 持续集成构建服务，当我们将 `Hexo 博客源码`推送到 Github 仓库库，`travis-cli` 察觉到这次推送，自动从 `Github 仓库`拉取代码并构建，构建完成后，将结果推送到 `master 分支`。

在项目文件下添加 `Travis-Cli` 构建配置文件 `.travis.yml`, 内容如下参考. `$GH_TOKEN` 是需要在 [travis-cli][0] 站点添加的环境变量，这个 TOKEN 是在 `Github 项目设置页`生成的项目 TOKEN。

```yml
sudo: false
language: node_js
node_js:
  - 10 # use nodejs v10 LTS
cache: npm
branches:
  only:
    - hexo # build hexo branch only
script:
  - hexo generate # generate static files
deploy:
  provider: pages
  skip-cleanup: true
  github-token: $GH_TOKEN
  keep-history: true
  target_branch: master
  on:
    branch: hexo
  local-dir: public
```

以上的 `target_branch: master` 的意思是构建成功后部署到 master 分支；`local-dir` 的意思是，hexo 构建完成后的结果在 `public 文件夹`，这个文件夹里的结果将被推送到 `Github Page` 的 `master` 分支。on->branch: hexo 的意思是 hexo 博客的源码在 Github 的 `hexo 分支`，`travis-cli` 将从 Github 的 `hexo 分支`拉取代码进行构建。

[0]: https://travis-ci.com/