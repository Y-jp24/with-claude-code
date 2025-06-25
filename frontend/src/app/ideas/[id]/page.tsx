'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { 
  faArrowLeft, faEdit, faRobot, faComment, faBookmark, faShare 
} from '@fortawesome/free-solid-svg-icons'
import Layout from '../../../components/Layout'
import axios from '../../../lib/axios'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'

interface Idea {
  id: number
  title: string
  content: string
  created_at: string
  updated_at?: string
  requirements: Requirement[]
  comments: Comment[]
  bookmarks: Bookmark[]
}

interface Requirement {
  id: number
  content: string
  llm_model: string
  created_at: string
}

interface Comment {
  id: number
  content: string
  created_at: string
}

interface Bookmark {
  id: number
  note?: string
  position: any
  created_at: string
}

export default function IdeaDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [idea, setIdea] = useState<Idea | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [selectedModel, setSelectedModel] = useState<'openai' | 'google' | 'claude'>('openai')

  useEffect(() => {
    fetchIdea()
  }, [params.id])

  const fetchIdea = async () => {
    try {
      const response = await axios.get(`/ideas/${params.id}`)
      setIdea(response.data)
    } catch (error) {
      console.error('Failed to fetch idea:', error)
      toast.error('アイデアの取得に失敗しました')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateRequirement = async () => {
    setIsGenerating(true)
    try {
      const response = await axios.post('/requirements/generate', {
        idea_id: parseInt(params.id),
        llm_model: selectedModel
      })
      toast.success('要件定義書を生成しました')
      fetchIdea() // リロードして新しい要件定義を表示
    } catch (error) {
      console.error('Failed to generate requirement:', error)
    } finally {
      setIsGenerating(false)
    }
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

  if (!idea) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-500">アイデアが見つかりません</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex justify-between items-start">
          <button
            onClick={() => router.back()}
            className="text-gray-600 hover:text-gray-800 flex items-center space-x-2"
          >
            <FontAwesomeIcon icon={faArrowLeft} />
            <span>戻る</span>
          </button>
          <div className="flex space-x-2">
            <Link
              href={`/ideas/${params.id}/edit`}
              className="btn-outline flex items-center space-x-2"
            >
              <FontAwesomeIcon icon={faEdit} />
              <span>編集</span>
            </Link>
          </div>
        </div>

        <div className="card mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{idea.title}</h1>
          <div className="prose max-w-none">
            <p className="whitespace-pre-wrap">{idea.content}</p>
          </div>
        </div>

        {/* 要件定義書生成セクション */}
        <div className="card mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <FontAwesomeIcon icon={faRobot} className="mr-2" />
            要件定義書生成
          </h2>
          <div className="flex items-center space-x-4">
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value as any)}
              className="input-field w-auto"
            >
              <option value="openai">OpenAI GPT-4</option>
              <option value="google">Google Gemini</option>
              <option value="claude">Claude</option>
            </select>
            <button
              onClick={handleGenerateRequirement}
              disabled={isGenerating}
              className="btn-primary flex items-center space-x-2"
            >
              <FontAwesomeIcon icon={faRobot} />
              <span>{isGenerating ? '生成中...' : '要件定義書を生成'}</span>
            </button>
          </div>
        </div>

        {/* 要件定義書一覧 */}
        {idea.requirements.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-gray-900">要件定義書</h2>
            {idea.requirements.map((req) => (
              <div key={req.id} className="card">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm text-gray-500">
                    {req.llm_model} - {new Date(req.created_at).toLocaleString('ja-JP')}
                  </span>
                </div>
                <div className="prose max-w-none">
                  <ReactMarkdown>{req.content}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}