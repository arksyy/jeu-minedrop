import { Link } from 'react-router-dom'

function NavBar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-white border-b border-gray-200 text-gray-900">
      <Link to="/" className="text-2xl font-bold">MineDrop</Link>
      <div className="flex gap-6">
        <Link to="/">Accueil</Link>
        <Link to="/jeu">Jeu</Link>
        <Link to="/tokens">Tokens</Link>
      </div>
    </nav>
  )
}

export default NavBar
