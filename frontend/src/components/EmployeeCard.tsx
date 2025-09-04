import React from 'react'

export default function EmployeeCard({ emp }: any) {
  return (
    <div className="border rounded p-4 bg-white shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-lg">{emp.name}</h3>
          <p className="text-sm text-gray-600">{emp.experience_years} yrs · {emp.availability}</p>
        </div>
        <div className="text-sm text-gray-500">Score: {emp.match_score}</div>
      </div>
      <div className="mt-3">
        <p className="text-sm"><strong>Skills:</strong> {emp.skills.join(', ')}</p>
        <p className="text-sm mt-1"><strong>Projects:</strong> {emp.projects.join(', ')}</p>
      </div>
    </div>
  )
}
