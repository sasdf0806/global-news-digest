import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Global News Digest",
  description: "全球热点新闻智能简报",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
