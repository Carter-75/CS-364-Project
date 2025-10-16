## Project TODO

**Environment**
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
  - FRONTEND_ORIGIN=`<your-frontend-url>`  # e.g., `http://localhost:3000` for local dev

- **Install & Run (backend)**
  - [ ] `cd backend`
  - [ ] Create venv: `python -m venv .venv`
  - [ ] Activate venv: `.venv\\Scripts\\activate` (Windows)
  - [ ] `pip install -r requirements.txt`
  - [ ] `waitress-serve --listen=0.0.0.0:5000 run:app`

- **Verify API**
  - [ ] Root health: open `http://127.0.0.1:5000/` → expect `{ "status": "ok" }`
  - [ ] API Health: open `http://127.0.0.1:5000/api/health` → expect `{ "status": "ok" }`
  - [ ] DB Ping: open `http://127.0.0.1:5000/api/db/ping`
    - Expect `{ "status": "ok" }` if credentials are valid
    - Otherwise `{ "status": "error", "error": "..." }`

- **Frontend**
  - [ ] Open `frontend/index.html` in browser
  - [ ] Confirm the page shows `Backend: ok`

- **MySQL Checklist**
  - [ ] Ensure MySQL server is running and accessible
  - [ ] Confirm user/password and DB exist
  - [ ] If needed, update `.env` with correct credentials

- **Next (optional, later)**
  - [ ] Add CRUD endpoints with MySQL queries
  - [ ] Add simple UI form that calls new endpoints


