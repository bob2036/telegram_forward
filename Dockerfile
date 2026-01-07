FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du script
COPY tg_forward.py .

# Création du répertoire sessions
RUN mkdir -p /app/sessions

# Garder le container actif pour utilisation manuelle
CMD ["tail", "-f", "/dev/null"]