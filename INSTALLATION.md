# Installation Guide

## System Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: Minimum 2GB free space

## Step-by-Step Installation

### 1. Clone or Download the Project

Ensure you have the project files in:
```
c:/Users/karis/OneDrive/Desktop/M.tech/Rakshita
```

### 2. Backend Installation

#### 2.1 Create Virtual Environment

Open a terminal/command prompt and navigate to the project directory:

```bash
cd c:/Users/karis/OneDrive/Desktop/M.tech/Rakshita
```

Create a Python virtual environment:

```bash
python -m venv venv
```

#### 2.2 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

#### 2.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you encounter any installation errors, try:

```bash
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

#### 2.4 Initialize Directories

```bash
python -c "from backend.utils.helpers import Config; Config.initialize_directories()"
```

Or manually create the directories:

```bash
mkdir uploads\temp
mkdir uploads\heatmaps
mkdir reports
mkdir backend\models\trained
```

### 3. Frontend Installation

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node Dependencies

```bash
npm install
```

Or if you use yarn:

```bash
yarn install
```

### 4. Verify Installation

#### 4.1 Check Backend

```bash
cd c:/Users/karis/OneDrive/Desktop/M.tech/Rakshita
python -c "import fastapi; import cv2; import sklearn; print('Backend dependencies OK')"
```

#### 4.2 Check Frontend

```bash
cd frontend
npm --version
node --version
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd c:/Users/karis/OneDrive/Desktop/M.tech/Rakshita
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
python backend/main.py
```

Backend will start at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:3000`

## Troubleshooting

### Common Issues

#### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue: OpenCV installation fails

**Solution:**
```bash
pip install opencv-python-headless
```

#### Issue: Node modules installation fails

**Solution:**
```bash
npm cache clean --force
npm install
```

#### Issue: Port already in use

**Solution:**
- Change the port in `backend/main.py` (line ~65)
- Change the port in `frontend/vite.config.js` (line ~7)

#### Issue: CORS errors

**Solution:**
- Ensure backend is running before starting frontend
- Check CORS configuration in `backend/main.py`

#### Issue: File upload fails

**Solution:**
- Check file size limits in `backend/utils/helpers.py`
- Ensure upload directories exist and have write permissions

## Development Mode

For development with hot-reload:

### Backend
```bash
python backend/main.py
```
(FastAPI auto-reload is enabled by default)

### Frontend
```bash
npm run dev
```
(Vite hot-reload is enabled by default)

## Production Deployment

### Backend Production

1. Use a production ASGI server:
```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Use PostgreSQL instead of SQLite
3. Set up environment variables for sensitive configuration
4. Configure proper logging
5. Set up reverse proxy (nginx)

### Frontend Production

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Serve the `dist/` folder with nginx or similar

## Updating Dependencies

### Backend
```bash
pip list --outdated
pip install --upgrade <package-name>
pip freeze > requirements.txt
```

### Frontend
```bash
npm outdated
npm update <package-name>
```

## Uninstallation

To remove the application:

1. Deactivate virtual environment:
```bash
deactivate
```

2. Delete virtual environment:
```bash
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

3. Delete node_modules:
```bash
cd frontend
rm -rf node_modules
```

4. Delete generated files (optional):
```bash
rm -rf uploads/*
rm -rf reports/*
rm -rf backend/models/trained/*
rm -f *.db
```

## Support

For installation issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Ensure all prerequisites are met
4. Check Python and Node.js versions
