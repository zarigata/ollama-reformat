import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './pages/Dashboard'
import { Models } from './pages/Models'
import { FineTuning } from './pages/FineTuning'
import { DataImport } from './pages/DataImport'
import { Settings } from './pages/Settings'

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-surface">
        <Sidebar />
        <main className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/models" element={<Models />} />
            <Route path="/fine-tuning" element={<FineTuning />} />
            <Route path="/data-import" element={<DataImport />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
