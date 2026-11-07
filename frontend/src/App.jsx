import { useEffect, useState } from 'react'
import { Activity, BrainCircuit, CheckCircle2, CircleHelp, FileText, Gauge, Github, Loader2, MessageSquareText, ShieldCheck, Sparkles, ThumbsDown, ThumbsUp, TriangleAlert } from 'lucide-react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState(null)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [history, setHistory] = useState([])

  async function refresh() {
    try {
      const [s, h] = await Promise.all([fetch(`${API}/model/status`), fetch(`${API}/feedback`)])
      setStatus(await s.json())
      setHistory(await h.json())
    } catch {
      setStatus({ model_ready: false, message: 'Cannot reach backend. Start the FastAPI server.' })
    }
  }
  useEffect(() => { refresh() }, [])

  async function analyze() {
    if (text.trim().length < 10) { setMessage('Enter at least 10 characters of news text.'); return }
    setBusy(true); setMessage(''); setResult(null)
    try {
      const response = await fetch(`${API}/predict`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Prediction failed.')
      setResult(data)
    } catch (e) { setMessage(e.message) }
    finally { setBusy(false) }
  }

  async function sendFeedback(label) {
    setBusy(true); setMessage('')
    try {
      const response = await fetch(`${API}/feedback`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text, label })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Could not save feedback.')
      setMessage(`Your ${label} feedback has been saved.`)
      await refresh()
    } catch (e) { setMessage(e.message) }
    finally { setBusy(false) }
  }

  const isFake = result?.label === 'FAKE'
  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#"><span className="brand-icon"><BrainCircuit size={22}/></span><span>ADAPTIVE<span className="brand-accent">AI</span></span></a>
      <div className="top-actions"><span className={`status-pill ${status?.model_ready ? 'online' : 'offline'}`}><i/>{status?.model_ready ? 'Model ready' : 'Model not trained'}</span><a className="github-link" href="https://github.com/" target="_blank" rel="noreferrer"><Github size={17}/> GitHub</a></div>
    </header>

    <main>
      <section className="hero">
        <div className="eyebrow"><Sparkles size={14}/> NLP · BERT · HUMAN FEEDBACK</div>
        <h1>Pause. Verify.<br/><span>Know what you read.</span></h1>
        <p className="hero-copy">An experimental AI assistant that analyzes news text using a fine-tuned BERT language model and learns from saved human feedback.</p>
      </section>

      <section className="workspace">
        <div className="panel input-panel">
          <div className="panel-heading"><div><span className="step">01 / ANALYZE</span><h2>News analyzer</h2></div><FileText size={21}/></div>
          <label htmlFor="news">Paste a news headline or article</label>
          <textarea id="news" value={text} onChange={e => setText(e.target.value)} placeholder="Paste the news text you want to analyze..." maxLength={10000}/>
          <div className="input-footer"><span>{text.length.toLocaleString()} / 10,000 characters</span><button className="analyze-btn" onClick={analyze} disabled={busy}>{busy ? <Loader2 className="spin" size={17}/> : <Activity size={17}/>} Analyze news</button></div>
          {message && <div className="message"><TriangleAlert size={16}/>{message}</div>}
          <div className="privacy-note"><ShieldCheck size={15}/> Text is sent to your configured backend for analysis.</div>
        </div>

        <div className="panel result-panel">
          <div className="panel-heading"><div><span className="step">02 / RESULT</span><h2>Analysis result</h2></div><Gauge size={21}/></div>
          {!result ? <div className="empty-result"><div className="empty-icon"><BrainCircuit size={30}/></div><h3>Waiting for your text</h3><p>Your classification and confidence score will appear here after analysis.</p></div> :
            <div className="result-content">
              <div className={`verdict ${isFake ? 'fake' : 'real'}`}><span className="verdict-icon">{isFake ? <TriangleAlert size={22}/> : <CheckCircle2 size={22}/>}</span><div><small>MODEL CLASSIFICATION</small><strong>{result.label} NEWS</strong></div></div>
              <div className="confidence"><div className="confidence-top"><span>Model confidence</span><strong>{result.confidence == null ? 'Feedback label' : `${(result.confidence * 100).toFixed(1)}%`}</strong></div><div className="meter"><i style={{width: `${(result.confidence ?? 0) * 100}%`}}/></div></div>
              <p className="result-note"><CircleHelp size={16}/>{result.note}</p>
              <div className="feedback"><span>Is this classification correct?</span><div><button onClick={() => sendFeedback('REAL')} disabled={busy}><ThumbsUp size={15}/> Real</button><button onClick={() => sendFeedback('FAKE')} disabled={busy}><ThumbsDown size={15}/> Fake</button></div></div>
            </div>}
        </div>
      </section>

      <section className="bottom-grid">
        <div className="info-card"><div className="info-icon"><BrainCircuit/></div><div><h3>BERT-powered NLP</h3><p>Context-aware text representation through a Transformer model.</p></div></div>
        <div className="info-card"><div className="info-icon"><MessageSquareText/></div><div><h3>Human feedback memory</h3><p>Stores corrections and applies them to the exact same text in future checks.</p></div></div>
        <div className="info-card"><div className="info-icon"><Activity/></div><div><h3>Continuous improvement</h3><p>Feedback can be exported and included in a later model-training run.</p></div></div>
      </section>

      <section className="history panel">
        <div className="panel-heading"><div><span className="step">03 / FEEDBACK</span><h2>Recent feedback</h2></div><span className="history-count">{history.length} saved</span></div>
        {history.length === 0 ? <p className="muted">No feedback submitted yet. Your saved corrections will appear here.</p> :
          <div className="history-list">{history.slice(0,5).map(item => <div className="history-row" key={item.id}><span className={`label-chip ${item.label.toLowerCase()}`}>{item.label}</span><span className="history-text">{item.text}</span><time>{new Date(item.created_at + 'Z').toLocaleDateString()}</time></div>)}</div>}
      </section>
      <p className="disclaimer"><TriangleAlert size={15}/> Research / academic prototype only. AI classification can be wrong. Always verify claims with trustworthy primary sources; this tool does not establish factual truth.</p>
    </main>
    <footer><span>ADAPTIVE AI · FAKE NEWS DETECTOR</span><span>Built with React · FastAPI · PyTorch · BERT</span></footer>
  </div>
}
