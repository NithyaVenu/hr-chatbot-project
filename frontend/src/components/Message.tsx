import React from 'react'

export default function Message({ text }: { text: string }) {
  return (
    <div className="p-3 bg-gray-50 rounded">
      {text}
    </div>
  )
}
