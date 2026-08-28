# Vision-Based Chladni Pattern Analysis for Electric Motor Vibration Fault Diagnosis

A comprehensive multimodal electric motor vibration fault diagnosis system that uses computer vision and machine learning to analyze Chladni/vibration patterns from images, videos, and textual information.

## Features

- **Multimodal Input Support**: Upload images, videos, and text descriptions for comprehensive analysis
- **Chladni Pattern Analysis**: Advanced detection and analysis of vibration patterns and nodal lines
- **8 Fault Class Classification**: Healthy, Rotor Unbalance, Shaft Misalignment, Bearing Fault, Rotor Fault, Stator Fault, Mechanical Looseness, Coupling Fault
- **Severity Assessment**: Automatic severity estimation with confidence scores
- **Explainable AI**: Visual heatmaps and feature importance for transparent predictions
- **PDF Report Generation**: Professional diagnostic reports with recommendations
- **History Tracking**: Store and retrieve past diagnosis records
- **Demo Mode**: Fully functional prototype mode for demonstration

## Architecture

### Backend (Python + FastAPI)

```
backend/
├── main.py                 # FastAPI application entry point
├── api/
│   ├── diagnosis.py        # Diagnosis endpoints
│   ├── upload.py           # File upload endpoints
│   └── history.py          # History management endpoints
├── models/
│   ├── image_model.py      # Image-based classification
│   ├── video_model.py      # Video-based classification
│   ├── text_model.py       # Text-based classification
│   └── fusion_model.py     # Multimodal fusion model
├── preprocessing/
│   ├── image_processing.py # Image preprocessing pipeline
│   ├── video_processing.py # Video preprocessing pipeline
│   └── text_processing.py  # Text processing pipeline
├── features/
│   ├── pattern_features.py # Chladni pattern features
│   ├── visual_features.py  # General visual features
│   └── temporal_features.py # Temporal video features
├── explainability/
│   └── gradcam.py          # Grad-CAM and heatmap generation
├── database/
│   └── database.py         # SQLite database models
├── reports/
│   └── report_generator.py # PDF report generation
└── utils/
    ├── helpers.py          # Utility functions
    └── exceptions.py       # Custom exceptions
```

### Frontend (React + Tailwind CSS)

```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUploader.jsx
│   │   ├── VideoUploader.jsx
│   │   ├── TextInput.jsx
│   │   ├── ProcessingStatus.jsx
│   │   ├── FaultResult.jsx
│   │   ├── ProbabilityChart.jsx
│   │   ├── SeverityCard.jsx
│   │   └── ExplainabilityPanel.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Diagnosis.jsx
│   │   ├── Results.jsx
│   │   └── History.jsx
│   ├── services/
│   │   └── api.js          # API integration
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the project directory:
```bash
cd c:/Users/karis/OneDrive/Desktop/M.tech/Rakshita
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize directories:
```bash
python -c "from backend.utils.helpers import Config; Config.initialize_directories()"
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

```bash
# From project root
python backend/main.py
```

The backend will start on `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Start the Frontend

```bash
# From frontend directory
npm run dev
```

The frontend will start on `http://localhost:3000`

## Usage

### 1. Start Diagnosis

Navigate to the Diagnosis page and provide inputs:

- **Image**: Upload a vibration pattern image (JPG, PNG, BMP, TIFF)
- **Video**: Upload a motor vibration video (MP4, AVI, MOV, MKV)
- **Text**: Enter motor operating information (RPM, load, temperature, observations)

### 2. Motor Information

Optionally provide motor parameters:
- Motor ID
- Motor Type
- RPM
- Load (%)
- Temperature (°C)

### 3. Analysis

Click "Analyze Motor" to start the diagnosis process. The system will:

1. Validate inputs
2. Preprocess images/videos
3. Detect Chladni patterns
4. Extract visual and temporal features
5. Process textual information
6. Fuse multimodal features
7. Classify fault type
8. Estimate severity
9. Generate explainability visualizations
10. Create diagnostic report

### 4. View Results

The results page displays:
- Predicted fault with confidence
- Severity assessment
- Probability distribution chart
- Feature importance
- Explainability heatmap
- Processing steps

### 5. Download Report

Generate and download a professional PDF report containing:
- Motor information
- Input details
- Pattern analysis
- Diagnosis results
- Recommendations

### 6. View History

Access past diagnosis records from the History page.

## Fault Classes

The system classifies the following fault types:

1. **Healthy Motor** - No significant abnormal vibration
2. **Rotor Unbalance** - Uneven mass distribution in rotating assembly
3. **Shaft Misalignment** - Angular or parallel shaft misalignment
4. **Bearing Fault** - Inner/outer race, ball, or cage defects
5. **Rotor Fault** - Broken rotor bar, asymmetry, mechanical defects
6. **Stator Fault** - Winding abnormalities, inter-turn faults
7. **Mechanical Looseness** - Loose components, mounting issues
8. **Coupling Fault** - Coupling-related mechanical problems

