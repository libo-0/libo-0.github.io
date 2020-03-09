---
title: Git-Submodule-学习
date: 2020-03-02 12:08:01
tags:
  - Git
  - Git-Submodule
categories:
  - Git
img: /images/git.jpg
---

Git 命令用法，tag， submodule。

<!-- more -->

## Git clone 

1. 递归克隆，包含子模块

`git clone --recursive [URL to Git repo]`

## Git tag

Git tag 用于打标签，打一次标签对应 GitHub 的一次源码 release。

`git tab v1.0.0`
`git push master v1.0.0`

## Git submodule

Git 支持子模块，子模块也是一个 Git 项目。Git 不能在父项目提交子项目模块的代码。子项目只能在自己的 Git 项目提交。

1. 添加子模块

`git submodule add http://github.com/libo-0/hexo-theme-matery.git themes/matery`

上述命令会在当前项目目录创建 theme/matery 目录追踪之前的 Git 仓库。

2. 更新子模块

`git submodule update --remote`

3. 拉取子模块

`git submodule update --init`

4. 拉取包含子模块的子模块

`git submodule update --init --recursive`

5. 同时下载多个子模块

`git submodule update --init --recursive --jobs 8`

`git clone --recursive --jobs 8 [URL to Git repo]`

```bash
# short version
git submodule update --init --recursive -j 8
```

6. 拉取子模块

```bash
# 拉取包含子模块的改变
git pull --recurse-submodules

# 拉取所有子模块的改变
git submodule update --remote
```

7. 在每个子模块执行命令

```bash
git submodule foreach 'git reset --hard'
# 包含嵌套子模块
git submodule foreach --recursive 'git reset --hard'
```

8. 添加子模块到一个仓库

`git submodule init` 会为子模块创建配置文件，如果配置文件不存在

```bash
git submodule add -b master [URL to Git repo]
git submodule init
```

9. 删除子模块

当前 Git 没有提供标准的接口来删除一个子模块。为了删除一个子模块，你需要做

```bash
git submodule deinit -f — mymodule
rm -rf .git/modules/mymodule
git rm -f mymodule
```

## Git 同时 push 到多个远程仓库

`git remote set-url --add origin git@github.com:warmfrog/warmfrog.github.io.git`

## 参考

[Using submodules in Git - Tutorial][0]


[0]: https://www.vogella.com/tutorials/GitSubmodules/article.html