# MediaWatchList

## Purpose
MediaWatchList is a full-stack web application designed to track and manage personal media consumption across various entertainment types (Movies, Shows, Books, Games). It allows users to log entries, rate content, and perform advanced analytical queries to discover trends in their viewing habits.

## Architecture
The project follows a modular full-stack architecture:

### Frontend
- **Framework**: React (Vite)
- **Styling**: Custom CSS with Dark Theme (CSS Variables, Grid/Flexbox)
- **Communication**: REST API via `fetch` (proxied to backend in dev)
- **Structure**:
  - `src/components`: Reusable UI components (e.g., `QueryResults`)
  - `src/App.jsx`: Main application logic and state management

### Backend
- **Runtime**: Python 3.10+
- **Framework**: Flask
- **Database**: MySQL 8.0+
- **Security**:
  - Parameterized SQL queries (prevention of SQL Injection)
  - Environment-based configuration (Secrets management)
  - Input validation and sanitization
- **Layers**:
  - **Routes** (`routes.py`): Handles HTTP requests, validation, and response formatting.
  - **Data Access** (`db.py`): Manages database connections, transactions, and SQL execution.

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- MySQL Server running locally or accessible via network

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure Environment:
   - Create a `.env` file in `backend/` with the following:
     ```env
     DB_HOST=localhost
     DB_PORT=3306
     DB_USER=your_user
     DB_PASSWORD=your_password
     DB_NAME=mediawatchlist
     ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

### Running the Application (Cross-Platform)
We provide a unified startup script that handles both backend and frontend:

```bash
# From the project root
python start_app.py
```

### Manual Startup
**Backend:**
```bash
cd backend
python run.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```
Access the application at `http://localhost:5173`.

## Testing
Run the backend test suite to verify API and Database logic:

```bash
cd backend
python -m unittest discover tests
```

## Environment Configuration
| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database Hostname | `localhost` |
| `DB_PORT` | Database Port | `3306` |
| `DB_USER` | Database Username | `root` |
| `DB_PASSWORD` | Database Password | *None* |
| `DB_NAME` | Database Name | `mediawatchlist` |

## Security & Best Practices
- **Input Validation**: All API endpoints validate required fields and data types.
- **SQL Safety**: All database interactions use parameterized queries to prevent SQL injection.
- **Error Handling**: Centralized error logging and safe client-facing error messages.

