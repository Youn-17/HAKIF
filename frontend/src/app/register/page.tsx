'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function RegisterPage() {
  const router = useRouter()
  const { register } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    chinese_name: '',
    pinyin_first_name: '',
    pinyin_family_name: '',
    phone: '',
    gender: '男' as '男' | '女' | '其他',
    school: '',
    major: '',
    role: 'student' as 'student' | 'teacher',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('两次输入的密码不一致')
      return
    }

    if (!/^[a-zA-Z]+$/.test(formData.pinyin_first_name) ||
        !/^[a-zA-Z]+$/.test(formData.pinyin_family_name)) {
      setError('拼音姓名必须是英文字母')
      return
    }

    setLoading(true)

    try {
      const { confirmPassword, ...registerData } = formData
      await register(registerData)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.message || '注册失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-orange-50 p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle className="text-center text-primary">
            知识交互论坛 - 注册
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label>角色类型</Label>
              <div className="flex gap-4">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="radio"
                    value="student"
                    checked={formData.role === 'student'}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value as 'student' })}
                    className="w-4 h-4 text-primary"
                  />
                  <span>学生</span>
                </label>
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="radio"
                    value="teacher"
                    checked={formData.role === 'teacher'}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value as 'teacher' })}
                    className="w-4 h-4 text-primary"
                  />
                  <span>教师</span>
                </label>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="email">邮箱 *</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">手机号 *</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="13800138000"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="password">密码 *</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword">确认密码 *</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="chinese_name">中文姓名 *</Label>
                <Input
                  id="chinese_name"
                  placeholder="张三"
                  value={formData.chinese_name}
                  onChange={(e) => setFormData({ ...formData, chinese_name: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="pinyin_first_name">拼音名 *</Label>
                <Input
                  id="pinyin_first_name"
                  placeholder="San"
                  value={formData.pinyin_first_name}
                  onChange={(e) => setFormData({ ...formData, pinyin_first_name: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="pinyin_family_name">拼音姓 *</Label>
                <Input
                  id="pinyin_family_name"
                  placeholder="Zhang"
                  value={formData.pinyin_family_name}
                  onChange={(e) => setFormData({ ...formData, pinyin_family_name: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="gender">性别 *</Label>
                <select
                  id="gender"
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value as '男' | '女' | '其他' })}
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
                  required
                >
                  <option value="男">男</option>
                  <option value="女">女</option>
                  <option value="其他">其他</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="school">学校 *</Label>
                <Input
                  id="school"
                  placeholder="北京大学"
                  value={formData.school}
                  onChange={(e) => setFormData({ ...formData, school: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="major">专业 *</Label>
                <Input
                  id="major"
                  placeholder="计算机科学"
                  value={formData.major}
                  onChange={(e) => setFormData({ ...formData, major: e.target.value })}
                  required
                />
              </div>
            </div>

            {formData.role === 'teacher' && (
              <div className="bg-yellow-50 border border-yellow-200 px-4 py-3 rounded">
                <p className="text-sm text-yellow-800">
                  📌 教师注册需要管理员审核，审核通过后您将收到邮件通知。
                </p>
              </div>
            )}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? '注册中...' : '注册'}
            </Button>

            <div className="text-center text-sm text-gray-600">
              已有账号？{' '}
              <Link href="/login" className="text-primary hover:underline">
                立即登录
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
