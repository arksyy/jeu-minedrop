import { BrowserRouter, Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Jeu from './pages/Jeu'
import Tokens from './pages/Tokens'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-sky-300 text-gray-900">
        <NavBar />
        <main className="flex-1 flex items-center justify-center p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/jeu" element={<Jeu />} />
            <Route path="/tokens" element={<Tokens />} />
          </Routes>
        </main>
        <div className="relative h-32 bg-green-500">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-xs h-10 bg-gray-300 border-2 border-gray-500" />
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
