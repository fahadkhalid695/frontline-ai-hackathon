'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, 
  Route, 
  Calendar, 
  Phone, 
  CheckCircle, 
  Loader2,
  Clock,
  AlertTriangle
} from 'lucide-react'

interface AgentProgressProps {
  isProcessing: boolean
  emergencyData: any
}

const agents = [
  {
    id: 'triage',
    name: 'Triage Agent',
    description: 'Analyzing symptoms and assigning priority',
    icon: Brain,
    color: 'text-red-600',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200'
  },
  {
    id: 'guidance',
    name: 'Guidance Agent',
    description: 'Finding appropriate services and routing',
    icon: Route,
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200'
  },
  {
    id: 'booking',
    name: 'Booking Agent',
    description: 'Scheduling appointments and preparing forms',
    icon: Calendar,
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200'
  },
  {
    id: 'followup',
    name: 'Follow-up Agent',
    description: 'Setting up reminders and tracking',
    icon: Phone,
    color: 'text-purple-600',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200'
  }
]

export default function AgentProgress({ isProcessing, emergencyData }: AgentProgressProps) {
  const [currentAgent, setCurrentAgent] = useState(0)
  const [completedAgents, setCompletedAgents] = useState<string[]>([])

  useEffect(() => {
    if (!isProcessing) return

    const interval = setInterval(() => {
      setCurrentAgent(prev => {
        if (prev < agents.length - 1) {
          // Mark current agent as completed
          setCompletedAgents(completed => [...completed, agents[prev].id])
          return prev + 1
        } else {
          // Mark final agent as completed
          setCompletedAgents(completed => [...completed, agents[prev].id])
          clearInterval(interval)
          return prev
        }
      })
    }, 2000) // Each agent takes 2 seconds

    return () => clearInterval(interval)
  }, [isProcessing])

  const getAgentStatus = (index: number) => {
    if (completedAgents.includes(agents[index].id)) {
      return 'completed'
    } else if (index === currentAgent && isProcessing) {
      return 'processing'
    } else if (index < currentAgent) {
      return 'completed'
    } else {
      return 'pending'
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Processing Emergency Request</h2>
          <p className="text-gray-600">Our AI agents are working together to help you</p>
        </div>

        {/* Emergency Summary */}
        <div className="bg-gray-50 rounded-xl p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Request Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Type:</span>
              <span className="ml-2 capitalize">{emergencyData?.emergency_type}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Location:</span>
              <span className="ml-2">{emergencyData?.location}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Patient:</span>
              <span className="ml-2">{emergencyData?.citizen_data?.name}</span>
            </div>
          </div>
        </div>

        {/* Agent Progress */}
        <div className="space-y-4">
          {agents.map((agent, index) => {
            const Icon = agent.icon
            const status = getAgentStatus(index)
            
            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`relative p-6 rounded-xl border-2 transition-all ${
                  status === 'completed' 
                    ? `${agent.bgColor} ${agent.borderColor} border-opacity-50`
                    : status === 'processing'
                    ? `${agent.bgColor} ${agent.borderColor}`
                    : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center space-x-4">
                  {/* Agent Icon */}
                  <div className={`relative p-3 rounded-full ${
                    status === 'completed' ? 'bg-green-100' : 
                    status === 'processing' ? agent.bgColor : 'bg-gray-100'
                  }`}>
                    {status === 'completed' ? (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    ) : status === 'processing' ? (
                      <Loader2 className={`h-6 w-6 ${agent.color} animate-spin`} />
                    ) : (
                      <Icon className={`h-6 w-6 ${status === 'pending' ? 'text-gray-400' : agent.color}`} />
                    )}
                  </div>

                  {/* Agent Info */}
                  <div className="flex-1">
                    <h4 className={`text-lg font-semibold ${
                      status === 'pending' ? 'text-gray-400' : 'text-gray-900'
                    }`}>
                      {agent.name}
                    </h4>
                    <p className={`text-sm ${
                      status === 'pending' ? 'text-gray-400' : 'text-gray-600'
                    }`}>
                      {agent.description}
                    </p>
                  </div>

                  {/* Status Indicator */}
                  <div className="text-right">
                    {status === 'completed' && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="text-green-600 font-medium text-sm"
                      >
                        ✓ Completed
                      </motion.div>
                    )}
                    {status === 'processing' && (
                      <motion.div
                        animate={{ opacity: [1, 0.5, 1] }}
                        transition={{ repeat: Infinity, duration: 1.5 }}
                        className={`${agent.color} font-medium text-sm`}
                      >
                        Processing...
                      </motion.div>
                    )}
                    {status === 'pending' && (
                      <div className="text-gray-400 font-medium text-sm">
                        Waiting...
                      </div>
                    )}
                  </div>
                </div>

                {/* Processing Animation */}
                {status === 'processing' && (
                  <motion.div
                    className="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 2, ease: 'easeInOut' }}
                  />
                )}
              </motion.div>
            )
          })}
        </div>

        {/* Progress Bar */}
        <div className="mt-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Progress</span>
            <span>{Math.round(((completedAgents.length + (isProcessing ? 1 : 0)) / agents.length) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ 
                width: `${((completedAgents.length + (isProcessing && currentAgent < agents.length ? 1 : 0)) / agents.length) * 100}%` 
              }}
              transition={{ duration: 0.5, ease: 'easeInOut' }}
            />
          </div>
        </div>

        {/* Estimated Time */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center space-x-2 text-sm text-gray-600 bg-gray-50 px-4 py-2 rounded-full">
            <Clock className="h-4 w-4" />
            <span>
              {isProcessing 
                ? `Estimated time remaining: ${Math.max(0, (agents.length - currentAgent) * 2)} seconds`
                : 'Processing complete!'
              }
            </span>
          </div>
        </div>
      </motion.div>
    </div>
  )
}