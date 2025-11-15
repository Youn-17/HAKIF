'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface Application {
  id: string
  applicant: {
    chinese_name: string
    email: string
    phone: string
    school: string
    major: string
  }
  application_info: Record<string, any>
  status: string
  applied_at: string
}

export default function AdminApplicationsPage() {
  const router = useRouter()
  const { user, logout } = useAuth()
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user?.role !== 'admin') {
      router.push('/dashboard')
      return
    }
    fetchApplications()
  }, [user])

  const fetchApplications = async () => {
    try {
      const { data } = await apiClient.get<{applications: Application[]}>('/admin/teacher-applications')
      setApplications(data.applications)
    } catch (err) {
      console.error('Failed to fetch applications', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReview = async (appId: string, action: 'approved' | 'rejected') => {
    try {
      await apiClient.put(`/admin/teacher-applications/${appId}/review`, {
        action,
        comment: action === 'approved' ? '审核通过' : '审核未通过'
      })
      alert(`已${action === 'approved' ? '批准' : '拒绝'}申请`)
      fetchApplications()
    } catch (err: any) {
      alert('操作失败：' + (err.response?.data?.message || '未知错误'))
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
                管理员面板
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                审核教师注册申请
              </p>
            </div>
            <Button variant="outline" onClick={logout}>
              退出登录
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">待审核教师申请</h2>
          <p className="text-gray-600">
            共 {applications.length} 个待审核申请
          </p>
        </div>

        <div className="space-y-4">
          {applications.map((app) => (
            <Card key={app.id}>
              <CardHeader>
                <CardTitle className="text-lg">
                  {app.applicant.chinese_name} - {app.applicant.school}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-500">邮箱</p>
                    <p className="font-medium">{app.applicant.email}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">手机</p>
                    <p className="font-medium">{app.applicant.phone}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">学校</p>
                    <p className="font-medium">{app.applicant.school}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">专业领域</p>
                    <p className="font-medium">{app.applicant.major}</p>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="default"
                    onClick={() => handleReview(app.id, 'approved')}
                  >
                    批准
                  </Button>
                  <Button
                    variant="destructive"
                    onClick={() => handleReview(app.id, 'rejected')}
                  >
                    拒绝
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {applications.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">暂无待审核申请</p>
          </div>
        )}
      </main>
    </div>
  )
}
