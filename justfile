# Charge automatiquement les variables du fichier .env s'il existe
set dotenv-load := true

# On veut un shell moderne
set shell := ["bash", "-c"]

default:
    just --list

run:
    uv run uvicorn app.main:app --no-access-log

run-dev:
    uv run uvicorn app.main:app --reload --no-access-log

test:
    uv run pytest -v

migrate:
    uv run alembic upgrade head

ruff *args:
    uv run ruff check {{args}} app tests migrations

lint:
    uv run ruff format app tests migrations
    just ruff --fix

sort:
    uv run isort .

build:
    echo "INFO - Construction de l'image..."
    podman build -t "${IMAGE_NAME}" .

create:
    # Vérifier .env
    if [[ ! -f .env ]]; then \
      echo "ERROR - Fichier .env manquant !"; \
      exit 1; \
    fi

    # Créer réseau et volume si nécessaire
    echo "INFO - Création du volume et du réseau nécessaires au pod..."
    podman network exists "${NETWORK_NAME}" || podman network create "${NETWORK_NAME}"

    # Créer le pod
    echo "INFO - Création du pod..."
    podman pod create \
        --name "${POD_NAME}" \
        -p "${PORT}:8000" \
        --net "${NETWORK_NAME}"

    # Démarrer le conteneur FastAPI
    echo "INFO - Démarrage du conteneur sur le port spécifié..."
    podman run -d --pod "${POD_NAME}" \
        --name "${CONTAINER_NAME}" \
        --env-file .env \
        "${IMAGE_NAME}"

start:
    echo "INFO - Démarrage du conteneur sur le port spécifié..."
    podman pod start "${POD_NAME}"

stop:
    echo "INFO - Arrêt du conteneur..."
    podman pod stop "${POD_NAME}" 2>/dev/null || true

clean:
    echo "INFO - Demande de suppression du pod..."
    podman pod rm -f "${POD_NAME}" 2>/dev/null || true

logs:
    podman logs -f "${CONTAINER_NAME}"