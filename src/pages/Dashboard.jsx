import React, { useState, useEffect } from 'react'
import { Activity, Cpu, Download, Zap, Clock } from 'lucide-react'

export function Dashboard() {
  const [stats, setStats] = useState({
    installedModels: 0,
    runningModels: 0,
    totalDownloads: 0,
    activeJobs: 0
  })

  const [recentActivity, setRecentActivity] = useState([])

  useEffect(() => {
    // Fetch dashboard data
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/dashboard/stats')
      const data = await response.json()
      setStats(data.stats)
      setRecentActivity(data.recentActivity)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  }

  const statCards = [
    {
      title: 'Installed Models',
      value: stats.installedModels,
      icon: Cpu,
      color: 'text-blue-400',
      bgColor: 'bg-blue-400/10'
    },
    {
      title: 'Running Models',
      value: stats.runningModels,
      icon: Activity,
      color: 'text-green-400',
      bgColor: 'bg-green-400/10'
    },
    {
      title: 'Total Downloads',
      value: stats.totalDownloads,
      icon: Download,
      color: 'text-purple-400',
      bgColor: 'bg-purple-400/10'
    },
    {
      title: 'Active Jobs',
      value: stats.activeJobs,
      icon: Zap,
      color: 'text-orange-400',
      bgColor: 'bg-orange-400/10'
    }
  ]

  return (
    <div className="p-8 bg-surface min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Dashboard</h1>
          <p className="text-text-secondary">Welcome to your Ollama fine-tuning workspace</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat) => (
            <div key={stat.title} className="bg-surface-light border border-border rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-text-secondary">{stat.title}</p>
                  <p className="text-2xl font-bold text-text-primary mt-1">{stat.value}</p>
                </div>
                <div className={`${stat.bgColor} p-3 rounded-lg`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-surface-light border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Recent Activity</h3>
            <div className="space-y-4">
              {recentActivity.length === 0 ? (
                <p className="text-text-secondary text-center py-8">No recent activity</p>
              ) : (
                recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <Clock className="w-4 h-4 text-text-muted" />
                    <div>
                      <p className="text-sm text-text-primary">{activity.description}</p>
                      <p className="text-xs text-text-muted">{activity.time}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-surface-light border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full text-left px-4 py-3 bg-surface hover:bg-surface-light border border-border rounded-lg transition-colors">
                <p className="font-medium text-text-primary">Download New Model</p>
                <p className="text-sm text-text-secondary">Browse and install models from Ollama</p>
              </button>
              <button className="w-full text-left px-4 py-3 bg-surface hover:bg-surface-light border border-border rounded-lg transition-colors">
                <p className="font-medium text-text-primary">Start Fine-Tuning</p>
                <p className="text-sm text-text-secondary">Begin training with custom datasets</p>
              </button>
              <button className="w-full text-left px-4 py-3 bg-surface hover:bg-surface-light border border-border rounded-lg transition-colors">
                <p className="font-medium text-text-primary">Import Data</p>
                <p className="text-sm text-text-secondary">Upload PDFs and documents for training</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
