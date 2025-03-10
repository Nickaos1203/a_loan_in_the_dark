FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances pour pyodbc
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    g++ \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Installation du pilote ODBC pour SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# Commande de démarrage pour le port 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]