import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Jeu from './pages/Jeu'
import Tokens from './pages/Tokens'

const TITLES = {
  '/': 'Minedrop',
  '/jeu': 'Jeu - Minedrop',
  '/tokens': 'Tokens - Minedrop',
}

function Layout() {
  const { pathname } = useLocation()
  const showPlatform = pathname === '/jeu'
  const [tokens, setTokens] = useState(() => {
    const saved = Number(localStorage.getItem('minedrop.tokens'))
    return Number.isFinite(saved) ? saved : 0
  })
  const [winnings, setWinnings] = useState(0)
  const [motionConnected, setMotionConnected] = useState(false)

  useEffect(() => {
    localStorage.setItem('minedrop.tokens', String(tokens))
  }, [tokens])

  useEffect(() => {
    document.title = TITLES[pathname] ?? 'Minedrop'
  }, [pathname])

  useEffect(() => {
    const host = window.location.hostname || 'localhost'
    const ws = new WebSocket(`ws://${host}:8000/ws`)
    ws.onopen = () => setMotionConnected(true)
    ws.onclose = () => setMotionConnected(false)
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data)
        if (typeof data.tokens === 'number') {
          setTokens(t => t + data.tokens)
        }
      } catch {
        // ignore malformed payload
      }
    }
    return () => ws.close()
  }, [])

  return (
    <div className="min-h-screen flex flex-col bg-sky-300 text-gray-900">
      <NavBar />
      <main className="flex-1 flex flex-col items-center px-8 pt-4 pb-14">
        {showPlatform && (
          <div className="flex-1 flex items-center">
            <span className="font-bold">Tokens : {tokens.toFixed(2)}</span>
          </div>
        )}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/jeu"
            element={
              <Jeu
                tokens={tokens}
                setTokens={setTokens}
                winnings={winnings}
                setWinnings={setWinnings}
              />
            }
          />
          <Route path="/tokens" element={<Tokens tokens={tokens} setTokens={setTokens} motionConnected={motionConnected} />} />
        </Routes>
      </main>
      <div className="relative h-32 bg-green-500 flex items-center justify-center">
        {showPlatform && (
          <div className="absolute bottom-full left-1/2 -translate-x-1/2 w-[232px] h-10 bg-gray-300 border-2 border-gray-500 flex items-center justify-center font-bold">
            {winnings.toFixed(2)}
          </div>
        )}
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}

export default App
