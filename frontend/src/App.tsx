import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ClinicianDashboard from './pages/ClinicianDashboard'
import AdminDashboard from './pages/AdminDashboard'
import PatientPortal from './pages/PatientPortal'

function App() {
  const { user, isAuthenticated } = useAuthStore()

  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes */}
        <Route
          path="/clinician/*"
          element={
            isAuthenticated && user?.role === 'clinician' ? (
              <ClinicianDashboard />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        <Route
          path="/admin/*"
          element={
            isAuthenticated && user?.role === 'admin' ? (
              <AdminDashboard />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        <Route
          path="/patient/*"
          element={
            isAuthenticated && user?.role === 'patient' ? (
              <PatientPortal />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* Default redirect */}
        <Route
          path="/"
          element={
            isAuthenticated ? (
              user?.role === 'clinician' ? (
                <Navigate to="/clinician" />
              ) : user?.role === 'admin' ? (
                <Navigate to="/admin" />
              ) : (
                <Navigate to="/patient" />
              )
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
