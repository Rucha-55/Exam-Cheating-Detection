# Exam Cheating Detection System

A real-time AI-powered exam integrity monitoring system using computer vision and deep learning.

## What's Included
- **Backend:** Flask server with real-time pose and face detection
- **Frontend:** Modern HTML/CSS/JavaScript interface with live video streaming
- **Model:** Pre-trained PyTorch model for cheating detection
- **Features:** 
  - Real-time webcam monitoring
  - Head posture analysis
  - Multi-person detection
  - Alert system with severity levels
  - Session recording and reporting

## Project Structure
```
.
├── app.py                          # Flask backend application
├── requirements.txt                # Python dependencies
├── cheating_model_best.pt         # Trained model (ignored by .gitignore)
├── cheating_model.ipynb           # Jupyter notebook for training/analysis
├── templates/
│   ├── index.html                 # Home page
│   └── camera.html                # Detection interface
├── static/
│   ├── style.css                  # Responsive styling
│   └── script.js                  # Frontend JavaScript
├── runs/                          # Detection outputs (ignored)
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+ 
- pip (Python package manager)
- Webcam (for live detection)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Rucha-55/Exam-Cheating-Detection.git
cd Exam-Cheating-Detection
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Place Model File
Ensure `cheating_model_best.pt` is in the project root directory. If not training from scratch:
- Train a model using `cheating_model.ipynb` or
- Download a pre-trained model and place it in the root folder

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The application will be available at:
- **Home:** http://localhost:5000/
- **Detection:** http://localhost:5000/camera

### Using the Detection Interface
1. Navigate to http://localhost:5000/camera
2. Click **Start** to begin monitoring
3. The system will:
   - Stream live webcam feed
   - Analyze posture and head position
   - Display cheating score and alerts
   - Show detected indicators in real-time
4. Click **Stop** to end monitoring
5. Click **Save Report** to export results

## Features & Capabilities

### Detection Indicators
- ✅ Head tilt detection
- ✅ Looking down/away detection
- ✅ Abnormal posture detection
- ✅ Hand visibility tracking
- ✅ Multiple person detection
- ✅ Real-time scoring (0.0 - 1.0)

### Alert Levels
- 🟢 **SAFE** (Score < 0.4): Normal behavior
- 🟠 **WARNING** (Score 0.4 - 0.7): Suspicious activity
- 🔴 **CRITICAL** (Score > 0.7): High probability of cheating

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/camera` | GET | Detection interface |
| `/video_feed` | GET | MJPEG video stream |
| `/get_results` | GET | Current detection results |
| `/api/results` | POST | Save detection results |
| `/health` | GET | Health check |

## Configuration

### Adjusting Detection Sensitivity
Edit thresholds in `app.py`:
```python
# Lines ~60-90 in analyze_cheating_indicators()
if eye_angle > 0.05:  # Adjust this value to change head tilt sensitivity
if nose.y > 0.6:      # Adjust for looking down sensitivity
if shoulder_diff > 0.1:  # Adjust for posture sensitivity
```

### Output Files
- `detection_results.json` - Saved detection sessions
- Browser console logs - Real-time debug information

## Troubleshooting

### Webcam Not Working
- Check if camera is connected and not in use by another application
- Ensure permissions are granted to Python/Flask
- Try: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Model Loading Error
- Verify `cheating_model_best.pt` exists in the root directory
- Check PyTorch installation: `python -c "import torch; print(torch.__version__)"`

### High CPU Usage
- Reduce video resolution in `app.py` line ~45
- Decrease model complexity in `app.py` line ~56

## Training Your Own Model

Use `cheating_model.ipynb` to:
1. Prepare training data
2. Define and train the model
3. Evaluate performance
4. Export as `.pt` file

## Technologies Used

- **Backend:** Flask, Python
- **Computer Vision:** OpenCV, MediaPipe
- **Deep Learning:** PyTorch
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data Processing:** NumPy, scikit-learn

## Future Enhancements

- [ ] Multi-user concurrent monitoring
- [ ] Cloud deployment (AWS/GCP)
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Integration with Learning Management Systems
- [ ] Real-time notifications
- [ ] Historical data visualization

## License

This project is open source and available under the MIT License.

## Contact & Support

For issues, questions, or contributions:
- Create an Issue on GitHub
- Submit a Pull Request
- Email: exam-detection@example.com

---

**Last Updated:** November 2025  
**Version:** 1.0.0
- 🟠 **WARNING** (Score 0.4 - 0.7): Suspicious activity
- 🔴 **CRITICAL** (Score > 0.7): High probability of cheating
