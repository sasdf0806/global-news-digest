# 系统架构设计

## 1. 服务划分

```text
apps/web
  Web 页面、用户交互、管理后台

services/api
  认证、新闻查询、日报查询、管理接口

services/worker
  采集、清洗、翻译、去重、聚类、排序、摘要、日报生成

infra/docker-compose.yml
  PostgreSQL、Redis、Keycloak、Flower、可选 RSSHub 和观测组件

database
  PostgreSQL 保存业务数据和任务状态

future/channels
  DingTalk、微信公众号、邮件、Webhook 等渠道适配器
```

## 2. 任务流水线

```text
collect → normalize → deduplicate → cluster → rank → summarize → publish
```

每一步都应有明确输入、输出和状态，失败可从最近一个成功步骤继续执行。V1 使用 Celery + Redis，任务由数据库 `job_runs.run_key` 保证幂等；复杂长流程保留迁移到 Temporal 的边界。

## 3. 推荐目录

```text
apps/web/
services/api/
services/worker/
packages/shared/
tests/
infra/
```

`packages/shared` 保存跨服务纯函数和契约；TypeScript API 类型优先从 FastAPI OpenAPI 自动生成，避免手工重复定义。

## 4. 组件职责

### Web 前端

只负责展示和用户交互，不直接调用新闻源或模型服务。

### API 服务

负责权限校验、查询、筛选、后台管理和任务触发。

### Worker

负责耗时任务，禁止在 Web 请求中同步执行抓取和 AI 生成。

### 数据库

保存新闻、事件、日报、用户偏好、任务记录和审计记录。

## 5. 推送扩展接口

```python
class NotificationChannel:
    name: str

    def send(self, report: dict, target: dict) -> dict:
        """发送统一日报对象并返回渠道结果。"""
        raise NotImplementedError
```

第一阶段只实现空适配器或日志适配器，避免业务代码绑定具体平台。
