'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Mic, 
  MicOff, 
  Send, 
  Phone, 
  MessageSquare,
  Bot,
  User,
  AlertTriangle,
  CheckCircle,
  Clock,
  PhoneCall,
  MapPin,
  Calendar
} from 'lucide-react'
import toast from 'react-hot-toast'

interface AgenticInterfaceProps {
  onEmergencyProcessed: (result: any) => void
}

interface Message {
  id: string
  type: 'user' | 'agent' | 'system' | 'action'
  content: string
  timestamp: Date
  metadata?: any
}

export default function AgenticInterface({ onEmergencyProcessed }: AgenticInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'agent',
      content: "Hello! I'm your AI Emergency Assistant. Just tell me what's happening and I'll take care of everything. You can type or use voice.",
      timestamp: new Date(),
    }
  ])
  
  const [inputText, setInputText] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStep, setCurrentStep] = useState<string>('')
  const [userLocation, setUserLocation] = useState<{lat: number, lng: number, address?: string} | null>(null)
  
  const recognitionRef = useRef<any>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initialize speech recognition
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = 'en-US'
      
      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript
        setInputText(transcript)
        setIsListening(false)
      }
      
      recognitionRef.current.onerror = () => {
        setIsListening(false)
        toast.error('Voice recognition failed. Please try typing instead.')
      }
      
      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    // Get user's location on component mount
    getCurrentLocation()
  }, [])

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords
          setUserLocation({ lat: latitude, lng: longitude })
          
          // Try to get address from coordinates
          try {
            const address = await reverseGeocode(latitude, longitude)
            setUserLocation(prev => ({ ...prev!, address }))
            
            addMessage({
              type: 'system',
              content: `📍 Location detected: ${address}. This will be shared with emergency services if needed.`
            })
          } catch (error) {
            addMessage({
              type: 'system',
              content: `📍 Location detected (${latitude.toFixed(4)}, ${longitude.toFixed(4)}). This will be shared with emergency services if needed.`
            })
          }
        },
        (error) => {
          console.warn('Location access denied:', error)
          addMessage({
            type: 'system',
            content: "📍 Location access not available. You may need to provide your location manually if needed."
          })
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
      )
    }
  }

  const reverseGeocode = async (lat: number, lng: number): Promise<string> => {
    // Using a free geocoding service (you might want to use Google Maps API in production)
    try {
      const response = await fetch(
        `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lng}&localityLanguage=en`
      )
      const data = await response.json()
      
      if (data.locality && data.countryName) {
        return `${data.locality}, ${data.principalSubdivision}, ${data.countryName}`
      } else {
        return `${lat.toFixed(4)}, ${lng.toFixed(4)}`
      }
    } catch (error) {
      return `${lat.toFixed(4)}, ${lng.toFixed(4)}`
    }
  }

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
    return newMessage
  }

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true)
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  const processEmergencyInput = async (userInput: string) => {
    // Add user message
    addMessage({
      type: 'user',
      content: userInput
    })

    setIsProcessing(true)
    
    try {
      // Step 1: AI analyzes the input
      addMessage({
        type: 'agent',
        content: "I'm analyzing your situation..."
      })
      
      setCurrentStep('Analyzing emergency situation...')
      
      // Call the intelligent parsing endpoint with location data
      const parseResponse = await fetch('http://localhost:5000/api/parse-emergency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_input: userInput,
          location_data: userLocation 
        })
      })
      
      if (!parseResponse.ok) throw new Error('Failed to parse emergency')
      
      const parsedData = await parseResponse.json()
      
      // Show what the AI understood
      addMessage({
        type: 'agent',
        content: `I understand you have a ${parsedData.emergency_type} emergency: "${parsedData.summary}". Let me assess the priority and find the right help.`
      })
      
      // Step 2: Process through agents
      setCurrentStep('Processing through emergency agents...')
      
      const agentResponse = await fetch('http://localhost:5000/api/emergency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'full_workflow',
          case_data: parsedData.case_data
        })
      })
      
      if (!agentResponse.ok) throw new Error('Failed to process emergency')
      
      const result = await agentResponse.json()
      
      // Step 3: Show results and take actions
      await showAgentResults(result)
      
      onEmergencyProcessed(result)
      
    } catch (error) {
      console.error('Error:', error)
      addMessage({
        type: 'agent',
        content: "I'm sorry, I encountered an error processing your emergency. Let me connect you directly to emergency services."
      })
      
      // Fallback action
      addMessage({
        type: 'action',
        content: "🚨 Connecting to Emergency Hotline: 1122",
        metadata: { action: 'call', number: '1122' }
      })
      
      toast.error('Processing failed. Emergency services contacted.')
    } finally {
      setIsProcessing(false)
      setCurrentStep('')
    }
  }

  const showAgentResults = async (result: any) => {
    const agentResult = result.result
    
    // Show priority assessment
    const priorityEmoji = agentResult.priority === 'high' ? '🚨' : 
                         agentResult.priority === 'medium' ? '⚠️' : 'ℹ️'
    
    addMessage({
      type: 'agent',
      content: `${priorityEmoji} Priority Assessment: ${agentResult.priority?.toUpperCase()} priority case. Urgency: ${agentResult.urgency?.replace('_', ' ')}`
    })
    
    await delay(1000)
    
    // Show service matching
    if (agentResult.recommended_service) {
      const serviceName = typeof agentResult.recommended_service === 'string' 
        ? agentResult.recommended_service 
        : agentResult.recommended_service.name
      
      addMessage({
        type: 'agent',
        content: `🏥 I've found the right service for you: ${serviceName}`
      })
      
      await delay(1000)
    }
    
    // Show booking confirmation
    if (agentResult.appointment_details) {
      const appointment = agentResult.appointment_details
      const appointmentTime = new Date(appointment.appointment_time).toLocaleString()
      
      addMessage({
        type: 'agent',
        content: `📅 Great! I've booked your ${appointment.slot_type.toLowerCase()} appointment for ${appointmentTime}. Confirmation: ${agentResult.confirmation_details?.confirmation_number}`
      })
      
      await delay(1000)
      
      // Show instructions
      if (appointment.instructions) {
        addMessage({
          type: 'agent',
          content: `📋 Instructions: ${appointment.instructions}`
        })
      }
    }
    
    // Show follow-up setup
    if (agentResult.reminder_schedule) {
      addMessage({
        type: 'agent',
        content: `🔔 I've set up ${agentResult.reminder_schedule.length} reminders to keep you updated. You'll receive notifications via SMS.`
      })
    }
    
    // Autonomous actions based on priority
    if (agentResult.priority === 'high') {
      await delay(1000)
      addMessage({
        type: 'action',
        content: "🚨 HIGH PRIORITY: Initiating emergency call now...",
        metadata: { 
          action: 'emergency_call', 
          number: agentResult.contact_information || '1122',
          service: agentResult.recommended_service
        }
      })
      
      // Simulate emergency call
      setTimeout(() => {
        addMessage({
          type: 'system',
          content: "📞 Emergency services have been notified. Help is on the way. Stay on the line."
        })
      }, 2000)
      
    } else if (agentResult.priority === 'medium') {
      await delay(1000)
      addMessage({
        type: 'action',
        content: "📱 Sending appointment details to your phone and preparing quick-dial options...",
        metadata: { 
          action: 'send_sms', 
          appointment: agentResult.appointment_details 
        }
      })
    }
    
    // Final summary
    await delay(2000)
    addMessage({
      type: 'agent',
      content: "✅ All done! I've handled everything for you. Is there anything else you need help with?"
    })
  }

  const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputText.trim() && !isProcessing) {
      processEmergencyInput(inputText.trim())
      setInputText('')
    }
  }

  const handleActionClick = (metadata: any) => {
    if (metadata.action === 'call' || metadata.action === 'emergency_call') {
      // Real phone call implementation
      const phoneNumber = metadata.number
      
      // Show confirmation dialog for emergency calls
      if (metadata.action === 'emergency_call') {
        const confirmed = window.confirm(
          `This will call emergency services (${phoneNumber}). Are you sure you want to proceed?`
        )
        if (!confirmed) return
      }
      
      try {
        // Attempt to make the call
        window.open(`tel:${phoneNumber}`)
        toast.success(`Calling ${phoneNumber}...`)
        
        // Log the call attempt
        addMessage({
          type: 'system',
          content: `📞 Call initiated to ${phoneNumber}. If the call doesn't start automatically, please dial ${phoneNumber} manually.`
        })
        
        // For emergency calls, also show additional guidance
        if (metadata.action === 'emergency_call') {
          setTimeout(() => {
            addMessage({
              type: 'agent',
              content: "While waiting for emergency services, stay calm and follow any instructions they give you. Keep your phone nearby for updates."
            })
          }, 2000)
        }
        
      } catch (error) {
        toast.error(`Unable to make call automatically. Please dial ${phoneNumber} manually.`)
        addMessage({
          type: 'system',
          content: `⚠️ Automatic calling failed. Please manually dial: ${phoneNumber}`
        })
      }
      
    } else if (metadata.action === 'send_sms') {
      toast.success('SMS sent with appointment details!')
    }
  }

  return (
    <div className="max-w-4xl mx-auto h-[80vh] flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-2xl">
        <div className="flex items-center space-x-3">
          <Bot className="h-8 w-8" />
          <div>
            <h2 className="text-2xl font-bold">AI Emergency Assistant</h2>
            <p className="text-blue-100">Just tell me what's happening - I'll handle the rest</p>
          </div>
        </div>
        
        {isProcessing && (
          <div className="mt-4 bg-blue-800 bg-opacity-50 rounded-lg p-3">
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              <span className="text-sm">{currentStep}</span>
            </div>
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 bg-white p-6 overflow-y-auto space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] rounded-2xl p-4 ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : message.type === 'action'
                  ? 'bg-red-50 border-2 border-red-200 text-red-800'
                  : message.type === 'system'
                  ? 'bg-green-50 border-2 border-green-200 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                <div className="flex items-start space-x-2">
                  {message.type === 'user' ? (
                    <User className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  ) : message.type === 'action' ? (
                    <AlertTriangle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  ) : message.type === 'system' ? (
                    <CheckCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  ) : (
                    <Bot className="h-5 w-5 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm">{message.content}</p>
                    {message.metadata && (
                      <button
                        onClick={() => handleActionClick(message.metadata)}
                        className="mt-2 inline-flex items-center px-3 py-1 bg-white bg-opacity-20 rounded-full text-xs hover:bg-opacity-30 transition-colors"
                      >
                        {message.metadata.action === 'call' || message.metadata.action === 'emergency_call' ? (
                          <>
                            <PhoneCall className="h-3 w-3 mr-1" />
                            Call Now
                          </>
                        ) : (
                          <>
                            <MessageSquare className="h-3 w-3 mr-1" />
                            View Details
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>
                <div className="text-xs opacity-70 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-gray-50 p-6 rounded-b-2xl">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Describe your emergency situation... (e.g., 'I have severe chest pain' or 'There's a fire in my building')"
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isProcessing}
            />
            {isListening && (
              <div className="absolute right-3 top-3">
                <div className="w-6 h-6 bg-red-500 rounded-full animate-pulse flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                </div>
              </div>
            )}
          </div>
          
          <button
            type="button"
            onClick={isListening ? stopListening : startListening}
            className={`px-4 py-3 rounded-xl transition-colors ${
              isListening 
                ? 'bg-red-600 hover:bg-red-700 text-white' 
                : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
            }`}
            disabled={isProcessing}
          >
            {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
          </button>
          
          <button
            type="submit"
            disabled={!inputText.trim() || isProcessing}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-xl transition-colors flex items-center space-x-2"
          >
            <Send className="h-5 w-5" />
            <span>Send</span>
          </button>
        </form>
        
        <div className="mt-3 text-xs text-gray-500 text-center">
          💡 Try: "I'm having chest pain", "My house is on fire", "Someone broke into my store", "I fell and can't get up"
        </div>
      </div>
    </div>
  )
}