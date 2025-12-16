## MVP TocToc Precios

Aplicación MVP para visualizar productos y sus precios en varias cadenas, y un índice diario de precios.

### Requisitos previos

- **Python**: 3.12.10 o superior
- **Node.js**: v22.17.1 o superior (incluye npm)

### Backend (FastAPI)

- Ir a `backend/`
- Crear un entorno virtual (opcional) e instalar dependencias:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- El backend expone:
  - `POST /auth/login-json` – login con JSON.
  - `GET /auth/me` – usuario actual.
  - `GET /products` – listado de productos con precios por cadena.
  - `GET /products/{id}` – detalle + histórico.
  - `GET /indices/daily` – índice diario (promedio de precios).

Se crea automáticamente un usuario demo en el arranque:

- **email**: `demo@toctoc.local`
- **password**: `demo1234`

### Frontend (Vite + React + TS)

- Ir a `frontend/`
- Instalar dependencias (si aún no):

```bash
npm install
npm run dev
```

- Configurar (opcional) `VITE_API_BASE_URL` en un archivo `.env` dentro de `frontend/` si el backend no corre en `http://localhost:8000`.

El flujo base:

1. Login con el usuario demo.
2. Pantalla de **Productos**: filtros básicos por fecha y búsqueda, tabla con precios por cadena.
3. Pantalla de **Índice diario**: lista de puntos `{fecha, índice}`.
4. **Detalle de producto**: al hacer clic en un producto, se ve su histórico de precios por cadena.



