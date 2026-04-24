import { Link } from 'react-router-dom'

function Home() {
  return (
    <section className="w-full max-w-5xl mx-auto text-gray-900">
      <div className="grid gap-6 lg:grid-cols-[1.45fr_0.85fr] items-start">
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-white">
              Casino
            </p>
          </div>

          <div className="bg-gray-200 px-6 py-8 sm:px-8">
            <h1 className="text-4xl font-black uppercase leading-tight sm:text-5xl">
              MineDrop transforme l'effort en jeu de hasard
            </h1>

            <p className="mt-5 max-w-2xl text-base leading-7 text-gray-700 sm:text-lg">
              Le joueur doit obtenir des crédits en affectuant une activité physique. Lorsque je le joeur a des crédits, il peut
              jouer au jeu, le but du jeu est détruire une colonne poiur ouvrir le coffre qui contient un multiplicateur déterminé au hasard.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/jeu"
                className="border-2 border-black bg-yellow-400 px-5 py-3 font-bold uppercase tracking-wide text-black transition hover:bg-cyan-300"
              >
                Voir le jeu
              </Link>
              <Link
                to="/tokens"
                className="border-2 border-black bg-gray-400 px-5 py-3 font-bold uppercase tracking-wide text-white transition hover:bg-amber-800"
              >
                Voir les credits
              </Link>
            </div>
          </div>
        </div>

        <aside className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-cyan-300 px-4 py-3">
            <h2 className="text-xl font-black uppercase text-black">Activités physiques</h2>
          </div>
          <ul className="grid gap-1 p-3">
            <li className="border border-black bg-white px-4 py-3 font-bold uppercase text-gray-900">Push ups</li>
            <li className="border border-black bg-white px-4 py-3 font-bold uppercase text-gray-900">Jumping jacks</li>
            <li className="border border-black bg-white px-4 py-3 font-bold uppercase text-gray-900">Shadow boxing</li>
            <li className="border border-black bg-white px-4 py-3 font-bold uppercase text-gray-900">6-7 memes</li>
          </ul>
        </aside>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-wide text-white">
              Etape 1
            </p>
          </div>
          <div className="px-5 py-5">
            <h3 className="text-2xl font-black uppercase">Bouge</h3>
            <p className="mt-3 text-sm leading-6 text-gray-700">
              Tu réalises un défi physique pour obtenir des crédits.
            </p>
          </div>
        </div>
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-wide text-white">
              Etape 2
            </p>
          </div>
          <div className="px-5 py-5">
            <h3 className="text-2xl font-black uppercase">Validation des crédis</h3>
            <p className="mt-3 text-sm leading-6 text-gray-700">
              Les crédits sont appliqué lorsque tu valides une activité physique
            </p>
          </div>
        </div>
        <div className="border-2 border-black bg-gray-300">
          <div className="border-b-2 border-black bg-amber-800 px-4 py-2">
            <p className="text-sm font-bold uppercase tracking-wide text-white">
              Etape 3
            </p>
          </div>
          <div className="px-5 py-5">
            <h3 className="text-2xl font-black uppercase">Miser et jouer</h3>
            <p className="mt-3 text-sm leading-6 text-gray-700">
              Mettre une mise pour lancer le jeu
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Home
