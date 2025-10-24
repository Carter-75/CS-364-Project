## Project TODO

Environment
- [ ] Create `backend/.env` with:
  - FLASK_RUN_HOST=`0.0.0.0`
  - FLASK_RUN_PORT=`5000`
  - FLASK_DEBUG=`0`
  - FLASK_ENV=`production`
  - DB_HOST=`<your-db-host>`
  - DB_PORT=`3306`
  - DB_USER=`<your-db-user>`
  - DB_PASSWORD=`<your-db-password>`
  - DB_NAME=`<your-database>`
  - FRONTEND_ORIGIN=`<your-frontend-url>`  # e.g., `http://127.0.0.1:5500` if using Live Server, or `*` for quick local tests

- Install & Run (backend)
  - [ ] `cd backend`
  - [ ] Create venv: `python -m venv .venv`
  - [ ] Activate venv: `.venv\Scripts\activate` (Windows)
  - [ ] `pip install -r requirements.txt`
  - [ ] `waitress-serve --listen=0.0.0.0:5000 run:app`

- Verify API
  - [ ] Root health: open `http://127.0.0.1:5000/` → expect `{ "status": "ok" }`
  - [ ] API Health: open `http://127.0.0.1:5000/api/health` → expect `{ "status": "ok" }`
  - [ ] DB Ping: open `http://127.0.0.1:5000/api/db/ping`
    - Expect `{ "status": "ok" }` if credentials are valid
    - Otherwise `{ "status": "error", "error": "..." }`

- Frontend
  - [ ] `cd frontend`
  - [ ] Install Node deps: `npm install`
  - [ ] Start dev server: `npm run dev` (serves on `http://127.0.0.1:5173`)
  - [ ] Confirm the page shows API and Database status

- MySQL Checklist
  - [ ] Ensure MySQL server is running and accessible
  - [ ] Confirm user/password and DB exist
  - [ ] If needed, update `.env` with correct credentials

Notes
- Vite dev server proxies `/api/*` to Flask at `http://127.0.0.1:5000` per `frontend/vite.config.js`. Keep Flask running while using `npm run dev`.


