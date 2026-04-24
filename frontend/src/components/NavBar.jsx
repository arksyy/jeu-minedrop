import { Link } from 'react-router-dom'

function NavBar() {
  return (
    <nav className="flex gap-6 p-4 bg-white border-b border-gray-200 text-gray-900">
      <Link to="/">Accueil</Link>
      <Link to="/jeu">Jeu</Link>
      <Link to="/tokens">Tokens</Link>
    </nav>
  )
}

export default NavBar
