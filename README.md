# Coach MediaPipe — Veille techno

Petite app webcam qui detecte 3 exercices avec MediaPipe Pose + OpenCV:

- **Jumping jack** — bras en l'air + jambes ecartees (cycle haut/bas)
- **Shadowboxing** — coude qui passe de plie a tendu (chaque poing compte)
- **Push-up** — torse horizontal, coude qui cycle plie/tendu

L'app cycle les 3 exercices, te dit quoi faire a l'ecran, compte les reps, et passe au suivant quand tu atteins la cible (5 par defaut).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer

```bash
python main.py
```

**macOS:** la premiere execution demande la permission camera a Terminal/iTerm.

## Controles

- `q` ou `Esc` — quitter
- `Espace` — passer a l'exercice suivant

## Architecture

| Fichier        | Role                                                |
|----------------|-----------------------------------------------------|
| `main.py`      | Boucle principale, orchestre la sequence            |
| `pose.py`      | Wrapper MediaPipe Pose — 33 landmarks -> pixels     |
| `geometry.py`  | Helpers math (angle articulaire, distance)          |
| `exercises.py` | Detecteurs rule-based (state machine par exercice)  |
| `ui.py`        | Overlay OpenCV (texte, compteur, feedback)          |

## Comment ca marche

Chaque detecteur lit les landmarks MediaPipe et applique des seuils geometriques:

- **Jumping jack** — compare la position verticale des poignets vs epaules (`arms_up`) et l'ecart des chevilles vs hanches (`legs_apart`). Une rep = cycle `down -> up -> down`.
- **Shadowboxing** — calcule l'angle du coude (epaule-coude-poignet). Chaque transition `plie (<110 deg) -> tendu (>155 deg)` compte 1 rep, gauche et droite independants.
- **Push-up** — verifie que torse est horizontal (dx shoulders-hips > dy), puis cycle sur l'angle du coude `up -> down -> up`.

## Ajuster

Seuils dans `exercises.py` (ex. `sw * 0.3` pour "bras au-dessus epaules", `155 deg` pour coude tendu). Nombre de reps cible dans `main.py` (`TARGET_REPS = 5`).
