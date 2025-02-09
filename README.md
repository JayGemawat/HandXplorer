# HandXplorer - Virtual Mouse Using Hand Gestures

## 📌 Introduction
HandXplorer is a **virtual mouse application** that enables users to control their cursor using **hand gestures**. Built with **OpenCV, MediaPipe, PyAutoGUI, and Flask**, it leverages computer vision to track hand movements and translate them into mouse actions.

## 🚀 Features
- **Move Cursor** – Control your mouse pointer by moving your hand.
- **Left Click** – Pinch your **thumb & index finger**.
- **Right Click** – Pinch your **thumb, index, & middle finger**.
- **Double Click** – Close your fingers together.
- **Web-Based UI** – Simple interface to start and view the video stream.
- **Smooth Tracking** – Uses filtering for smoother cursor movement.

## 🛠️ Installation Guide
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/JayGemawat/HandXplorer.git
cd HandXplorer
```

### **2️⃣ Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Application**
```bash
python app.py
```

### **5️⃣ Open the Web UI**
Once running, open your browser and go to:
```
http://127.0.0.1:5000/
```

## 🖥️ Deployment on Render
1. **Push your project to GitHub**
2. **Create a new Web Service on [Render](https://render.com/)**
3. **Set Runtime:** Python 3.x
4. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Start Command:**
   ```bash
   gunicorn app:app
   ```
6. **Deploy & Get Live URL**

## 🔧 Troubleshooting
- **Camera Not Working?** Ensure Python has access to your webcam.
- **Cursor Too Fast?** Adjust `smooth_factor` in `app.py`.
- **Error with Flask UI?** Ensure `index.html` is inside the `templates/` folder.

## 🤝 Contributing
Feel free to fork this repository, submit issues, and contribute with pull requests!

## 📜 License
This project is licensed under the **MIT License**.

