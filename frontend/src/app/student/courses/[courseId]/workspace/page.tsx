'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { RichTextEditor } from '@/components/editor/RichTextEditor'
import type { Note, Course } from '@/types'
import {
  FileText,
  Plus,
  ArrowLeft,
  Save,
  X,
  Lightbulb,
  BookOpen
} from 'lucide-react'

export default function WorkspacePage() {
  const router = useRouter()
  const params = useParams()
  const { user, logout } = useAuth()
  const courseId = params.courseId as string

  const [course, setCourse] = useState<Course | null>(null)
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(true)
  const [showEditor, setShowEditor] = useState(false)
  const [selectedNote, setSelectedNote] = useState<Note | null>(null)
  const [noteTitle, setNoteTitle] = useState('')
  const [noteContent, setNoteContent] = useState('')
  const [parentNoteId, setParentNoteId] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!user) {
      router.push('/login')
      return
    }
    fetchCourseData()
    fetchNotes()
  }, [user, courseId])

  const fetchCourseData = async () => {
    try {
      const { data } = await apiClient.get(`/courses/${courseId}`)
      setCourse(data)
    } catch (err) {
      console.error('Failed to fetch course', err)
      setError('无法加载课程信息')
    } finally {
      setLoading(false)
    }
  }

  const fetchNotes = async () => {
    try {
      const { data } = await apiClient.get<{notes: Note[]}>(`/notes?course_id=${courseId}`)
      setNotes(data.notes)
    } catch (err) {
      console.error('Failed to fetch notes', err)
    }
  }

  const handleCreateNote = () => {
    setSelectedNote(null)
    setNoteTitle('')
    setNoteContent('')
    setParentNoteId(null)
    setShowEditor(true)
  }

  const handleEditNote = (note: Note) => {
    setSelectedNote(note)
    setNoteTitle(note.title)
    setNoteContent(typeof note.content === 'string' ? note.content : JSON.stringify(note.content))
    setParentNoteId(null)
    setShowEditor(true)
  }

  const handleBuildOnNote = (note: Note) => {
    setSelectedNote(null)
    setNoteTitle(`回应: ${note.title}`)
    setNoteContent(`<p><strong>基于笔记：</strong>${note.title}</p><p></p><p><strong>我的想法：</strong></p><p></p>`)
    setParentNoteId(note.id)
    setShowEditor(true)
  }

  const handleSaveNote = async () => {
    if (!noteTitle.trim()) {
      setError('请输入笔记标题')
      return
    }

    setSaving(true)
    setError('')

    try {
      if (selectedNote) {
        // Update existing note
        await apiClient.put(`/notes/${selectedNote.id}`, {
          title: noteTitle,
          content: noteContent,
        })
      } else {
        // Create new note
        await apiClient.post('/notes', {
          title: noteTitle,
          content: noteContent,
          course_id: courseId,
          note_type: parentNoteId ? 'response' : 'standard',
          parent_note_id: parentNoteId,
          tags: [],
        })
      }

      setShowEditor(false)
      setNoteTitle('')
      setNoteContent('')
      fetchNotes()
    } catch (err: any) {
      setError(err.response?.data?.message || '保存失败')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setShowEditor(false)
    setNoteTitle('')
    setNoteContent('')
    setSelectedNote(null)
    setParentNoteId(null)
    setError('')
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
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => router.push('/student/courses')}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                返回课程
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-primary">
                  {course?.name || '课程工作空间'}
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  {user?.chinese_name} · {notes.length} 篇笔记
                </p>
              </div>
            </div>
            <Button variant="outline" onClick={logout}>
              退出登录
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Notes List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold">我的笔记</h2>
                <Button size="sm" onClick={handleCreateNote}>
                  <Plus className="h-4 w-4 mr-1" />
                  新建
                </Button>
              </div>

              <div className="space-y-2">
                {notes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">还没有笔记</p>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-2"
                      onClick={handleCreateNote}
                    >
                      创建第一篇笔记
                    </Button>
                  </div>
                ) : (
                  notes.map((note) => (
                    <div
                      key={note.id}
                      className={`p-3 rounded-lg border transition-colors ${
                        selectedNote?.id === note.id
                          ? 'border-primary bg-blue-50'
                          : 'border-gray-200'
                      }`}
                    >
                      <div
                        className="cursor-pointer hover:bg-gray-50 -m-3 p-3 rounded-lg"
                        onClick={() => handleEditNote(note)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-medium text-sm mb-1">
                              {note.title}
                            </h3>
                            <p className="text-xs text-gray-500">
                              {new Date(note.created_at).toLocaleDateString('zh-CN')}
                            </p>
                          </div>
                          <FileText className="h-4 w-4 text-gray-400" />
                        </div>
                      </div>
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="w-full text-xs"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleBuildOnNote(note)
                          }}
                        >
                          Build-on 接续笔记
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Scaffolds Section */}
            <div className="bg-white rounded-lg border border-gray-200 p-4 mt-4">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                <h3 className="font-semibold">脚手架模板</h3>
              </div>
              <div className="space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => {
                    setNoteContent('<p><strong>我的观点：</strong></p><p></p><p><strong>支持证据：</strong></p><p></p><p><strong>可能的反驳：</strong></p><p></p>')
                    setShowEditor(true)
                  }}
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  论证结构模板
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => {
                    setNoteContent('<p><strong>问题：</strong></p><p></p><p><strong>假设：</strong></p><p></p><p><strong>测试方法：</strong></p><p></p>')
                    setShowEditor(true)
                  }}
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  科学探究模板
                </Button>
              </div>
            </div>
          </div>

          {/* Editor / Welcome */}
          <div className="lg:col-span-2">
            {showEditor ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>
                      {selectedNote ? '编辑笔记' : '创建新笔记'}
                    </CardTitle>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleCancel}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                      {error}
                    </div>
                  )}

                  <div>
                    <Input
                      placeholder="笔记标题"
                      value={noteTitle}
                      onChange={(e) => setNoteTitle(e.target.value)}
                      className="text-lg font-semibold"
                    />
                  </div>

                  <RichTextEditor
                    content={noteContent}
                    onChange={setNoteContent}
                    placeholder="在这里开始写作..."
                  />

                  <div className="flex justify-end gap-2">
                    <Button
                      variant="outline"
                      onClick={handleCancel}
                    >
                      取消
                    </Button>
                    <Button
                      onClick={handleSaveNote}
                      disabled={saving}
                    >
                      <Save className="h-4 w-4 mr-2" />
                      {saving ? '保存中...' : '保存笔记'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
                <FileText className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                <h2 className="text-xl font-semibold mb-2">欢迎来到课程工作空间</h2>
                <p className="text-gray-600 mb-6">
                  选择左侧的笔记进行编辑，或创建一篇新笔记开始学习
                </p>
                <Button onClick={handleCreateNote}>
                  <Plus className="h-4 w-4 mr-2" />
                  创建第一篇笔记
                </Button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
