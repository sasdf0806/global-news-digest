# 第三方源码子模块

本目录只放需要独立运行、审计或后续维护的完整应用源码：

- `rsshub`：非标准来源适配器，AGPL-3.0，通过 Compose `feeds` profile 使用。
- `miniflux`：可选 RSS 阅读器和来源管理服务，Apache-2.0，通过 Compose `feeds` profile 使用。

更新子模块后必须记录上游提交、许可证变化和本地兼容性验证结果。Python/Node 框架不复制到此目录，而是通过锁定依赖管理。
