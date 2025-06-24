'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faEdit, faTrash, faEye } from '@fortawesome/free-solid-svg-icons'
import Layout from '@/components/Layout'
import { useAuthStore } from '@/stores/authStore'
import axios from '@/lib/axios'
import toast from 'react-hot-toast'

interface Idea {
  id: number
  title: string
  content: string
  created_at: string
  updated_at?: string
}

export default function IdeasPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [ideas, setIdeas] = useState<Idea[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchIdeas()
  }, [isAuthenticated, router])

  const fetchIdeas = async () => {
    try {
      const response = await axios.get('/ideas')
      setIdeas(response.data)
    } catch (error) {
      console.error('Failed to fetch ideas:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('このアイデアを削除してもよろしいですか？')) {
      return
    }

    try {
      await axios.delete(`/ideas/${id}`)
      setIdeas(ideas.filter(idea => idea.id !== id))
      toast.success('アイデアを削除しました')
    } catch (error) {
      console.error('Failed to delete idea:', error)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">アイデア一覧</h2>
        <Link href="/ideas/new" className="btn-primary flex items-center space-x-2">
          <FontAwesomeIcon icon={faPlus} />
          <span>新規作成</span>
        </Link>
      </div>

      {ideas.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">アイデアがまだありません</p>
          <Link href="/ideas/new" className="btn-secondary">
            最初のアイデアを作成
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {ideas.map((idea) => (
            <div key={idea.id} className="card hover:shadow-xl">
              <h3 className="text-lg font-bold text-gray-900 mb-2">{idea.title}</h3>
              <p className="text-gray-600 mb-4 line-clamp-3">{idea.content}</p>
              <div className="text-sm text-gray-500 mb-4">
                作成日: {formatDate(idea.created_at)}
              </div>
              <div className="flex justify-end space-x-2">
                <Link
                  href={`/ideas/${idea.id}`}
                  className="text-secondary-600 hover:text-secondary-700"
                  title="詳細を見る"
                >
                  <FontAwesomeIcon icon={faEye} />
                </Link>
                <Link
                  href={`/ideas/${idea.id}/edit`}
                  className="text-primary-600 hover:text-primary-700"
                  title="編集"
                >
                  <FontAwesomeIcon icon={faEdit} />
                </Link>
                <button
                  onClick={() => handleDelete(idea.id)}
                  className="text-red-600 hover:text-red-700"
                  title="削除"
                >
                  <FontAwesomeIcon icon={faTrash} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}