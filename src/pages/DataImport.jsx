import React, { useState, useCallback } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { useDropzone } from 'react-dropzone'

export function DataImport() {
  const [files, setFiles] = useState([])
  const [processingFiles, setProcessingFiles] = useState([])
  const [processedFiles, setProcessedFiles] = useState([])

  const onDrop = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substring(2, 15),
      status: 'pending',
      progress: 0
    }))
    setFiles(prev => [...prev, ...newFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    }
  })

  const processFile = async (fileData) => {
    setProcessingFiles(prev => [...prev, fileData.id])
    
    const formData = new FormData()
    formData.append('file', fileData.file)

    try {
      const response = await fetch('/api/data/process', {
        method: 'POST',
        body: formData
      })
      
      const result = await response.json()
      
      setFiles(prev => prev.map(f => 
        f.id === fileData.id 
          ? { ...f, status: 'processed', processedData: result }
          : f
      ))
      
      setProcessedFiles(prev => [...prev, { ...fileData, processedData: result }])
    } catch (error) {
      setFiles(prev => prev.map(f => 
        f.id === fileData.id 
          ? { ...f, status: 'error', error: error.message }
          : f
      ))
    } finally {
      setProcessingFiles(prev => prev.filter(id => id !== fileData.id))
    }
  }

  const removeFile = (fileId) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
    setProcessedFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const FileIcon = ({ type }) => {
    switch (type) {
      case 'application/pdf': return <FileText className="w-8 h-8 text-red-400" />
      case 'text/plain': return <FileText className="w-8 h-8 text-blue-400" />
      case 'text/markdown': return <FileText className="w-8 h-8 text-purple-400" />
      default: return <FileText className="w-8 h-8 text-gray-400" />
    }
  }

  const FileStatus = ({ status }) => {
    switch (status) {
      case 'pending':
        return <span className="text-yellow-400">Pending</span>
      case 'processing':
        return <span className="text-blue-400 flex items-center"><Loader className="w-4 h-4 mr-1 animate-spin" />Processing</span>
      case 'processed':
        return <span className="text-green-400 flex items-center"><CheckCircle className="w-4 h-4 mr-1" />Ready</span>
      case 'error':
        return <span className="text-red-400 flex items-center"><AlertCircle className="w-4 h-4 mr-1" />Error</span>
      default:
        return null
    }
  }

  return (
    <div className="p-8 bg-surface min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Data Import</h1>
          <p className="text-text-secondary">Upload and process documents for model training</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Upload Documents</h3>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragActive 
                    ? 'border-primary bg-primary/10' 
                    : 'border-border hover:border-primary/50'
                }`}
              >
                <input {...getInputProps()} />
                <Upload className="w-12 h-12 text-text-muted mx-auto mb-4" />
                <p className="text-text-primary mb-2">
                  {isDragActive ? 'Drop files here...' : 'Drag & drop files here'}
                </p>
                <p className="text-sm text-text-secondary">
                  Supports PDF, TXT, MD, DOCX files
                </p>
              </div>

              {files.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-sm font-medium text-text-primary mb-3">Uploaded Files</h4>
                  <div className="space-y-3">
                    {files.map((fileData) => (
                      <div key={fileData.id} className="flex items-center justify-between p-3 bg-surface rounded-lg">
                        <div className="flex items-center space-x-3">
                          <FileIcon type={fileData.file.type} />
                          <div>
                            <p className="text-sm font-medium text-text-primary">{fileData.file.name}</p>
                            <p className="text-xs text-text-secondary">
                              {(fileData.file.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <FileStatus status={fileData.status} />
                          {fileData.status === 'pending' && (
                            <button
                              onClick={() => processFile(fileData)}
                              className="px-3 py-1 bg-primary text-white text-sm rounded hover:bg-primary/90 transition-colors"
                            >
                              Process
                            </button>
                          )}
                          <button
                            onClick={() => removeFile(fileData.id)}
                            className="text-red-400 hover:text-red-300 transition-colors"
                          >
                            ×
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Processing Options</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Text Extraction Method
                  </label>
                  <select className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary">
                    <option>OCR + Text Extraction</option>
                    <option>Text Only</option>
                    <option>Structured Data</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Chunk Size (tokens)
                  </label>
                  <input
                    type="number"
                    defaultValue="512"
                    className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-primary mb-2">
                    Overlap (tokens)
                  </label>
                  <input
                    type="number"
                    defaultValue="50"
                    className="w-full px-3 py-2 bg-surface border border-border rounded-lg text-text-primary"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Processed Data</h3>
              
              {processedFiles.length === 0 ? (
                <p className="text-center text-text-secondary py-8">No processed data yet</p>
              ) : (
                <div className="space-y-3">
                  {processedFiles.map((file) => (
                    <div key={file.id} className="p-3 bg-surface rounded-lg">
                      <p className="text-sm font-medium text-text-primary mb-1">{file.file.name}</p>
                      <p className="text-xs text-text-secondary">
                        {file.processedData?.chunks || 0} chunks • {file.processedData?.tokens || 0} tokens
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-surface-light border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4">Data Summary</h3>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-text-secondary">Total Files</span>
                  <span className="text-text-primary font-medium">{processedFiles.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-secondary">Total Chunks</span>
                  <span className="text-text-primary font-medium">
                    {processedFiles.reduce((sum, f) => sum + (f.processedData?.chunks || 0), 0)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-secondary">Total Tokens</span>
                  <span className="text-text-primary font-medium">
                    {processedFiles.reduce((sum, f) => sum + (f.processedData?.tokens || 0), 0)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
