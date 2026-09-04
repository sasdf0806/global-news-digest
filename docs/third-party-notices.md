# 第三方组件声明

本仓库通过锁定依赖和 Git 子模块使用第三方开源组件。各组件的完整许可证文本保留在其发行包、镜像或子模块中。

## 源码子模块

- `vendor/rsshub`：RSSHub，AGPL-3.0，许可证见子模块 `LICENSE`。
- `vendor/miniflux`：Miniflux，Apache-2.0，许可证见子模块 `LICENSE`。

## 运行时依赖

FastAPI、SQLAlchemy、Alembic、Celery、feedparser、trafilatura、pgvector、sentence-transformers、Next.js、React、TanStack Query 和 OpenTelemetry 等组件均按各自上游许可证使用。LiteLLM 当前仅作为后续模型网关候选，尚未纳入运行时依赖。发布前应从锁定版本生成完整 SBOM，并复核模型权重、新闻源条款及其数据使用限制。
