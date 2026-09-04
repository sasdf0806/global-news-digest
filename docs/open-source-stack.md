# 开源组件与维护边界

调研日期：2026-09-02。

## 结论

V1 采用少量、边界清晰的成熟组件：PostgreSQL + pgvector 作为统一数据层，FastAPI 提供 REST API，Celery 负责后台任务，Keycloak 负责身份认证，Next.js 提供 Web 产品。模型网关暂保留 LiteLLM 作为候选，当前 Mock 模式不引入远程模型依赖。

框架包通过 Python/Node 包管理器锁定版本，基础设施通过 Docker 镜像锁定版本；不把 FastAPI、Next.js、PostgreSQL 等第三方框架源码作为 Git 子模块。将完整框架源码复制到本仓库会造成重复构建、许可证边界混乱和升级困难。

RSSHub 和 Miniflux 是可独立运行的完整应用，分别通过 `feeds` profile 或外部部署接入，不与核心业务代码耦合。
它们的源码分别位于 `vendor/rsshub` 和 `vendor/miniflux` Git 子模块，升级时只更新子模块指针并记录兼容性验证结果。

## 组件事实与用途

| 组件 | 事实 | 本项目用途 | 边界/风险 |
|---|---|---|---|
| [feedparser](https://github.com/kurtmckee/feedparser) | Python RSS/Atom/JSON Feed 解析库 | 采集标准新闻源 | 仍需自行处理来源限流、超时和幂等 |
| [trafilatura](https://github.com/adbar/trafilatura) | Web 正文和元数据抽取，Apache-2.0 | 允许时抽取正文摘要 | 不默认长期保存完整正文 |
| [Miniflux](https://github.com/Miniflux/v2) | 支持 RSS/Atom/JSON Feed、分类、书签和正文提取的独立阅读器，Apache-2.0 | 可选的来源管理/阅读器旁路 | 不作为核心数据源，避免重复建模 |
| [RSSHub](https://github.com/DIYgod/RSSHub) | 大量站点适配器，AGPL-3.0 | 可选非标准来源扩展 | 独立容器部署并进行许可证与来源条款审查 |
| [Celery](https://github.com/celery/celery) | 分布式 Python 任务队列，New BSD | 采集、处理、日报和定时任务 | 幂等键仍由业务数据库保证 |
| [Temporal Python SDK](https://github.com/temporalio/sdk-python) | 持久化、容错工作流编排，MIT | 后续复杂工作流升级路径 | V1 暂不引入 Temporal Server |
| [pgvector](https://github.com/pgvector/pgvector) | PostgreSQL 向量近邻搜索扩展 | 新闻相似度和事件聚类 | 百万级以上再评估独立向量库 |
| [sentence-transformers](https://github.com/UKPLab/sentence-transformers) | embedding、相似度和 reranker 框架，Apache-2.0 | 多语言新闻向量化 | 模型权重许可证需单独核对 |
| [LiteLLM](https://github.com/BerriAI/litellm) | 统一调用 100+ LLM 的 OpenAI 兼容网关 | 后续接入摘要、翻译、fallback、成本统计的候选 | 当前未安装；启用前需评估依赖体积、许可证和供应商密钥管理 |
| [Keycloak](https://github.com/keycloak/keycloak) | 开源 IAM，支持用户管理、联邦和细粒度授权，Apache-2.0 | OIDC 登录和 admin/user RBAC | 本地使用 dev 模式，生产需独立数据库和 HTTPS |
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | 厂商无关的 traces/metrics/logs 收集器，Apache-2.0 | 统一观测数据出口 | 本地默认只启动 debug exporter |

## 事实、摘要和分析的数据边界

- 原始新闻只保留来源、标题、摘要、发布时间、URL 和内容指纹。
- `fact_summary`、`key_facts` 与 `impact_analysis` 使用不同字段和不同提示词版本。
- 模型输出必须通过 Pydantic schema 校验；缺少来源链接的事件不得发布。
- 转载/近似新闻先做 URL、SHA-256、SimHash/MinHash，再做向量相似度。

## 依赖和版本策略

- Python 依赖：`services/api/requirements.lock`、`services/worker/requirements.lock`。
- Node 依赖：`apps/web/package-lock.json`。
- 基础设施：`infra/docker-compose.yml` 中使用固定主版本或版本标签。
- 模型权重不直接提交 Git；通过镜像启动或首次运行时下载到 Docker volume。
- 只有需要独立开发、独立构建的完整应用才考虑 Git 子模块；当前仓库暂不添加框架源码子模块。

## 升级路径

1. Celery → Temporal：出现长时间、跨服务、需要暂停/补偿的工作流时。
2. pgvector → Qdrant/OpenSearch：向量或全文数据达到独立扩缩容规模时。
3. Docker Compose → Kubernetes：需要多环境编排和水平自动扩容时。
4. 远程 LLM → vLLM/Ollama：需要本地模型、成本控制或离线运行时。
