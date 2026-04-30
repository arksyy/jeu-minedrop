const ACTIVITIES = [
  'Push ups',
  'Jumping jacks',
  'Shadow boxing',
  '6-7 memes',
]

function Tokens({ tokens, setTokens: _setTokens }) {
  return (
    <section className="w-full max-w-5xl mx-auto text-gray-900">
      <div className="grid gap-6 lg:grid-cols-[1.45fr_0.85fr] items-start">
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-white">
              Obtenir des jetons
            </p>
          </div>

          <div className="bg-gray-200 px-6 py-8 sm:px-8">
            <h1 className="text-4xl font-black uppercase leading-tight sm:text-5xl">
              Gagne des jetons avec des defis
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-gray-700 sm:text-lg">
              Realise un defi physique, valide-le, puis recupere des jetons pour revenir jouer.
            </p>
            <p className="mt-4 text-sm font-bold uppercase tracking-wide text-gray-900">
              Solde actuel : {tokens}
            </p>

            <div
              id="camera-mount"
              className="mt-6 aspect-square w-full max-w-xl border-2 border-black bg-gray-100 flex items-center justify-center"
            >
              <p className="px-4 text-center text-sm font-bold uppercase tracking-wide text-gray-700">
                La camera sera affichee ici
              </p>
            </div>
          </div>
        </div>

        <aside className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-cyan-300 px-4 py-3">
            <h2 className="text-xl font-black uppercase text-black">Defis physiques</h2>
          </div>
          <ul className="grid gap-1 p-3">
            {ACTIVITIES.map(activity => (
              <li
                key={activity}
                className="border border-black bg-white px-4 py-3 font-bold uppercase text-gray-900"
              >
                {activity}
              </li>
            ))}
          </ul>
        </aside>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-wide text-white">Etape 1</p>
          </div>
          <div className="px-5 py-5">
            <h3 className="text-2xl font-black uppercase">Bouge</h3>
            <p className="mt-3 text-sm leading-6 text-gray-700">
              Tu realises un defi physique devant la camera pour debloquer des jetons.
            </p>
          </div>
        </div>

        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-wide text-white">Etape 2</p>
          </div>
          <div className="px-5 py-5">
            <h3 className="text-2xl font-black uppercase">Validation</h3>
            <p className="mt-3 text-sm leading-6 text-gray-700">
              Quand ton defi est valide, tu pourras ajouter des jetons a ton solde.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Tokens
