import { BrowserRouter, Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Jeu from './pages/Jeu'
import Tokens from './pages/Tokens'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-900">
        <NavBar />
        <main className="flex items-center justify-center p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/jeu" element={<Jeu />} />
            <Route path="/tokens" element={<Tokens />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
