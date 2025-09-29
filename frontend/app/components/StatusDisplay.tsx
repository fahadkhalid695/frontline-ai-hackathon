'use client'

import { motion } from 'framer-motion'
import { CheckCircle, Clock, AlertTriangle, Wifi, WifiOff } from 'lucide-react'

interface StatusDisplayProps {
  systemMode: 'enhanced' | 'degraded'
  isOnline: boolean
}

export default function StatusDisplay({ systemMode, isOnline }: StatusDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-sm font-medium text-gray-700">
            System Status: {isOnline ? 'Online' : 'Offline'}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          {isOnline ? (
            <Wifi className="h-4 w-4 text-green-600" />
          ) : (
            <WifiOff className="h-4 w-4 text-red-600" />
          )}
          <span className={`text-xs px-2 py-1 rounded-full ${
            systemMode === 'enhanced' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {systemMode === 'enhanced' ? 'AI Enhanced' : 'Basic Mode'}
          </span>
        </div>
      </div>
      
      {systemMode === 'degraded' && (
        <div className="mt-2 text-xs text-yellow-700 bg-yellow-50 p-2 rounded">
          <AlertTriangle className="h-3 w-3 inline mr-1" />
          Running in basic mode. Some advanced features may be limited.
        </div>
      )}
    </motion.div>
  )
}