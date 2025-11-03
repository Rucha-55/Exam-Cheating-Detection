# Exam-Cheating-Detection
## Mini Project Report

**Institution:** K. K. Wagh Institute of Engineering Education & Research / Polytechnic, Nashik

---

## 1. Abstract

This project presents **FlexiCare – Intelligent Posture Correction System**, a web-based posture correction system that uses computer vision and deep learning to analyze body posture in real-time. Using a webcam and mediapipe pose estimation, it detects body landmarks and provides instant visual and textual feedback to help users maintain correct posture. The system is lightweight, user-friendly, and deployable online.

---

## 2. Objectives

- **Detect human posture** using pose estimation techniques
- **Provide real-time feedback** for corrected posture
- **Develop a web-based, easy-to-use application**

---

## 3. Technologies and Tools

### Backend
- **Language:** Python
- **Framework:** Flask

### Frontend
- **Technologies:** HTML, CSS, JavaScript

### Libraries
- **Computer Vision:** MediaPipe, OpenCV
- **Deep Learning:** NumPy

### Deployment
- **Framework:** Gunicorn, Render

---

## 4. System Overview

**How it Works:**
- User's webcam captures real-time video
- MediaPipe detects keypoints of the body
- The system checks the alignment and posture against correct posture criteria
- Feedback is displayed on the browser with the detected posture

---

## 5. Key Features

- Real-time posture detection using pose estimation
- Instant visual and textual feedback
- Web-based interface for easy accessibility
- Lightweight and user-friendly design
- Deployable online

---

## 6. Implementation Details

### System Architecture
1. **Frontend (Web Interface):**
   - HTML/CSS for UI layout
   - JavaScript for interactivity
   - Webcam integration

2. **Backend (Server):**
   - Flask application handles requests
   - MediaPipe processes pose data
   - OpenCV handles video frame processing

3. **Processing Pipeline:**
   - Capture frame from webcam
   - Extract body keypoints using MediaPipe
   - Analyze keypoint positions for posture correctness
   - Generate feedback (visual + textual)
   - Display on browser in real-time

---

## 7. Results and Output

- **Real-time Detection:** Successfully detects and classifies posture correctness
- **Feedback Accuracy:** Provides accurate visual indicators and guidance
- **User Experience:** Clean, intuitive interface with minimal latency
- **Performance:** Efficient on standard hardware with web deployment capability

---

## 8. Advantages

- ✓ Uses advanced pose estimation for accuracy
- ✓ Accessible via web browser (no installation required)
- ✓ Real-time feedback for immediate user response
- ✓ Lightweight and efficient algorithm
- ✓ Scalable and deployable on cloud platforms

---

## 9. Applications

- **Healthcare & Wellness:** Posture monitoring in physical therapy
- **Office Ergonomics:** Workplace posture correction
- **Fitness Training:** Real-time form correction during exercises
- **Education:** Student posture monitoring in classrooms

---

## 10. Limitations & Future Scope

### Current Limitations
- Requires webcam and adequate lighting
- Works best in controlled environments
- Single-person detection per session

### Future Enhancements
- Multi-person posture detection
- Improved accuracy with custom ML models
- Mobile app development
- Integration with wearable devices
- Advanced analytics and posture history tracking

---

## 11. Conclusion

The **FlexiCare – Intelligent Posture Correction System** successfully demonstrates the application of computer vision and pose estimation in real-world posture monitoring. The system is effective, user-friendly, and has significant potential for deployment in healthcare, fitness, and workplace ergonomics sectors.

---

## 12. References

- MediaPipe Documentation: https://mediapipe.dev
- OpenCV Documentation: https://docs.opencv.org
- Flask Documentation: https://flask.palletsprojects.com
- NumPy Documentation: https://numpy.org

---

**Project Status:** ✅ Completed and Deployed

**Repository:** [Exam-Cheating-Detection](https://github.com/Rucha-55/Exam-Cheating-Detection)

**Last Updated:** November 2025

