import React, { useState } from 'react'
import axios from 'axios'
import Chat from './components/Chat'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-blue-800">HR Resource Chatbot</h1>
          <p className="text-sm text-gray-600">Ask natural language queries to find employees.</p>
        </header>
        <Chat backend={BACKEND} />
      </div>
    </div>
  )
}

export default App
