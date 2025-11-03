# Quick Start Guide - Exam Cheating Detection System

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2. Run the Application (30 sec)
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 3. Open in Browser (30 sec)
Visit: **http://localhost:5000**

You'll see the home page with navigation to the detection system.

---

## 📱 Using the Detection Interface

### Home Page Features
- ✨ Overview of the system
- 🎯 Key features and capabilities
- 📊 How it works (4-step process)
- 🚀 Call-to-action to start detection

### Camera/Detection Page
1. **Start Monitoring:** Click the **Start** button
2. **Watch Real-time Stream:** See your webcam feed with pose detection overlay
3. **Monitor Scores:** 
   - Cheating Score: 0.0 to 1.0
   - Status: SAFE / WARNING / CRITICAL
4. **View Alerts:** Detected suspicious indicators appear in real-time
5. **Stop & Save:** Click Stop, then Save Report

---

## 🔧 Configuration

### Change Detection Sensitivity
Edit `app.py` lines 65-85:

```python
# More strict (catches more false positives)
if eye_angle > 0.03:  # was 0.05
if nose.y > 0.55:     # was 0.6

# Less strict (fewer alerts)
if eye_angle > 0.08:  # was 0.05
if nose.y > 0.7:      # was 0.6
```

### Reduce System Load
In `app.py` line 45:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # was 640
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # was 480
```

---

## 🎯 Detection Indicators Explained

| Indicator | What it detects | Score Impact |
|-----------|-----------------|--------------|
| **Head tilt** | Head not aligned vertically | +0.15 |
| **Looking down/away** | Nose Y-position too low | +0.20 |
| **Abnormal posture** | Shoulders misaligned | +0.15 |
| **Hands visible** | Hand detection in frame | +0.10 per hand |
| **Multiple people** | >1 face detected | +0.25 |

---

## 🐛 Troubleshooting

### "Error loading video stream"
- [ ] Check webcam is plugged in and working
- [ ] Close any other app using the camera
- [ ] Try: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`

### Flask won't start
- [ ] Check port 5000 is free: `netstat -ano | findstr :5000`
- [ ] Try a different port: `app.run(port=5001)`
- [ ] Reinstall Flask: `pip install --upgrade Flask`

### Model not loading
- [ ] Verify `cheating_model_best.pt` exists in project root
- [ ] Check you have enough disk space (~500MB)
- [ ] The app will work even without model (basic detection only)

### Slow performance
- [ ] Lower video resolution in `app.py`
- [ ] Close other applications
- [ ] Use `model_complexity=0` in `app.py` line 58

---

## 📊 Data & Results

### Saving Results
Click **Save Report** to export session data to `detection_results.json`

### Result Format
```json
{
  "timestamp": "2025-11-03T22:30:00",
  "duration": "00:05:42",
  "final_score": 0.35,
  "status": "🟢 SAFE",
  "total_frames": 342
}
```

---

## 🔒 Privacy & Security

- ✅ All processing happens locally
- ✅ No data sent to external servers
- ✅ Results saved only if you click Save
- ✅ Can run completely offline

---

## 📚 File Structure
```
project/
├── app.py                    ← Flask backend (main file)
├── requirements.txt          ← Dependencies
├── cheating_model_best.pt   ← AI model
├── templates/
│   ├── index.html           ← Home page
│   └── camera.html          ← Detection interface
├── static/
│   ├── style.css            ← Styling
│   └── script.js            ← Frontend logic
└── detection_results.json   ← Saved results (auto-created)
```

---

## ⚡ Performance Tips

| Tip | Benefit | How-to |
|-----|---------|--------|
| Lower resolution | Faster FPS | Change line 45-46 in `app.py` |
| Simple model | Less CPU | Change `model_complexity` to 0 |
| Close apps | More resources | Close background programs |
| Use wired connection | Better stability | WiFi → Ethernet |

---

## 🎓 Next Steps

1. **Test the system** - Run detection on sample videos
2. **Adjust thresholds** - Fine-tune for your environment
3. **Deploy online** - Use Heroku or AWS
4. **Train custom model** - Use `cheating_model.ipynb`

---

## 📞 Support

- **Issues?** Check GitHub issues
- **Questions?** Create a discussion
- **Bugs?** Submit with screenshots

---

**Happy Monitoring! 🎯**
