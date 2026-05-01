const ACTIVITIES = [
  'Push ups',
  'Jumping jacks',
  'Shadow boxing',
  '6-7 memes',
]

function Tokens({ tokens, setTokens: _setTokens }) {
  return (
    <section className="w-full max-w-5xl mx-auto flex-1 flex flex-col text-gray-900">
      <div className="flex-1 grid gap-4 lg:grid-cols-[1.45fr_0.85fr]">
        <div className="border-2 border-black bg-gray-300 flex flex-col">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-1.5">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-white">
              Obtenir des jetons
            </p>
          </div>

          <div className="bg-gray-200 px-5 py-4 sm:px-6 flex-1 flex flex-col">
            <h1 className="text-2xl font-black uppercase leading-tight sm:text-3xl">
              Gagne des jetons avec des défis
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-700">
              Réalise un défi physique, valide-le, puis récupère des jetons pour revenir jouer.
            </p>
            <p className="mt-2 text-xs font-bold uppercase tracking-wide text-gray-900">
              Solde actuel : {tokens}
            </p>

            <div
              id="camera-mount"
              className="mt-3 flex-1 w-full border-2 border-black bg-gray-100 flex items-center justify-center"
            >
              <p className="px-4 text-center text-xs font-bold uppercase tracking-wide text-gray-700">
                La caméra sera affichée ici
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <aside className="border-2 border-black bg-gray-300">
            <div className="border-b-2 border-black bg-cyan-300 px-4 py-3">
              <h2 className="text-xl font-black uppercase text-black">Activités physiques</h2>
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

          <div className="border-2 border-black bg-gray-300">
            <div className="border-b-2 border-black bg-amber-800 px-3 py-1.5">
              <p className="text-xs font-bold uppercase tracking-wide text-white">Etape 1</p>
            </div>
            <div className="px-3 py-2">
              <h3 className="text-base font-black uppercase">Bouge</h3>
              <p className="mt-1 text-xs leading-5 text-gray-700">
                Réalise un défi physique devant la caméra.
              </p>
            </div>
          </div>

          <div className="border-2 border-black bg-gray-300">
            <div className="border-b-2 border-black bg-amber-800 px-3 py-1.5">
              <p className="text-xs font-bold uppercase tracking-wide text-white">Etape 2</p>
            </div>
            <div className="px-3 py-2">
              <h3 className="text-base font-black uppercase">Validation</h3>
              <p className="mt-1 text-xs leading-5 text-gray-700">
                Ajoute les jetons gagnés à ton solde.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Tokens
