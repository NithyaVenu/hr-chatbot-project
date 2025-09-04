import React, { useState } from 'react'
import axios from 'axios'
import Message from './Message'
import EmployeeCard from './EmployeeCard'

type Props = { backend: string }

export default function Chat({ backend }: Props) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState<string | null>(null)
  const [candidates, setCandidates] = useState<any[]>([])

  const ask = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${backend}/chat`, { query, top_k: 5 }, { timeout: 60000 })
      setAnswer(res.data.answer)
      setCandidates(res.data.candidates || [])
    } catch (err: any) {
      console.error(err)
      setAnswer('Error: ' + (err?.response?.data?.detail || err.message))
      setCandidates([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <div className="mb-4">
        <textarea
          className="w-full border rounded p-3 h-28"
          placeholder="e.g., Find Python developers with 3+ years for healthcare"
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-3 mb-6">
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={ask} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
        <button className="px-4 py-2 bg-gray-200 rounded" onClick={() => { setQuery(''); setAnswer(null); setCandidates([]) }}>
          Clear
        </button>
      </div>

      <div>
        {answer && (
          <div className="mb-4">
            <h2 className="font-semibold text-lg">Answer</h2>
            <div className="whitespace-pre-wrap mt-2 text-gray-800 p-4 bg-gray-50 rounded">{answer}</div>
          </div>
        )}

        {candidates.length > 0 && (
          <div>
            <h2 className="font-semibold text-lg mb-2">Candidates</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {candidates.map(c => <EmployeeCard key={c.id} emp={c} />)}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
