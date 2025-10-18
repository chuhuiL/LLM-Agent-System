import { useAuthStore } from '@/store/authStore'
import { LogOut } from 'lucide-react'

export default function PatientPortal() {
  const { user, logout } = useAuthStore()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Patient Portal</h1>
          <button
            onClick={logout}
            className="btn-secondary flex items-center space-x-2 px-4 py-2"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4">Welcome, {user?.profile?.first_name}!</h2>
          <p className="text-gray-600">
            View your clinical notes and encounter history here.
          </p>
        </div>
      </main>
    </div>
  )
}
