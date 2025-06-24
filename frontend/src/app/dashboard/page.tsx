'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Draggable from 'react-draggable'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faTimes, faEdit, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons'
import Layout from '@/components/Layout'
import { useAuthStore } from '@/stores/authStore'
import axios from '@/lib/axios'
import toast from 'react-hot-toast'

interface HomeItem {
  id: number
  title: string
  content?: string
  link?: string
  position_x: number
  position_y: number
  width: number
  height: number
  color: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [items, setItems] = useState<HomeItem[]>([])
  const [isAddingItem, setIsAddingItem] = useState(false)
  const [editingItem, setEditingItem] = useState<number | null>(null)
  const [newItem, setNewItem] = useState({
    title: '',
    content: '',
    link: '',
    color: '#FFE4B5'
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchItems()
  }, [isAuthenticated, router])

  const fetchItems = async () => {
    try {
      const response = await axios.get('/home/items')
      setItems(response.data)
    } catch (error) {
      console.error('Failed to fetch items:', error)
    }
  }

  const handleAddItem = async () => {
    if (!newItem.title) {
      toast.error('タイトルを入力してください')
      return
    }

    try {
      const response = await axios.post('/home/items', {
        ...newItem,
        position_x: Math.random() * 500,
        position_y: Math.random() * 300,
      })
      setItems([...items, response.data])
      setIsAddingItem(false)
      setNewItem({ title: '', content: '', link: '', color: '#FFE4B5' })
      toast.success('付箋を追加しました')
    } catch (error) {
      console.error('Failed to add item:', error)
    }
  }

  const handleUpdatePosition = async (id: number, x: number, y: number) => {
    try {
      await axios.put(`/home/items/${id}`, {
        position_x: x,
        position_y: y,
      })
    } catch (error) {
      console.error('Failed to update position:', error)
    }
  }

  const handleDeleteItem = async (id: number) => {
    try {
      await axios.delete(`/home/items/${id}`)
      setItems(items.filter(item => item.id !== id))
      toast.success('付箋を削除しました')
    } catch (error) {
      console.error('Failed to delete item:', error)
    }
  }

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">ダッシュボード</h2>
        <button
          onClick={() => setIsAddingItem(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <FontAwesomeIcon icon={faPlus} />
          <span>付箋を追加</span>
        </button>
      </div>

      <div className="relative bg-white rounded-xl shadow-lg" style={{ height: '600px' }}>
        {items.map((item) => (
          <Draggable
            key={item.id}
            defaultPosition={{ x: item.position_x, y: item.position_y }}
            onStop={(e, data) => handleUpdatePosition(item.id, data.x, data.y)}
            bounds="parent"
            handle=".handle"
          >
            <div
              className="sticky-note handle"
              style={{
                width: `${item.width}px`,
                height: `${item.height}px`,
                background: item.color,
              }}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-gray-800">{item.title}</h3>
                <div className="flex space-x-1">
                  {item.link && (
                    <a
                      href={item.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-600 hover:text-gray-800"
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} className="text-sm" />
                    </a>
                  )}
                  <button
                    onClick={() => handleDeleteItem(item.id)}
                    className="text-gray-600 hover:text-red-600"
                  >
                    <FontAwesomeIcon icon={faTimes} className="text-sm" />
                  </button>
                </div>
              </div>
              {item.content && (
                <p className="text-sm text-gray-700">{item.content}</p>
              )}
            </div>
          </Draggable>
        ))}
      </div>

      {/* 付箋追加モーダル */}
      {isAddingItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-bold mb-4">新しい付箋を追加</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  タイトル
                </label>
                <input
                  type="text"
                  value={newItem.title}
                  onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  内容
                </label>
                <textarea
                  value={newItem.content}
                  onChange={(e) => setNewItem({ ...newItem, content: e.target.value })}
                  className="input-field"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  リンク
                </label>
                <input
                  type="url"
                  value={newItem.link}
                  onChange={(e) => setNewItem({ ...newItem, link: e.target.value })}
                  className="input-field"
                  placeholder="https://..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  色
                </label>
                <input
                  type="color"
                  value={newItem.color}
                  onChange={(e) => setNewItem({ ...newItem, color: e.target.value })}
                  className="w-full h-10 rounded cursor-pointer"
                />
              </div>
            </div>
            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setIsAddingItem(false)}
                className="btn-outline"
              >
                キャンセル
              </button>
              <button
                onClick={handleAddItem}
                className="btn-primary"
              >
                追加
              </button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}