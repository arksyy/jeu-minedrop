const ROWS = [
  'bg-green-500',
  'bg-amber-800',
  'bg-amber-800',
  'bg-gray-400',
  'bg-red-400',
  'bg-yellow-400',
  'bg-cyan-300',
]

const COLS = 5

function Jeu() {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="p-2">
        <div className="grid grid-cols-5 gap-1">
          {ROWS.flatMap((color, row) =>
            Array.from({ length: COLS }, (_, col) => (
              <div
                key={`${row}-${col}`}
                className={`w-14 h-14 ${color} border border-black`}
              />
            ))
          )}
        </div>
      </div>

      <div className="grid grid-cols-5 gap-1 mt-24">
        {Array.from({ length: COLS }, (_, i) => (
          <div
            key={i}
            className="w-14 h-14 bg-amber-700 border-2 border-amber-900"
          />
        ))}
      </div>
    </div>
  )
}

export default Jeu
