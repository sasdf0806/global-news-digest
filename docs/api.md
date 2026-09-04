# API 设计草案

基础路径：`/api`

## 当前已实现

```text
GET /health
GET /events?category=&region=&keyword=&limit=&offset=
```

服务会在响应头返回 `X-Request-ID`；业务响应使用 `success/data/error/request_id` 结构。
事件列表只返回 `published` 状态，按重要性降序、更新时间降序排列；`keyword` 会同时匹配标题和事实摘要。

## 公共接口

```text
GET /reports/today
GET /reports?from=YYYY-MM-DD&to=YYYY-MM-DD
GET /reports/{date}
GET /events?category=&region=&keyword=&page=
GET /events/{id}
GET /categories
GET /regions
```

## 用户接口

```text
POST /auth/register
POST /auth/login
POST /auth/logout
GET  /user/preferences
PUT  /user/preferences
GET  /user/bookmarks
POST /user/bookmarks/{event_id}
DELETE /user/bookmarks/{event_id}
```

## 管理接口

```text
GET  /admin/sources
POST /admin/sources
PUT  /admin/sources/{id}
POST /admin/sources/{id}/test
GET  /admin/jobs
POST /admin/jobs/daily-report/run
POST /admin/events/{id}/regenerate
POST /admin/reports/{id}/publish
POST /admin/reports/{id}/withdraw
```

## 统一响应格式

```json
{
  "success": true,
  "data": {},
  "error": null,
  "request_id": "req_xxx"
}
```

## 分页格式

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100
}
```
