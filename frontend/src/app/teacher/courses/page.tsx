'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { Course } from '@/types'

export default function TeacherCoursesPage() {
  const router = useRouter()
  const { user, logout } = useAuth()
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    access_code: '',
  })
  const [error, setError] = useState('')

  useEffect(() => {
    if (user?.role !== 'teacher') {
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

  const handleCreateCourse = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    try {
      await apiClient.post('/courses', formData)
      setShowCreateDialog(false)
      setFormData({ name: '', description: '', access_code: '' })
      alert('课程创建成功！')
      fetchCourses()
    } catch (err: any) {
      setError(err.response?.data?.message || '创建失败')
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
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-primary">
                知识交互论坛 - 教师管理
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                欢迎，{user?.chinese_name} 老师
              </p>
            </div>
            <div className="flex gap-2">
              <Button onClick={() => setShowCreateDialog(true)}>
                创建课程
              </Button>
              <Button variant="outline" onClick={logout}>
                退出登录
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">我的课程</h2>
          <p className="text-gray-600">
            管理您创建的所有课程
          </p>
        </div>

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
                <div className="bg-gray-50 p-3 rounded mb-4">
                  <p className="text-xs text-gray-500 mb-1">访问代码</p>
                  <p className="font-mono font-bold text-primary">
                    {course.access_code}
                  </p>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>📚 {course.note_count} 笔记</span>
                  <span>👥 {course.member_count} 成员</span>
                </div>
                <Button className="w-full" variant="outline">
                  进入课程
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {courses.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">
              您还没有创建任何课程
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              创建第一个课程
            </Button>
          </div>
        )}
      </main>

      {showCreateDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>创建新课程</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateCourse} className="space-y-4">
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                    {error}
                  </div>
                )}

                <div className="space-y-2">
                  <Label htmlFor="name">课程名称 *</Label>
                  <Input
                    id="name"
                    placeholder="例如：计算思维"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">课程描述</Label>
                  <textarea
                    id="description"
                    placeholder="介绍课程内容..."
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="flex min-h-[80px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="access_code">访问代码 *</Label>
                  <Input
                    id="access_code"
                    placeholder="6-12位字母数字组合"
                    value={formData.access_code}
                    onChange={(e) => setFormData({ ...formData, access_code: e.target.value })}
                    required
                  />
                  <p className="text-xs text-gray-500">
                    学生需要此代码才能加入课程
                  </p>
                </div>

                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    className="flex-1"
                    onClick={() => {
                      setShowCreateDialog(false)
                      setFormData({ name: '', description: '', access_code: '' })
                      setError('')
                    }}
                  >
                    取消
                  </Button>
                  <Button type="submit" className="flex-1">
                    创建
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