## Demo Mode

The system operates in **Demo Mode** by default, which generates demonstration predictions for testing and prototyping. Demo Mode predictions are clearly labeled and should not be used for actual diagnostic decisions.

To use trained models:
1. Train models using experimental data
2. Save models to `backend/models/trained/`
3. Set `demo_mode: false` in diagnosis requests

## Training Models

### Dataset Structure

Organize your dataset as follows:

```
dataset/
├── healthy/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── unbalance/
├── misalignment/
├── bearing_fault/
├── rotor_fault/
├── stator_fault/
├── looseness/
└── coupling_fault/
```

### Training Process

Training functionality is available through the backend API. The system supports:

- Model selection (Random Forest, SVM, CNN)
- Train/validation/test split
- Hyperparameter configuration
- Performance metrics (Accuracy, Precision, Recall, F1-score)
- Confusion matrix and ROC curves

## API Endpoints

### Upload

- `POST /api/upload/image` - Upload image file
- `POST /api/upload/video` - Upload video file
- `DELETE /api/upload/{filename}` - Delete uploaded file

### Diagnosis

- `POST /api/diagnosis/analyze` - Perform fault diagnosis

### History

- `GET /api/history/` - Get diagnosis history
- `GET /api/history/{record_id}` - Get specific record
- `DELETE /api/history/{record_id}` - Delete record
- `GET /api/history/stats/summary` - Get statistics

## Technology Stack

### Backend
- **FastAPI** - Web framework
- **OpenCV** - Computer vision
- **scikit-learn** - Machine learning
- **PyTorch/TensorFlow** - Deep learning
- **SQLAlchemy** - Database ORM
- **ReportLab** - PDF generation

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Database
- **SQLite** (prototype) / **PostgreSQL** (production)

## Scientific Disclaimer

This system provides **model-based diagnostic assistance** based on pattern recognition. The fault-to-pattern relationship is learned and should be validated using experimental data.

**Important Notes:**
- Chladni patterns do not uniquely correspond to specific motor faults
- Final maintenance decisions should be confirmed using appropriate electrical, mechanical, and vibration measurements by qualified personnel
- Demo Mode predictions are for demonstration purposes only
- Model performance metrics should only be reported after proper validation with experimental data

## Security

- File type validation
- File size limits
- Secure temporary storage
- Filename sanitization
- No execution of uploaded files
- Automatic cleanup of temporary files

## Error Handling

The system handles:
- Unsupported file formats
- Corrupted images/videos
- Empty inputs
- Low-resolution images
- Large video files
- Missing models
- Processing timeouts

## Future Enhancements

- Real-time video streaming analysis
- Integration with IoT sensors
- Mobile application
- Advanced deep learning architectures (Vision Transformers, 3D CNNs)
- Multi-motor fleet management
- Predictive maintenance scheduling
- Cloud deployment options

## Deployment

### Production Build

#### Frontend Build
```bash
cd frontend
npm run build
```

The production build will be created in the `frontend/dist` directory.

### Deployment Options

#### Option 1: Vercel (Frontend) + Render/Railway (Backend)

**Frontend (Vercel):**
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel` from frontend directory
3. Set environment variables:
   - `VITE_API_URL`: Your backend URL

**Backend (Render/Railway):**
1. Push code to GitHub
2. Connect to Render/Railway
3. Set environment variables:
   - `PYTHON_VERSION`: 3.8+
   - `DATABASE_URL`: PostgreSQL connection string

#### Option 2: Docker Deployment

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", 8000]
```

Create `Dockerfile` for frontend:
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

Build and run:
```bash
docker-compose up -d
```

#### Option 3: Self-Hosted VPS

**Backend Setup:**
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Frontend Setup:**
```bash
# Build frontend
cd frontend
npm run build

# Serve with nginx
sudo cp -r dist/* /var/www/html/
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables

Create `.env` file in backend:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
UPLOAD_DIR=/path/to/uploads
MAX_IMAGE_SIZE=52428800
MAX_VIDEO_SIZE=524288000
DEMO_MODE=false
```

### Security for Production

1. **Enable CORS**: Configure allowed origins in FastAPI
2. **Add Authentication**: Implement JWT or OAuth2
3. **Use HTTPS**: Configure SSL certificates
4. **Rate Limiting**: Add rate limiting middleware
5. **Input Validation**: Strict validation of all inputs
6. **File Security**: Scan uploaded files for malware
7. **Database Security**: Use strong passwords and encryption

### Monitoring

- **Backend**: Add logging, error tracking (Sentry)
- **Frontend**: Add analytics, error monitoring
- **Health Checks**: Implement `/health` endpoint
- **Performance**: Monitor response times, memory usage

## License

This project is intended for academic and research purposes.

## Contact

For questions or support, please refer to the project documentation or contact the development team.

---

**Note**: This is a research prototype. Always validate predictions with appropriate engineering measurements before making maintenance decisions.
