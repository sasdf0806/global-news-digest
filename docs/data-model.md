# 数据模型设计

## sources 新闻源

```text
id, name, url, type, language, region, category,
weight, enabled, last_success_at, last_error, created_at, updated_at
```

## news_items 原始新闻

```text
id, source_id, title, original_title, summary, url,
language, region, category, published_at, fetched_at,
content_hash, status, created_at
```

## events 聚合事件

```text
id, title, summary, analysis, category, region,
importance_score, first_seen_at, last_updated_at, status,
created_at, updated_at
```

## event_news 事件与新闻关联

```text
event_id, news_item_id, similarity_score, created_at
```

## daily_reports 每日日报

```text
id, report_date, title, content_json, content_markdown,
status, generated_at, published_at, version, created_at
```

## users 用户

```text
id, email, password_hash, role, status, created_at, updated_at
```

## user_preferences 用户偏好

```text
user_id, topics_json, regions_json, language,
display_count, show_analysis, updated_at
```

## job_runs 任务执行记录

```text
id, job_name, run_key, status, started_at, finished_at,
retry_count, error_message, metrics_json
```

## audit_logs 审计日志

```text
id, user_id, action, resource_type, resource_id,
before_json, after_json, created_at
```
