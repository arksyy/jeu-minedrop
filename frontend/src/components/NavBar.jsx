import { Link, NavLink } from 'react-router-dom'

const linkClass = ({ isActive }) => (isActive ? 'font-bold' : '')

function NavBar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-white border-b border-gray-200 text-gray-900">
      <Link to="/" className="text-2xl font-bold">MineDrop</Link>
      <div className="flex gap-6">
        <NavLink to="/" end className={linkClass}>Accueil</NavLink>
        <NavLink to="/jeu" className={linkClass}>Jeu</NavLink>
        <NavLink to="/tokens" className={linkClass}>Tokens</NavLink>
      </div>
    </nav>
  )
}

export default NavBar
