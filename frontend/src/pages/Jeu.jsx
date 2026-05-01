import { useState } from 'react'

const ROWS = [
  { color: 'bg-amber-800', value: 1, text: 'text-white', reward: 0 },
  { color: 'bg-amber-800', value: 1, text: 'text-white', reward: 0 },
  { color: 'bg-gray-400', value: 2, text: 'text-white', reward: 0.001 },
  { color: 'bg-gray-400', value: 2, text: 'text-white', reward: 0.001 },
  { color: 'bg-yellow-400', value: 5, text: 'text-black', reward: 0.01 },
  { color: 'bg-cyan-300', value: 7, text: 'text-black', reward: 0.05 },
]

const TOP_ROWS = 3
const COLS = 5
const CELLS = TOP_ROWS * COLS
const MISE_STEP = 10
const MISE_MIN = 10
const SPINS_PER_MISE = 4
const MAX_PICKAXES = 12

const PICKAXES = [
  '/wood-pickaxe.png',
  '/iron-pickaxe.png',
  '/gold-pickaxe.png',
  '/diamond-pickaxe.png',
]

const PICKAXE_DAMAGE = {
  '/wood-pickaxe.png': 1,
  '/iron-pickaxe.png': 2,
  '/gold-pickaxe.png': 3,
  '/diamond-pickaxe.png': 5,
}

const MULTIPLIERS = [
  { value: 2, weight: 40 },
  { value: 4, weight: 30 },
  { value: 10, weight: 15 },
  { value: 18, weight: 10 },
  { value: 65, weight: 5 },
]

function randomMultiplier() {
  const total = MULTIPLIERS.reduce((s, m) => s + m.weight, 0)
  let r = Math.random() * total
  for (const m of MULTIPLIERS) {
    if (r < m.weight) return m.value
    r -= m.weight
  }
  return MULTIPLIERS[MULTIPLIERS.length - 1].value
}

function generatePickaxes() {
  const count = Math.floor(Math.random() * (MAX_PICKAXES + 1))
  const positions = new Set()
  while (positions.size < count) {
    positions.add(Math.floor(Math.random() * CELLS))
  }
  return Array.from({ length: CELLS }, (_, i) =>
    positions.has(i) ? PICKAXES[Math.floor(Math.random() * PICKAXES.length)] : null
  )
}

function initialHp() {
  return ROWS.map(row => Array.from({ length: COLS }, () => row.value))
}

function applyDamage(hp, pickaxes) {
  const next = hp.map(row => [...row])
  for (let col = 0; col < COLS; col++) {
    let dmg = 0
    for (let r = 0; r < TOP_ROWS; r++) {
      const src = pickaxes[r * COLS + col]
      if (src) dmg += PICKAXE_DAMAGE[src]
    }
    for (let r = 0; r < ROWS.length && dmg > 0; r++) {
      if (next[r][col] > 0) {
        const dealt = Math.min(dmg, next[r][col])
        next[r][col] -= dealt
        dmg -= dealt
      }
    }
  }
  return next
}

