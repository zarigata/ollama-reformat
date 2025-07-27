import React, { useState, useEffect } from 'react'
import { Search, Download, Trash2, Play, Pause, ExternalLink } from 'lucide-react'

export function Models() {
  const [models, setModels] = useState([])
  const [popularModels, setPopularModels] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [isSearching, setIsSearching] = useState(false)
  const [activeTab, setActiveTab] = useState('installed')

  useEffect(() => {
    fetchInstalledModels()
    fetchPopularModels()
  }, [])

  const fetchInstalledModels = async () => {
    try {
      const response = await fetch('/api/models/installed')
      const data = await response.json()
      setModels(data.models)
    } catch (error) {
      console.error('Failed to fetch installed models:', error)
    }
  }

  const fetchPopularModels = async () => {
    try {
      const response = await fetch('/api/models/popular')
      const data = await response.json()
      setPopularModels(data.models)
    } catch (error) {
      console.error('Failed to fetch popular models:', error)
    }
  }

  const searchOllamaModels = async (query) => {
    if (!query.trim()) {
      setSearchResults([])
      return
    }

    setIsSearching(true)
    try {
      const response = await fetch(`/api/models/search?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      setSearchResults(data.results)
    } catch (error) {
      console.error('Failed to search models:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const handleSearchChange = (e) => {
    const query = e.target.value
    setSearchQuery(query)
    searchOllamaModels(query)
  }

  const downloadModel = async (modelName) => {
    try {
      await fetch('/api/models/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modelName })
      })
      fetchInstalledModels()
    } catch (error) {
      console.error('Failed to download model:', error)
    }
  }

  const removeModel = async (modelName) => {
    try {
      await fetch(`/api/models/${modelName}`, { method: 'DELETE' })
      fetchInstalledModels()
    } catch (error) {
      console.error('Failed to remove model:', error)
    }
  }

  const ModelCard = ({ model, type }) => (
    <div className="bg-surface-light border border-border rounded-lg p-6 hover:border-primary/50 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-text-primary">{model.name}</h3>
          <p className="text-sm text-text-secondary">{model.description}</p>
        </div>
        <div className="flex space-x-2">
          {type === 'installed' ? (
            <>
              <button className="p-2 text-green-400 hover:bg-green-400/10 rounded-lg transition-colors">
                <Play className="w-4 h-4" />
              </button>
              <button 
                onClick={() => removeModel(model.name)}
                className="p-2 text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </>
          ) : (
            <button 
              onClick={() => downloadModel(model.name)}
              className="p-2 text-blue-400 hover:bg-blue-400/10 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
      
      <div className="flex items-center justify-between text-sm">
        <span className="text-text-muted">{model.size}</span>
        <span className="text-text-muted">{model.tags?.join(', ')}</span>
      </div>
    </div>
  )

  return (
    <div className="p-8 bg-surface min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Models</h1>
          <p className="text-text-secondary">Manage your Ollama models</p>
        </div>

        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted w-5 h-5" />
            <input
              type="text"
              placeholder="Search models on Ollama..."
              value={searchQuery}
              onChange={handleSearchChange}
              className="w-full pl-10 pr-4 py-3 bg-surface-light border border-border rounded-lg text-text-primary placeholder-text-secondary focus:outline-none focus:border-primary"
            />
          </div>
        </div>

        {searchQuery && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Search Results</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.map((model) => (
                <ModelCard key={model.name} model={model} type="search" />
              ))}
            </div>
          </div>
        )}

        <div className="border-b border-border mb-6">
          <nav className="flex space-x-8">
            {['installed', 'popular'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-2 px-1 text-sm font-medium transition-colors ${
                  activeTab === tab
                    ? 'text-primary border-b-2 border-primary'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)} Models
              </button>
            ))}
          </nav>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {activeTab === 'installed' && models.map((model) => (
            <ModelCard key={model.name} model={model} type="installed" />
          ))}
          {activeTab === 'popular' && popularModels.map((model) => (
            <ModelCard key={model.name} model={model} type="popular" />
          ))}
        </div>
      </div>
    </div>
  )
}
