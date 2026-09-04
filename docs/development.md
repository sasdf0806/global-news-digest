# 本地开发

## 前置条件

- Docker 29+
- Docker Compose v2+
- Git

本机无需安装 Python 或 Node，依赖在容器内安装。

## 初始化

```bash
git submodule update --init --recursive
cp config/.env.example .env
docker compose -f infra/docker-compose.yml build
docker compose -f infra/docker-compose.yml up -d
```

访问：

- Web：http://localhost:3000
- API 文档：http://localhost:8000/docs
- API 健康检查：http://localhost:8000/api/health
- Celery Flower：http://localhost:5555
- Keycloak：http://localhost:8080（开发管理员：`admin` / `change_me`，首次启动后请立即修改）

可选启动来源扩展和观测组件：

```bash
docker compose -f infra/docker-compose.yml --profile feeds up -d
docker compose -f infra/docker-compose.yml --profile observability up -d
```

## 数据库迁移

API 容器启动时自动执行 `alembic upgrade head`。新增表结构必须提交迁移脚本，不允许直接修改运行中的数据库。

## 常用命令

```bash
docker compose -f infra/docker-compose.yml logs -f api worker
docker compose -f infra/docker-compose.yml exec api alembic current
docker compose -f infra/docker-compose.yml exec worker celery -A app.celery_app inspect ping
docker compose -f infra/docker-compose.yml down
```

API 启动后，从 OpenAPI 规范生成前端类型，避免手工同步接口：

```bash
cd apps/web
npm run generate:api
```

Web 容器服务端渲染通过 `INTERNAL_API_BASE_URL=http://api:8000/api` 访问 API；浏览器端链接使用 `NEXT_PUBLIC_API_BASE_URL`。

## 环境和密钥

`.env` 仅用于本地，不提交真实 API Key、Webhook、数据库密码。AI、采集和定时任务都应使用 Mock 模式或本地服务进行测试。
