# Global News Digest

全球热点新闻智能简报 Web 系统。

> 当前状态：开发准备（V1.0）。业务代码尚未开始实现。

## 项目定位

每天自动采集全球公开新闻源，完成清洗、翻译、去重、事件聚类、热点排序和中文摘要生成，并通过 Web 页面提供当日简报与历史检索。

第一阶段只建设 Web 产品；钉钉、微信公众号、邮件等渠道作为后续扩展，不进入 V1.0 的交付范围。

## 文档入口

- [项目规范](./PROJECT_SPEC.md)
- [系统架构](./docs/architecture.md)
- [数据模型](./docs/data-model.md)
- [API 设计](./docs/api.md)
- [开发路线图](./docs/roadmap.md)
- [环境变量模板](./config/.env.example)
- [GitHub 操作与 Token 配置](./docs/github.md)
- [开发协作规范](./AGENTS.md)

## 推荐技术栈

- 前端：Next.js + React + TypeScript
- 后端：FastAPI + Python
- 数据库：PostgreSQL
- 任务处理：Python Worker
- 缓存/队列：Redis（V1.1 引入）
- 部署：Docker

## 目录约定

```text
global-news-digest/
├─ docs/              设计和接口文档
├─ config/            环境变量和配置模板
├─ scripts/           运维和本地辅助脚本
├─ apps/web/          前端应用（待创建）
├─ services/api/      后端 API（待创建）
├─ services/worker/   采集、处理和日报任务（待创建）
├─ tests/             测试代码（待创建）
└─ PROJECT_SPEC.md    项目总规范
```

## 开发原则

1. 新闻内容处理、Web 展示和未来推送渠道必须解耦。
2. 所有新闻都必须保留原始来源与原文链接。
3. 事实摘要和模型分析分开存储、分开展示。
4. 所有定时任务必须具备幂等性、重试和可观测日志。
5. 优先使用 RSS/API，遵守来源网站的版权和使用条款。

## 本地初始化

```bash
cp config/.env.example .env
```

按需填写本地开发配置；`.env` 不应提交到 Git。当前仓库已包含 GitHub Actions 基线检查，后续添加前端、API 和 Worker 实现后，应在对应目录补充格式化、类型检查和测试步骤。

## GitHub 协作

- 提交信息使用 `feat:`、`fix:`、`docs:`、`test:` 等前缀。
- Pull Request 请参考仓库模板，并同步更新文档与测试。
- 安全问题请参考 [SECURITY.md](./SECURITY.md)，不要公开提交密钥或用户数据。
