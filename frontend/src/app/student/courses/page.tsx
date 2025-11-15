'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { Course } from '@/types'

export default function StudentCoursesPage() {
  const router = useRouter()
  const { user, logout } = useAuth()
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [showJoinDialog, setShowJoinDialog] = useState(false)
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null)
  const [accessCode, setAccessCode] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (user?.role !== 'student') {
      router.push('/dashboard')
      return
    }
    fetchCourses()
  }, [user])

  const fetchCourses = async () => {
    try {
      const { data } = await apiClient.get<{courses: Course[]}>('/courses')
      setCourses(data.courses)
    } catch (err) {
      console.error('Failed to fetch courses', err)
    } finally {
      setLoading(false)
    }
  }

  const handleJoinCourse = async () => {
    if (!selectedCourse) return
    setError('')

    try {
      await apiClient.post(`/courses/${selectedCourse.id}/join`, {
        access_code: accessCode
      })
      setShowJoinDialog(false)
      setAccessCode('')
      alert('成功加入课程！')
      fetchCourses()
    } catch (err: any) {
      setError(err.response?.data?.message || '加入失败')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>加载中...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航栏 */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-primary">
                知识交互论坛
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                欢迎，{user?.chinese_name}
              </p>
            </div>
            <Button variant="outline" onClick={logout}>
              退出登录
            </Button>
          </div>
        </div>
      </header>

      {/* 主要内容 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">课程大厅</h2>
          <p className="text-gray-600">
            浏览所有课程，输入访问代码加入课程
          </p>
        </div>

        {/* 课程网格 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Card key={course.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="text-lg">{course.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                  {course.description}
                </p>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>📚 {course.note_count} 笔记</span>
                  <span>👥 {course.member_count} 成员</span>
                </div>
                <Button
                  className="w-full"
                  onClick={() => {
                    setSelectedCourse(course)
                    setShowJoinDialog(true)
                  }}
                >
                  加入课程
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {courses.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">暂无可用课程</p>
          </div>
        )}
      </main>

      {/* 加入课程对话框 */}
      {showJoinDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>加入课程：{selectedCourse?.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}
              
              <div className="space-y-2">
                <label className="text-sm font-medium">课程访问代码</label>
                <Input
                  placeholder="输入访问代码"
                  value={accessCode}
                  onChange={(e) => setAccessCode(e.target.value)}
                />
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => {
                    setShowJoinDialog(false)
                    setAccessCode('')
                    setError('')
                  }}
                >
                  取消
                </Button>
                <Button
                  className="flex-1"
                  onClick={handleJoinCourse}
                  disabled={!accessCode}
                >
                  确认加入
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
