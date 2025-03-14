FROM python:3.12-slim

WORKDIR /app

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

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]