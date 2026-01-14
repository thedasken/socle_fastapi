# FastAPI Microservice Template (v2.1.0)

Template moderne, minimaliste et orienté production pour l'architecture microservices. 
Priorité à la sécurité, aux bonnes pratiques (SQL-first) et à l'observabilité.

## Stack Technique

* **Runtime**: Python 3.12 (Image slim)
* **Package Manager**: `uv`
* **Database**: PostgreSQL 17 (Image alpine) + SQLAlchemy (Async)
* **Migrations**: Alembic (Async workflow)
* **Observabilité**: OpenTelemetry (Traces) + Prometheus (Metrics)
* **Qualité**: Ruff + Pytest (Async ready)

---

## Démarrage Rapide

```bash
# Pré-requis : 'just' installé
# Debian / Ubuntu : sudo apt install just
# RHEL / AlmaLinux / Fedora : sudo dnf install just

# 1. Préparer l'environnement
cp .env.example .env

# 2. Installer les dépendances
uv sync

# 3. Lancer les migrations
uv run alembic upgrade head
# ou
# just migrate

# 4. Seeder la base (optionnel)
uv run scripts/seed_db.py

# 5. Démarrer
just run
```

---

## Structure du Projet

L'architecture suit les recommandations *FastAPI Best Practices* (Domain-driven) :

```text
app/
├── core/               # Config globale, Database engine, Logging, OTEL
├── api/
│   ├── routes/         # Endpoints par domaine
│   ├── repositories/   # Logique SQL pure (Pattern Repository)
│   ├── middlewares/    # Logging (RID/TraceID correlation)
├── schemas/            # Modèles Pydantic (CustomModel ISO-GMT)
├── models/             # Modèles SQLAlchemy
└── main.py             # Point d'entrée & Instrumentation
```

---

## Observabilité & Télémétrie

Le socle inclut une corrélation native entre Logs et Traces :

* **RID (Request ID)** : Identifiant unique par requête HTTP.
* **Trace ID** : Identifiant OpenTelemetry propagé dans les logs.
* **Metrics** : Disponibles sur `/metrics` (Format Prometheus).

---

## Gestion des Données

* **UUID v4** : Utilisé comme clé primaire pour l'indépendance en microservices.
* **Transactions** : Gestion via `async with transaction():` (Commit/Rollback auto).
* **Resilience** : Retries automatiques via `tenacity` sur les erreurs de connexion DB.
* **Naming Convention** : Contraintes DB explicites (`uq_table_column`).

---

## Commandes Utiles (Justfile)

```bash
just run        # Démarrer le serveur uvicorn
just run-dev    # Serveur avec --reload
just test       # Lancer la suite Pytest
just migrate    # Appliquer les migrations Alembic

```

---

## Sécurité

* Documentation API (`/docs`) désactivée en production.
* Validation stricte des entrées/sorties via Pydantic.
* Images Docker non-root (voir Dockerfile).