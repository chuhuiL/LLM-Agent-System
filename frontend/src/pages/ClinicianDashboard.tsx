import { useAuthStore } from '@/store/authStore'
import { Link } from 'react-router-dom'
import { FileText, Users, LogOut } from 'lucide-react'

export default function ClinicianDashboard() {
  const { user, logout } = useAuthStore()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Clinician Dashboard
          </h1>
          <div className="flex items-center space-x-4">
            <div className="text-sm">
              <p className="font-medium text-gray-900">
                {user?.profile?.first_name} {user?.profile?.last_name}
              </p>
              <p className="text-gray-500">{user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="btn-secondary flex items-center space-x-2 px-4 py-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link
                to="/clinician/encounter/new"
                className="btn-primary w-full py-3 flex items-center justify-center space-x-2"
              >
                <FileText className="w-5 h-5" />
                <span>New Consultation</span>
              </Link>

              <Link
                to="/clinician/patients"
                className="btn-secondary w-full py-3 flex items-center justify-center space-x-2"
              >
                <Users className="w-5 h-5" />
                <span>View Patients</span>
              </Link>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
            <div className="text-center text-gray-500 py-8">
              <p>No recent activity</p>
              <p className="text-sm mt-2">Start by creating a new consultation</p>
            </div>
          </div>

          {/* Pending Reviews */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold mb-4">Pending Reviews</h2>
            <div className="text-center text-gray-500 py-8">
              <p>No pending reviews</p>
            </div>
          </div>

          {/* Statistics */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold mb-4">Today's Statistics</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-primary-600">0</p>
                <p className="text-sm text-gray-600">Encounters</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-green-600">0</p>
                <p className="text-sm text-gray-600">Notes Signed</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
