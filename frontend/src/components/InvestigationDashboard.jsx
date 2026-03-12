import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const navItems = ['Dashboard', 'Cases', 'Search', 'Entities', 'Graph', 'Timeline', 'Findings', 'Analytics', 'Reports']

export function InvestigationDashboard() {
  const [identifier, setIdentifier] = useState('')
  const [summary, setSummary] = useState(null)
  const [result, setResult] = useState(null)

  const loadSummary = async () => {
    const { data } = await axios.get(`${API}/dashboard/summary`)
    setSummary(data)
  }

  useEffect(() => {
    loadSummary().catch(() => undefined)
  }, [])

  const runSearch = async () => {
    if (!identifier.trim()) return
    const payload = {
      case_name: `Investigation: ${identifier}`,
      description: 'Public-only OSINT lookup',
      identifiers: [{ input_type: 'username', value: identifier }],
    }
    const { data } = await axios.post(`${API}/search`, payload)
    setResult(data)
    await loadSummary()
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">OSINT.INTEL</div>
        <div className="sub">OPEN SOURCE INTELLIGENCE PLATFORM</div>
        <nav>
          {navItems.map((item, idx) => (
            <div key={item} className={`nav-item ${idx === 0 ? 'active' : ''}`}>{item}</div>
          ))}
        </nav>
      </aside>

      <main className="content">
        <header className="topbar">
          <h1>Research Dashboard</h1>
          <div className="status">SYSTEM ONLINE · NO AI API</div>
        </header>

        <section className="search-box">
          <input value={identifier} onChange={(e) => setIdentifier(e.target.value)} placeholder="Enter username, email, domain..." />
          <button onClick={runSearch}>Investigate</button>
        </section>

        <section className="cards">
          <Metric title="Active Cases" value={summary?.active_cases ?? 0} />
          <Metric title="Total Entities" value={summary?.tracked_entities ?? 0} />
          <Metric title="Findings" value={summary?.flagged_findings ?? 0} />
          <Metric title="Data Points" value={summary?.total_data_points ?? 0} />
        </section>

        <section className="panels">
          <div className="panel">
            <h3>Recent Cases</h3>
            {(summary?.recent_cases ?? []).map((c) => <p key={c.id}>{c.name}</p>)}
          </div>
          <div className="panel">
            <h3>High Severity Findings</h3>
            {(summary?.high_severity_findings ?? []).map((f, i) => <p key={i}>{f.title}</p>)}
          </div>
        </section>

        {result && (
          <section className="panel">
            <h3>Case #{result.case_id} Output</h3>
            <p>Risk Level: {result.risk.risk_level} | Confidence: {result.risk.identity_confidence}</p>
            <ul>
              {result.profiles.map((p, idx) => <li key={idx}>{p.platform} / {p.handle}</li>)}
            </ul>
            <h4>Live Web Search Hits</h4>
            <ul>
              {(result.web_results || []).slice(0, 6).map((r, idx) => (
                <li key={idx}><a href={r.url} target="_blank" rel="noreferrer">{r.title}</a></li>
              ))}
            </ul>
          </section>
        )}
      </main>
    </div>
  )
}

function Metric({ title, value }) {
  return (
    <div className="card">
      <div className="card-title">{title}</div>
      <div className="card-value">{value}</div>
    </div>
  )
}
