'use client'

import { useRouter } from 'next/navigation'
import { logout } from '@/lib/api'

interface LogoutButtonProps {
  variant?: 'default' | 'sidebar'
}

export function LogoutButton({ variant = 'default' }: LogoutButtonProps) {
  const router = useRouter()

  const handleLogout = async () => {
    const result = await logout()

    if (result.ok) {
      router.push('/login')
      router.refresh()
    }
  }

  if (variant === 'sidebar') {
    return (
      <button
        onClick={handleLogout}
        className="w-full px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition text-sm"
      >
        🚪 Cerrar Sesión
      </button>
    )
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
