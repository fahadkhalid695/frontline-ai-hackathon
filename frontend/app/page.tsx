'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  HeartPulse, 
  Shield, 
  Phone, 
  MapPin, 
  Clock, 
  CheckCircle,
  AlertTriangle,
  Loader2,
  User,
  Calendar,
  FileText
} from 'lucide-react'
import toast from 'react-hot-toast'
import EmergencyForm from './components/EmergencyForm'
import AgentProgress from './components/AgentProgress'
import ResultsPanel from './components/ResultsPanel'
import AgenticInterface from './components/AgenticInterface'

export default function Home() {
  const [currentStep, setCurrentStep] = useState<'agentic' | 'form' | 'processing' | 'results'>('agentic')
  const [emergencyData, setEmergencyData] = useState<any>(null)
  const [results, setResults] = useState<any>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleEmergencySubmit = async (data: any) => {
    setEmergencyData(data)
    setCurrentStep('processing')
    setIsProcessing(true)

    try {
      const response = await fetch('http://localhost:5000/api/emergency', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'full_workflow',
          case_data: data
        })
      })

      if (!response.ok) {
        throw new Error('Failed to process emergency request')
      }

      const result = await response.json()
      setResults(result)
      setCurrentStep('results')
      toast.success('Emergency processed successfully!')
    } catch (error) {
      console.error('Error:', error)
      toast.error('Failed to process emergency. Please try again.')
      setCurrentStep('form')
    } finally {
      setIsProcessing(false)
    }
  }

  const resetForm = () => {
    setCurrentStep('agentic')
    setEmergencyData(null)
    setResults(null)
    setIsProcessing(false)
  }

  const handleAgenticResult = (result: any) => {
    setResults(result)
    setCurrentStep('results')
  }

  const switchToManualForm = () => {
    setCurrentStep('form')
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <HeartPulse className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Frontline Worker AI</h1>
                <p className="text-sm text-gray-600">Emergency Response System</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>AI Assistant Online</span>
              </div>
              {currentStep === 'agentic' && (
                <button
                  onClick={switchToManualForm}
                  className="text-sm text-blue-600 hover:text-blue-800 underline"
                >
                  Use Manual Form
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Emergency Hotlines Banner */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-emergency-600 to-emergency-700 rounded-xl p-6 mb-8 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold mb-2">Emergency Hotlines</h2>
              <div className="flex space-x-6">
                <div className="flex items-center space-x-2">
                  <HeartPulse className="h-5 w-5" />
                  <span className="font-medium">Medical: 1122</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Shield className="h-5 w-5" />
                  <span className="font-medium">Police: 15</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Phone className="h-5 w-5" />
                  <span className="font-medium">Fire: 16</span>
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">For immediate life-threatening emergencies,</p>
              <p className="text-sm opacity-90">call directly. Use this system for guidance.</p>
            </div>
          </div>
        </motion.div>

        {/* Content based on current step */}
        {currentStep === 'agentic' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <AgenticInterface onEmergencyProcessed={handleAgenticResult} />
          </motion.div>
        )}

        {currentStep === 'form' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <EmergencyForm onSubmit={handleEmergencySubmit} />
            <div className="text-center mt-4">
              <button
                onClick={() => setCurrentStep('agentic')}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                ← Back to AI Assistant
              </button>
            </div>
          </motion.div>
        )}

        {currentStep === 'processing' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <AgentProgress 
              isProcessing={isProcessing}
              emergencyData={emergencyData}
            />
          </motion.div>
        )}

        {currentStep === 'results' && results && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <ResultsPanel 
              results={results}
              emergencyData={emergencyData}
              onReset={resetForm}
            />
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">Built with ❤️ for Pakistan's Frontline Workers</p>
            <p className="text-sm">Emergency Response AI System - Saving Lives Through Technology</p>
          </div>
        </div>
      </footer>
    </div>
  )
}