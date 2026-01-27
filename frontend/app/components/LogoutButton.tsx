'use client'

import { useRouter } from 'next/navigation'
import { logout } from '@/lib/api'

export function LogoutButton() {
  const router = useRouter()

  const handleLogout = async () => {
    const result = await logout()

    if (result.ok) {
      router.push('/login')
      router.refresh()
    }
  }

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition"
    >
      Cerrar Sesión
    </button>
  )
}
