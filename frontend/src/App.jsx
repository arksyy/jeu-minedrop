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
  const [tokens, setTokens] = useState(1234)
  const [winnings, setWinnings] = useState(0)

  useEffect(() => {
    document.title = TITLES[pathname] ?? 'Minedrop'
  }, [pathname])

  return (
    <div className="min-h-screen flex flex-col bg-sky-300 text-gray-900">
      <NavBar />
      <main className="flex-1 flex flex-col items-center justify-end px-8 pt-8 pb-12">
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
          <Route path="/tokens" element={<Tokens tokens={tokens} setTokens={setTokens} />} />
        </Routes>
      </main>
      <div className="relative h-32 bg-green-500 flex items-center justify-center">
        <span className="font-bold">Tokens : {tokens}</span>
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
