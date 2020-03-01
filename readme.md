# Hexo 生成的静态博客站点

1. 创建一篇博客

`hexo new Postman-用法学习`

2. 出版博客

`hexo publish Postman-用法学习`

3. 生成博客

`hexo generate`

4. 清除生成内容

`hexo clean`

5. 本地预览博客

`hexo server`

6. 部署博客

`hexo clean && hexo deploy`

在 [_config.yml](_config.yml) 中配置了 git 部署和 rsync 部署, 通过一键部署即可同时部署到 gitee pages，github pages，和阿里云 nginx 服务器。密匙保存在本地 ~/.ssh/id_rsa, id_rsa.pub 分别保存在 gitee 配置， github 配置， 以及阿里云服务器，通过 ssh 协议直接部署。


