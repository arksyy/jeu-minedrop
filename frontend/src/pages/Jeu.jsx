const ROWS = [
  { color: 'bg-amber-800', value: 1, text: 'text-white' },
  { color: 'bg-amber-800', value: 1, text: 'text-white' },
  { color: 'bg-gray-400', value: 2, text: 'text-white' },
  { color: 'bg-gray-400', value: 2, text: 'text-white' },
  { color: 'bg-yellow-400', value: 5, text: 'text-black' },
  { color: 'bg-cyan-300', value: 7, text: 'text-black' },
]

const TOP_ROWS = 3
const COLS = 5

function Jeu() {
  return (
    <div className="flex items-center gap-16">

      <div className="flex flex-col items-center gap-2">
        <span className="text-sm font-bold">Mise</span>
        <div className="flex items-center gap-2">
          <button className="w-8 h-8 bg-gray-300 border border-black font-bold">-</button>
          <span className="w-12 text-center font-bold">100</span>
          <button className="w-8 h-8 bg-gray-300 border border-black font-bold">+</button>
        </div>
      </div>

      <div className="flex flex-col items-center">
        <div className="grid grid-cols-5 gap-1 mb-6">
          {Array.from({ length: TOP_ROWS * COLS }, (_, i) => (
            <div key={`top-${i}`} className="w-10 h-10 bg-gray-400 border border-black" />
          ))}
        </div>

        <div className="p-2">
          <div className="grid grid-cols-5 gap-1">
            {ROWS.flatMap((block, row) =>
              Array.from({ length: COLS }, (_, col) => (
                <div
                  key={`${row}-${col}`}
                  className={`w-10 h-10 ${block.color} ${block.text} border border-black flex items-center justify-center font-bold`}
                >
                  {block.value}
                </div>
              ))
            )}
          </div>
        </div>

        <div className="grid grid-cols-5 gap-1 mt-6">
          {Array.from({ length: COLS }, (_, i) => (
            <div key={i} className="w-10 h-10 bg-[#b8794a] border-2 border-[#7a4e2a]" />
          ))}
        </div>
      </div>

      <button className="w-14 h-32 bg-green-500 text-white font-bold border border-black">
        SPIN
      </button>

    </div>
  )
}

export default Jeu
