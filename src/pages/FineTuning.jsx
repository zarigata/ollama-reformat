import React, { useState } from 'react'
import { Play, Pause, Square, Download, Upload, Settings, AlertCircle } from 'lucide-react'

export function FineTuning() {
  const [selectedModel, setSelectedModel] = useState('')
  const [fineTuningType, setFineTuningType] = useState('general')
  const [jailbreakPrompt, setJailbreakPrompt] = useState('')
  const [trainingData, setTrainingData] = useState([])
  const [isTraining, setIsTraining] = useState(false)
  const [progress, setProgress] = useState(0)

  const models = ['llama2', 'mistral', 'codellama', 'vicuna']
  const fineTuningTypes = [
    { id: 'general', name: 'General Fine-tuning', description: 'Improve model performance with custom data' },
    { id: 'jailbreak', name: 'Jailbreak Prompt', description: 'Add latest jailbreak techniques' },
    { id: 'data-import', name: 'Data Import Training', description: 'Train with imported PDFs and documents' }
  ]

  const handleStartTraining = async () => {
    setIsTraining(true)
    setProgress(0)
    
    // Simulate training progress
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsTraining(false)
          return 100
        }
        return prev + 5
      })
    }, 500)
  }

  const handleStopTraining = () => {
    setIsTraining(false)
    setProgress(0)
  }

  const searchJailbreakPrompts = async () => {
    try {
      const response = await fetch('/api/jailbreak/search')
      const data = await response.json()
      setJailbreakPrompt(data.latestPrompt)
    } catch (error) {
      console.error('Failed to fetch jailbreak prompts:', error)
    }
  }

  return (
    <div className="p-8 bg-surface min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Fine-Tuning</h1>
          <p className="text-text-secondary">Fine-tune your models with custom data and techniques</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Configuration</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Select Model
                  </label>
                  <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary focus:outline-none focus:border-primary"
                  >
                    <option value="">Choose a model</option>
                    {models.map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Fine-tuning Type
                  </label>
                  <div className="space-y-2">
                    {fineTuningTypes.map(type => (
                      <label key={type.id} className="flex items-center">
                        <input
                          type="radio"
                          name="fineTuningType"
                          value={type.id}
                          checked={fineTuningType === type.id}
                          onChange={(e) => setFineTuningType(e.target.value)}
                          className="mr-3"
                        />
                        <div>
                          <p className="text-sm font-medium text-text-primary">{type.name}</p>
                          <p className="text-xs text-text-secondary">{type.description}</p>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {fineTuningType === 'jailbreak' && (
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">
                      Jailbreak Prompt
                    </label>
                    <div className="space-y-2">
                      <textarea
                        value={jailbreakPrompt}
                        onChange={(e) => setJailbreakPrompt(e.target.value)}
                        placeholder="Enter jailbreak prompt..."
                        className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary focus:outline-none focus:border-primary h-24 resize-none"
                      />
                      <button
                        onClick={searchJailbreakPrompts}
                        className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                      >
                        Search Latest Prompts
                      </button>
                    </div>
                  </div>
                )}

                {fineTuningType === 'data-import' && (
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-2">
                      Training Data
                    </label>
                    <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                      <Upload className="w-12 h-12 text-text-muted mx-auto mb-3" />
                      <p className="text-text-secondary mb-2">Drop your training files here</p>
                      <button className="px-4 py-2 bg-surface border border-border rounded-lg text-text-primary hover:bg-surface-light transition-colors">
                        Browse Files
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-surface-light border border-border rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-text-primary">Training Progress</h3>
                <div className="flex space-x-2">
                  {!isTraining ? (
                    <button
                      onClick={handleStartTraining}
                      disabled={!selectedModel}
                      className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Start Training
                    </button>
                  ) : (
                    <>
                      <button
                        onClick={handleStopTraining}
                        className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                      >
                        <Square className="w-4 h-4 mr-2" />
                        Stop
                      </button>
                      <button className="flex items-center px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                        <Pause className="w-4 h-4 mr-2" />
                        Pause
                      </button>
                    </>
                  )}
                </div>
              </div>

              {isTraining && (
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-text-secondary">Progress</span>
                    <span className="text-text-primary">{progress}%</span>
                  </div>
                  <div className="w-full bg-surface rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>
              )}

              {!isTraining && progress === 0 && (
                <p className="text-center text-text-secondary py-8">
                  Configure your training parameters and start fine-tuning
                </p>
              )}

              {progress === 100 && (
                <div className="text-center">
                  <p className="text-green-400 mb-4">Training completed successfully!</p>
                  <button className="flex items-center mx-auto px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
                    <Download className="w-4 h-4 mr-2" />
                    Download Model
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Training Logs</h3>
              <div className="bg-surface rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
                <div className="text-green-400">[INFO] Training session started...</div>
                <div className="text-blue-400">[DEBUG] Loading model: {selectedModel || 'none selected'}</div>
                <div className="text-yellow-400">[WARN] Ensure sufficient GPU memory</div>
              </div>
            </div>

            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Quick Settings</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm text-text-secondary mb-1">Learning Rate</label>
                  <input type="number" defaultValue="0.001" step="0.0001" className="w-full px-3 py-1 bg-surface border border-border rounded text-sm" />
                </div>
                <div>
                  <label className="block text-sm text-text-secondary mb-1">Batch Size</label>
                  <input type="number" defaultValue="32" className="w-full px-3 py-1 bg-surface border border-border rounded text-sm" />
                </div>
                <div>
                  <label className="block text-sm text-text-secondary mb-1">Epochs</label>
                  <input type="number" defaultValue="3" className="w-full px-3 py-1 bg-surface border border-border rounded text-sm" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
