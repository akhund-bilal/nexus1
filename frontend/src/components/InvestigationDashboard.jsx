import React, { useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export function InvestigationDashboard() {
  const [identifier, setIdentifier] = useState('')
  const [result, setResult] = useState(null)

  const runSearch = async () => {
    const payload = {
      case_name: 'Demo Investigation',
      description: 'Public-only OSINT lookup',
      identifiers: [{ input_type: 'username', value: identifier }],
    }
    const { data } = await axios.post(`${API}/search`, payload)
    setResult(data)
  }

  return (
    <div style={{ fontFamily: 'sans-serif', margin: 24 }}>
      <h1>Nexus1 OSINT Intelligence Platform</h1>
      <p>Public data only. No private data or authentication bypass.</p>
      <input value={identifier} onChange={(e) => setIdentifier(e.target.value)} placeholder="username" />
      <button onClick={runSearch} style={{ marginLeft: 8 }}>Investigate</button>
      {result && (
        <div>
          <h2>Case #{result.case_id}</h2>
          <h3>Profiles</h3>
          <ul>
            {result.profiles.map((p, idx) => (
              <li key={idx}>{p.platform} / {p.handle} / {p.authenticity_score}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
