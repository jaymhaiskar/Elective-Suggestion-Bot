# Student Chatbot

A full-stack application for student course recommendations using AI. The project consists of a FastAPI backend and a React frontend.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** and **npm** (for frontend)

## Getting Started

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd chatbot_backend
   ```

2. **Create a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv

   # On macOS/Linux
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file in the `chatbot_backend` directory:**
   ```env
   FRONTEND_ORIGIN=http://localhost:5173
   # Add any other environment variables your application needs
   ```

6. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd chatbot_frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Project Structure

```
student_chatbot/
├── chatbot_backend/          # FastAPI backend
│   ├── controllers/          # API route handlers
│   ├── helpers/              # Utility functions
│   ├── main.py              # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
│
└── chatbot_frontend/         # React frontend
    ├── src/                 # Source files
    │   ├── api/             # API client
    │   └── ...
    ├── package.json         # Node.js dependencies
    └── vite.config.js       # Vite configuration
```

## Available Scripts

### Backend
- Run server: `uvicorn main:app --reload`
- Run with custom port: `uvicorn main:app --reload --port 8000`

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Development

- The backend runs on `http://localhost:8000` by default
- The frontend runs on `http://localhost:5173` by default
- CORS is configured to allow requests from the frontend origin
- The backend API documentation is available at `/docs` when the server is running

## Troubleshooting

### Backend Issues
- **Module not found errors**: Make sure your virtual environment is activated and dependencies are installed
- **Port already in use**: Change the port using `--port` flag or stop the process using the port
- **Environment variables not loading**: Ensure `.env` file exists in `chatbot_backend` directory

### Frontend Issues
- **Dependencies not installing**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
- **Port conflicts**: Vite will automatically try the next available port if 5173 is in use

## Notes

- Make sure both backend and frontend servers are running simultaneously for the full application to work
- The backend uses FastAPI with automatic API documentation
- The frontend uses React with Vite for fast development and Tailwind CSS for styling

