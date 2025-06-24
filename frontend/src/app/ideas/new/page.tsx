'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSave, faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import Layout from '@/components/Layout'
import axios from '@/lib/axios'
import toast from 'react-hot-toast'

interface IdeaForm {
  title: string
  content: string
}

export default function NewIdeaPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<IdeaForm>()

  const onSubmit = async (data: IdeaForm) => {
    setIsLoading(true)
    try {
      await axios.post('/ideas', data)
      toast.success('アイデアを作成しました')
      router.push('/ideas')
    } catch (error) {
      console.error('Failed to create idea:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="text-gray-600 hover:text-gray-800 flex items-center space-x-2"
          >
            <FontAwesomeIcon icon={faArrowLeft} />
            <span>戻る</span>
          </button>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">新しいアイデア</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                タイトル
              </label>
              <input
                type="text"
                {...register('title', { required: 'タイトルを入力してください' })}
                className="input-field"
                placeholder="アイデアのタイトル"
              />
              {errors.title && (
                <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                内容
              </label>
              <textarea
                {...register('content', { required: '内容を入力してください' })}
                className="input-field"
                rows={10}
                placeholder="アイデアの詳細を記入してください..."
              />
              {errors.content && (
                <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
              )}
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => router.back()}
                className="btn-outline"
              >
                キャンセル
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary flex items-center space-x-2"
              >
                <FontAwesomeIcon icon={faSave} />
                <span>{isLoading ? '保存中...' : '保存'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  )
}