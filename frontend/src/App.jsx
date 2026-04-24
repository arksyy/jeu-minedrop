import { useEffect } from 'react'
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

  useEffect(() => {
    document.title = TITLES[pathname] ?? 'Minedrop'
  }, [pathname])

  return (
    <div className="min-h-screen flex flex-col bg-sky-300 text-gray-900">
      <NavBar />
      <main className={`flex-1 flex flex-col items-center justify-end px-8 pt-8 ${showPlatform ? 'pb-0' : 'pb-12'}`}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/jeu" element={<Jeu />} />
          <Route path="/tokens" element={<Tokens />} />
        </Routes>
      </main>
      <div className="h-32 bg-green-500 flex items-center justify-center">
        <span className="font-bold">Tokens : 1234</span>
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
