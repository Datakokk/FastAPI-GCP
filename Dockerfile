# Utiliza imagen oficial de python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente
COPY . .

# Expone el puerto (FastAPI)
EXPOSE 8000

# Comando para correr la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