function Jeu({ tokens, setTokens, winnings, setWinnings }) {
  const [pickaxeGrid, setPickaxeGrid] = useState(() => Array(CELLS).fill(null))
  const [blockHp, setBlockHp] = useState(initialHp)
  const [chests, setChests] = useState(() => Array(COLS).fill(null))
  const [mise, setMise] = useState(100)
  const [spinsLeft, setSpinsLeft] = useState(0)
  const [message, setMessage] = useState('')

  const inBet = spinsLeft > 0

  const handleMiser = () => {
    if (inBet) return
    if (tokens < mise) {
      setMessage('Pas assez de tokens')
      return
    }
    setMessage('')
    setTokens(tokens - mise)
    setSpinsLeft(SPINS_PER_MISE)
    setBlockHp(initialHp())
    setPickaxeGrid(Array(CELLS).fill(null))
    setChests(Array(COLS).fill(null))
    setWinnings(0)
  }

  const handleSpin = () => {
    if (!inBet) return
    const newPickaxes = generatePickaxes()
    const newHp = applyDamage(blockHp, newPickaxes)

    let delta = 0
    for (let r = 0; r < ROWS.length; r++) {
      for (let c = 0; c < COLS; c++) {
        if (blockHp[r][c] > 0 && newHp[r][c] === 0) {
          delta += ROWS[r].reward * mise
        }
      }
    }

    const newChests = chests.map((existing, col) => {
      if (existing !== null) return existing
      const cleared = newHp.every(row => row[col] === 0)
      return cleared ? randomMultiplier() : null
    })

    const newSpinsLeft = spinsLeft - 1
    const rawTotal = winnings + delta
    let finalWinnings = rawTotal
    if (newSpinsLeft === 0) {
      const totalMult = newChests.reduce((s, m) => s + (m ?? 0), 0)
      if (totalMult > 0) finalWinnings = rawTotal * totalMult
      setTokens(tokens + finalWinnings)
    }

    setPickaxeGrid(newPickaxes)
    setBlockHp(newHp)
    setChests(newChests)
    setWinnings(finalWinnings)
    setSpinsLeft(newSpinsLeft)
  }

  return (
    <div className="flex items-center gap-16">
      <div className="w-44 flex flex-col items-center gap-2">
        <span className="text-sm font-bold">Mise</span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setMise(Math.max(MISE_MIN, mise - MISE_STEP))}
            disabled={inBet}
            className="w-8 h-8 bg-gray-300 border border-black font-bold disabled:opacity-50"
          >-</button>
          <span className="w-12 text-center font-bold">{mise}</span>
          <button
            onClick={() => setMise(mise + MISE_STEP)}
            disabled={inBet}
            className="w-8 h-8 bg-gray-300 border border-black font-bold disabled:opacity-50"
          >+</button>
        </div>
      </div>

      <div className="flex flex-col items-center">
        <div className="grid grid-cols-5 gap-1 mb-6">
          {pickaxeGrid.map((src, i) => (
            <div
              key={`top-${i}`}
              className="w-10 h-10 bg-gray-400 border border-black flex items-center justify-center"
            >
              {src && <img src={src} alt="" className="w-8 h-8 object-contain" />}
            </div>
          ))}
        </div>

        <div className="p-2">
          <div className="grid grid-cols-5 gap-1">
            {ROWS.flatMap((block, row) =>
              Array.from({ length: COLS }, (_, col) => {
                const hp = blockHp[row][col]
                if (hp <= 0) {
                  return <div key={`${row}-${col}`} className="w-10 h-10" />
                }
                return (
                  <div
                    key={`${row}-${col}`}
                    className={`w-10 h-10 ${block.color} ${block.text} border border-black flex items-center justify-center font-bold`}
                  >
                    {hp}
                  </div>
                )
              })
            )}
          </div>
        </div>

        <div className="relative z-10 grid grid-cols-5 gap-1 mt-6">
          {chests.map((mult, i) => (
            <div
              key={i}
              className="w-10 h-10 bg-[#b8794a] border-2 border-[#7a4e2a] flex items-center justify-center text-white font-bold text-xs"
            >
              {mult !== null && `x${mult}`}
            </div>
          ))}
        </div>
      </div>

      <div className="w-44 flex items-center justify-center gap-2 relative">
        <button
          onClick={handleMiser}
          disabled={inBet}
          className="w-16 h-16 bg-green-500 text-white font-bold border border-black disabled:opacity-50 disabled:cursor-not-allowed"
        >
          MISER
        </button>
        <button
          onClick={handleSpin}
          disabled={!inBet}
          className="w-16 h-16 bg-green-500 text-white font-bold border border-black flex flex-col items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span className="text-xs">SPIN</span>
          <span>{spinsLeft}</span>
        </button>
        {message && (
          <span className="absolute top-full mt-2 text-sm text-red-600 font-bold text-center whitespace-nowrap">
            {message}
          </span>
        )}
      </div>

    </div>
  )
}

export default Jeu
