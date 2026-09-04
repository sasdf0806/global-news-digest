type Event = {
  id: number;
  title: string;
  fact_summary: string | null;
  impact_analysis: string | null;
  category: string | null;
  region: string | null;
  importance_score: number;
  last_updated_at: string;
};

type ApiResponse = { data: Event[]; request_id: string };

const apiBaseUrl =
  process.env.INTERNAL_API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

async function getEvents(searchParams: { category?: string; region?: string; keyword?: string }) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(searchParams)) {
    if (value) params.set(key, value);
  }
  const response = await fetch(`${apiBaseUrl}/events?${params.toString()}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return (await response.json()) as ApiResponse;
}

export const dynamic = "force-dynamic";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; region?: string; keyword?: string }>;
}) {
  const query = await searchParams;
  let result: ApiResponse | null = null;
  let unavailable = false;
  try {
    result = await getEvents(query);
  } catch {
    unavailable = true;
  }

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 32 }}>
      <h1>全球热点新闻智能简报</h1>
      <p>按重要性查看已发布事件，事实摘要与影响分析分开展示。</p>
      <form action="/" method="get" style={{ display: "flex", gap: 8, margin: "24px 0" }}>
        <input name="keyword" defaultValue={query.keyword} placeholder="搜索标题或事实摘要" />
        <input name="category" defaultValue={query.category} placeholder="主题" />
        <input name="region" defaultValue={query.region} placeholder="地区" />
        <button type="submit">筛选</button>
      </form>
      {unavailable ? (
        <p role="status">API 暂不可用，请确认后端已启动。</p>
      ) : (
        <section aria-label="事件列表">
          <p>本次请求 ID：{result?.request_id}</p>
          {result?.data.length ? (
            <ol>
              {result.data.map((event) => (
                <li key={event.id} style={{ marginBottom: 24 }}>
                  <h2>{event.title}</h2>
                  <p>
                    {event.category ?? "未分类"} · {event.region ?? "未知地区"} · 热度 {event.importance_score.toFixed(2)}
                  </p>
                  <p><strong>事实摘要：</strong>{event.fact_summary ?? "暂无"}</p>
                  <p><strong>影响分析：</strong>{event.impact_analysis ?? "暂无"}</p>
                </li>
              ))}
            </ol>
          ) : (
            <p>暂无符合条件的已发布事件。</p>
          )}
        </section>
      )}
      <p>
        API 健康检查： <a href="http://localhost:8000/api/health">localhost:8000/api/health</a>
      </p>
    </main>
  );
}
