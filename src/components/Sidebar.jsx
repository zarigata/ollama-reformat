import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  Home, 
  Cpu, 
  Settings2, 
  Upload, 
  Settings,
  Brain,
  GitBranch
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Models', href: '/models', icon: Cpu },
  { name: 'Fine-Tuning', href: '/fine-tuning', icon: Settings2 },
  { name: 'Data Import', href: '/data-import', icon: Upload },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <div className="flex flex-col w-64 bg-surface-light border-r border-border">
      <div className="flex items-center h-16 px-6 border-b border-border">
        <Brain className="w-8 h-8 text-primary" />
        <span className="ml-3 text-xl font-bold text-text-primary">Ollama Studio</span>
      </div>
      
      <nav className="flex-1 px-4 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors duration-200 ${
                isActive
                  ? 'bg-primary/20 text-primary border border-primary/30'
                  : 'text-text-secondary hover:bg-surface hover:text-text-primary'
              }`}
            >
              <item.icon className="w-5 h-5 mr-3" />
              {item.name}
            </Link>
          )
        })}
      </nav>
      
      <div className="px-4 py-4 border-t border-border">
        <div className="flex items-center">
          <GitBranch className="w-4 h-4 text-text-muted mr-2" />
          <span className="text-xs text-text-muted">madebyzarigata</span>
        </div>
      </div>
    </div>
  )
}
