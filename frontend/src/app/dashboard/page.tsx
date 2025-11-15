'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'

export default function DashboardPage() {
  const router = useRouter()
  const { user, loading } = useAuth()

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push('/login')
      } else if (user.role === 'student') {
        router.push('/student/courses')
      } else if (user.role === 'teacher') {
        router.push('/teacher/courses')
      } else if (user.role === 'admin') {
        router.push('/admin/applications')
      }
    }
  }, [user, loading, router])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-gray-600">加载中...</p>
    </div>
  )
}
