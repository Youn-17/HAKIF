export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold text-primary">
        Human-AI Knowledge Interaction Forum
      </h1>
      <p className="mt-4 text-lg text-gray-600">
        知识交互论坛 - 混合架构版本
      </p>
      <div className="mt-8 space-y-2">
        <p>✅ Flask后端 (Python 3.12+)</p>
        <p>✅ Next.js前端 (TypeScript)</p>
        <p>✅ PostgreSQL数据库</p>
        <p>✅ FastAPI AI服务</p>
      </div>
    </main>
  )
}
