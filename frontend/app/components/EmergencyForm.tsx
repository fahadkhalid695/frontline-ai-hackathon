'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  User, 
  Phone, 
  MapPin,
  AlertTriangle,
  Heart,
  Shield,
  Flame,
  Calendar,
  FileText,
  Send
} from 'lucide-react'

interface EmergencyFormProps {
  onSubmit: (data: any) => void
}

export default function EmergencyForm({ onSubmit }: EmergencyFormProps) {
  const [formData, setFormData] = useState({
    // Emergency Details
    symptoms: '',
    emergency_type: 'medical',
    location: '',
    
    // Citizen Data
    citizen_data: {
      name: '',
      age: '',
      phone: '',
      email: '',
      emergency_contact: '',
      medical_conditions: [] as string[],
      allergies: '',
      incident_details: ''
    }
  })

  const [currentCondition, setCurrentCondition] = useState('')

  const emergencyTypes = [
    { value: 'medical', label: 'Medical Emergency', icon: Heart, color: 'text-red-600' },
    { value: 'police', label: 'Police Emergency', icon: Shield, color: 'text-blue-600' },
    { value: 'fire', label: 'Fire Emergency', icon: Flame, color: 'text-orange-600' }
  ]

  const pakistanCities = [
    'Lahore', 'Karachi', 'Islamabad', 'Rawalpindi', 'Faisalabad', 
    'Multan', 'Peshawar', 'Quetta', 'Sialkot', 'Gujranwala'
  ]

  const commonConditions = [
    'Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 'Allergies',
    'Pregnancy', 'Epilepsy', 'Kidney Disease', 'Liver Disease'
  ]

  const handleInputChange = (field: string, value: any) => {
    if (field.startsWith('citizen_data.')) {
      const citizenField = field.replace('citizen_data.', '')
      setFormData(prev => ({
        ...prev,
        citizen_data: {
          ...prev.citizen_data,
          [citizenField]: value
        }
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }))
    }
  }

  const addMedicalCondition = () => {
    if (currentCondition && !formData.citizen_data.medical_conditions.includes(currentCondition)) {
      setFormData(prev => ({
        ...prev,
        citizen_data: {
          ...prev.citizen_data,
          medical_conditions: [...prev.citizen_data.medical_conditions, currentCondition]
        }
      }))
      setCurrentCondition('')
    }
  }

  const removeMedicalCondition = (condition: string) => {
    setFormData(prev => ({
      ...prev,
      citizen_data: {
        ...prev.citizen_data,
        medical_conditions: prev.citizen_data.medical_conditions.filter(c => c !== condition)
      }
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate required fields
    if (!formData.symptoms || !formData.location || !formData.citizen_data.name || !formData.citizen_data.phone) {
      alert('Please fill in all required fields')
      return
    }

    // Convert age to number
    const submitData = {
      ...formData,
      citizen_data: {
        ...formData.citizen_data,
        age: parseInt(formData.citizen_data.age) || 0
      }
    }

    onSubmit(submitData)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Emergency Request Form</h2>
          <p className="text-gray-600">Please provide details about your emergency situation</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Emergency Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Emergency Type *
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {emergencyTypes.map((type) => {
                const Icon = type.icon
                return (
                  <motion.button
                    key={type.value}
                    type="button"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleInputChange('emergency_type', type.value)}
                    className={`p-4 rounded-xl border-2 transition-all ${
                      formData.emergency_type === type.value
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon className={`h-8 w-8 mx-auto mb-2 ${type.color}`} />
                    <div className="font-medium text-gray-900">{type.label}</div>
                  </motion.button>
                )
              })}
            </div>
          </div>

          {/* Symptoms/Incident Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {formData.emergency_type === 'medical' ? 'Symptoms Description *' : 'Incident Description *'}
            </label>
            <textarea
              value={formData.symptoms}
              onChange={(e) => handleInputChange('symptoms', e.target.value)}
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder={
                formData.emergency_type === 'medical' 
                  ? 'Describe your symptoms in detail (e.g., chest pain, difficulty breathing, fever)'
                  : 'Describe the incident (e.g., robbery, fire, accident)'
              }
              required
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Location *
            </label>
            <select
              value={formData.location}
              onChange={(e) => handleInputChange('location', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            >
              <option value="">Select your city</option>
              {pakistanCities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          {/* Personal Information */}
          <div className="bg-gray-50 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <User className="h-5 w-5 mr-2" />
              Personal Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  value={formData.citizen_data.name}
                  onChange={(e) => handleInputChange('citizen_data.name', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Age
                </label>
                <input
                  type="number"
                  value={formData.citizen_data.age}
                  onChange={(e) => handleInputChange('citizen_data.age', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter your age"
                  min="0"
                  max="120"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  value={formData.citizen_data.phone}
                  onChange={(e) => handleInputChange('citizen_data.phone', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="+92 300 1234567"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email (Optional)
                </label>
                <input
                  type="email"
                  value={formData.citizen_data.email}
                  onChange={(e) => handleInputChange('citizen_data.email', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="your.email@example.com"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Emergency Contact
                </label>
                <input
                  type="tel"
                  value={formData.citizen_data.emergency_contact}
                  onChange={(e) => handleInputChange('citizen_data.emergency_contact', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Emergency contact phone number"
                />
              </div>
            </div>
          </div>

          {/* Medical Information (only for medical emergencies) */}
          {formData.emergency_type === 'medical' && (
            <div className="bg-red-50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Heart className="h-5 w-5 mr-2 text-red-600" />
                Medical Information
              </h3>

              {/* Medical Conditions */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Existing Medical Conditions
                </label>
                <div className="flex gap-2 mb-2">
                  <select
                    value={currentCondition}
                    onChange={(e) => setCurrentCondition(e.target.value)}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Select a condition</option>
                    {commonConditions.map(condition => (
                      <option key={condition} value={condition}>{condition}</option>
                    ))}
                  </select>
                  <button
                    type="button"
                    onClick={addMedicalCondition}
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    Add
                  </button>
                </div>
                
                {/* Display selected conditions */}
                {formData.citizen_data.medical_conditions.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {formData.citizen_data.medical_conditions.map((condition, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800"
                      >
                        {condition}
                        <button
                          type="button"
                          onClick={() => removeMedicalCondition(condition)}
                          className="ml-2 text-primary-600 hover:text-primary-800"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Allergies */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Known Allergies
                </label>
                <input
                  type="text"
                  value={formData.citizen_data.allergies}
                  onChange={(e) => handleInputChange('citizen_data.allergies', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="List any known allergies (medications, food, etc.)"
                />
              </div>
            </div>
          )}

          {/* Incident Details (for police/fire emergencies) */}
          {formData.emergency_type !== 'medical' && (
            <div className="bg-blue-50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <FileText className="h-5 w-5 mr-2 text-blue-600" />
                Additional Details
              </h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Information
                </label>
                <textarea
                  value={formData.citizen_data.incident_details}
                  onChange={(e) => handleInputChange('citizen_data.incident_details', e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Provide any additional details that might be helpful"
                />
              </div>
            </div>
          )}

          {/* Submit Button */}
          <div className="text-center">
            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-xl shadow-lg hover:from-primary-700 hover:to-primary-800 transition-all"
            >
              <Send className="h-5 w-5 mr-2" />
              Submit Emergency Request
            </motion.button>
          </div>
        </form>
      </motion.div>
    </div>
  )
}