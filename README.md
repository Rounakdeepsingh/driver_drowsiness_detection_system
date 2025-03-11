🚗 Driver Drowsiness Detection

🌟 Overview

Driver drowsiness detection is a crucial technology that helps prevent road accidents caused by fatigue. This project utilizes advanced computer vision techniques to monitor a driver's eye state and sound an alarm if signs of drowsiness are detected.

✨ Features

✅ Real-time face and eye detection using OpenCV's Haar cascades.✅ Continuous monitoring of the driver's eye state.✅ Audio alert system to wake up the driver when drowsiness is detected.

📂 Project Structure

Driver_Drowsiness_Detection/
├── 📢 alarm.wav                      # Alert sound file for drowsiness detection
├── 👀 haarcascade_eye.xml            # Haar cascade model for eye detection
├── 😀 haarcascade_frontalface_default.xml # Haar cascade model for face detection
└── 🖥 monitoring.py                   # Main script for drowsiness detection

📌 Requirements

Ensure you have the following dependencies installed before running the project:

🐍 Python 3.x

📷 OpenCV (cv2)

🔢 NumPy

🔊 Pygame (for playing the alarm sound)

Install the dependencies using:

pip install opencv-python numpy pygame

🚀 Usage

1️⃣ Run the script:

python monitoring.py

2️⃣ The webcam will start detecting the driver's face and eyes.3️⃣ If drowsiness is detected, an alarm sound (alarm.wav) will play to alert the driver.

🔮 Future Improvements

🚀 Implement deep learning-based eye state classification for better accuracy.⚡ Optimize performance for low-power devices.🧵 Add support for multi-threading to enhance real-time processing.

📜 License

This project is open-source and available under the MIT License.

🙌 Acknowledgments

❤️ OpenCV for providing pre-trained Haar cascade models.

🌍 The open-source community for contributions to drowsiness detection research.

