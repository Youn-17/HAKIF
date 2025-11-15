export interface User {
  id: string
  email: string
  chinese_name: string
  pinyin_first_name: string
  pinyin_family_name: string
  phone?: string
  gender: string
  school: string
  major: string
  role: 'student' | 'teacher' | 'admin'
  avatar_url?: string
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  chinese_name: string
  pinyin_first_name: string
  pinyin_family_name: string
  phone: string
  gender: '男' | '女' | '其他'
  school: string
  major: string
  role: 'student' | 'teacher'
  additional_info?: Record<string, any>
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface Course {
  id: string
  name: string
  description: string
  access_code: string
  created_by: string
  is_active: boolean
  member_count: number
  note_count: number
  created_at: string
}

export interface Note {
  id: string
  title: string
  content: any
  author_id: string
  course_id: string
  note_type: 'standard' | 'response' | 'synthesis'
  tags: string[]
  created_at: string
  updated_at: string
}
