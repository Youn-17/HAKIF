'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import type { User, LoginRequest, RegisterRequest, AuthResponse } from '@/types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        const { data } = await apiClient.get('/auth/me')
        setUser(data)
      } catch (error) {
        localStorage.removeItem('access_token')
      }
    }
    setLoading(false)
  }

  const login = async (credentials: LoginRequest) => {
    const { data } = await apiClient.post<AuthResponse>('/auth/login', credentials)
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    setUser(data.user)
  }

  const register = async (userData: RegisterRequest) => {
    const { data } = await apiClient.post<AuthResponse>('/auth/register', userData)
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    setUser(data.user)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
