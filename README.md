# Socle FastAPI - Simple et Efficace

## 📁 Structure minimaliste

```
socle_fastapi/
├── Dockerfile
├── uv.lock
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── app/
|   ├── core/
|   |   ├── __init__.py
|   |   └── config.py
|   └── main.py
└── justfile
```

# FastAPI Service

Template FastAPI Python 3.12 slim pour micro-services avec Podman.

## Installation

```bash
git clone https://github.com/thedasken/socle_fastapi.git mon_service
cd mon_service
rm -rf .git
```

---

## 🚀 Installation en 30 secondes

```bash
# 1. Créer .env
cp .env.example .env

# 2. GO!
just build
just run
```

---

## Utilisation

```bash
just run        # Démarrer en local
just run-dev    # Démarrer en local en mode dev (hot reload)
just build      # Construire l'image
just start      # Démarrer le pod
just stop       # Arrêter le pod
just clean      # Supprimer le pod
just logs       # Voir les logs
just cli        # Se connecter au conteneur
```

## Configuration

Modifiez `.env` pour changer les credentials et noms de base.

## Démarrage (données d'exemple, à modifier en fonction de votre configuration)

- **Host:** `127.0.0.1` (le réseau `network_name` mappe les ports des pods sur la machine grâce au bridge, à désactiver en production suivant les besoins)
- **Port:** `8000`