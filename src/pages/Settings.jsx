import React, { useState } from 'react'
import { Settings, Save, RefreshCw, Github } from 'lucide-react'

export function Settings() {
  const [settings, setSettings] = useState({
    ollamaUrl: 'http://localhost:11434',
    maxModelSize: '7B',
    autoDownload: false,
    darkMode: true,
    notifications: true,
    githubIntegration: false,
    githubToken: ''
  })

  const handleSave = async () => {
    try {
      await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      })
      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save settings:', error)
    }
  }

  const handleReset = () => {
    setSettings({
      ollamaUrl: 'http://localhost:11434',
      maxModelSize: '7B',
      autoDownload: false,
      darkMode: true,
      notifications: true,
      githubIntegration: false,
      githubToken: ''
    })
  }

  return (
    <div className="p-8 bg-surface min-h-screen">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Settings</h1>
          <p className="text-text-secondary">Configure your Ollama Studio preferences</p>
        </div>

        <div className="bg-surface-light border border-border rounded-lg p-6 space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-text-primary mb-4">Ollama Configuration</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Ollama Server URL
                </label>
                <input
                  type="url"
                  value={settings.ollamaUrl}
                  onChange={(e) => setSettings({ ...settings, ollamaUrl: e.target.value })}
                  className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary focus:outline-none focus:border-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Maximum Model Size
                </label>
                <select
                  value={settings.maxModelSize}
                  onChange={(e) => setSettings({ ...settings, maxModelSize: e.target.value })}
                  className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary focus:outline-none focus:border-primary"
                >
                  <option value="3B">3B parameters</option>
                  <option value="7B">7B parameters</option>
                  <option value="13B">13B parameters</option>
                  <option value="30B">30B parameters</option>
                  <option value="70B">70B parameters</option>
                </select>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="autoDownload"
                  checked={settings.autoDownload}
                  onChange={(e) => setSettings({ ...settings, autoDownload: e.target.checked })}
                  className="mr-3"
                />
                <label htmlFor="autoDownload" className="text-sm text-text-primary">
                  Auto-download popular models
                </label>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">GitHub Integration</h3>
            
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="githubIntegration"
                  checked={settings.githubIntegration}
                  onChange={(e) => setSettings({ ...settings, githubIntegration: e.target.checked })}
                  className="mr-3"
                />
                <label htmlFor="githubIntegration" className="text-sm text-text-primary">
                  Enable GitHub integration
                </label>
              </div>

              {settings.githubIntegration && (
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    GitHub Personal Access Token
                  </label>
                  <input
                    type="password"
                    value={settings.githubToken}
                    onChange={(e) => setSettings({ ...settings, githubToken: e.target.value })}
                    placeholder="ghp_..."
                    className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary focus:outline-none focus:border-primary"
                  />
                  <p className="text-xs text-text-secondary mt-1">
                    Required for model sharing and backup
                  </p>
                </div>
              )}

              <div className="flex items-center space-x-2 text-sm text-text-secondary">
                <Github className="w-4 h-4" />
                <span>Connected as: zarigata</span>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Appearance</h3>
            
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="darkMode"
                  checked={settings.darkMode}
                  onChange={(e) => setSettings({ ...settings, darkMode: e.target.checked })}
                  className="mr-3"
                />
                <label htmlFor="darkMode" className="text-sm text-text-primary">
                  Dark mode
                </label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="notifications"
                  checked={settings.notifications}
                  onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
                  className="mr-3"
                />
                <label htmlFor="notifications" className="text-sm text-text-primary">
                  Enable notifications
                </label>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-6 flex justify-end space-x-4">
            <button
              onClick={handleReset}
              className="flex items-center px-4 py-2 bg-surface border border-border rounded-lg text-text-primary hover:bg-surface-light transition-colors"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Reset
            </button>
            <button
              onClick={handleSave}
              className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Save className="w-4 h-4 mr-2" />
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
