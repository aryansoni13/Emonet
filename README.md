# 🎭 Real-Time Face Emotion Avatar

A sophisticated real-time emotion detection and avatar visualization system that uses MediaPipe to track facial expressions and displays them as animated avatars. Available as both a desktop application and a web application.

## ✨ Features

- **Real-time Emotion Detection**: Detects 7 different emotions (happy, sad, angry, surprise, neutral, fear, disgust)
- **Multiple Avatar Styles**: Choose between mesh, points, or minimal visualization styles
- **Enhanced UI**: Beautiful interface with emotion descriptions and confidence scores
- **Screenshot Capability**: Capture moments with built-in screenshot functionality
- **Debug Mode**: Toggle debug information for development and tuning
- **Performance Tracking**: Real-time FPS monitoring and optimization
- **Error Handling**: Robust error handling for better user experience
- **🌐 Web Version**: Full web application with modern UI and mobile support
- **📱 Mobile Responsive**: Works perfectly on all devices and screen sizes

## 🚀 Quick Start

### Desktop Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run desktop app
python avatar.py
```

### Web Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run web server
python app.py

# Open browser to http://localhost:5000
```

## 🌐 Web Deployment

The web version can be easily deployed to various hosting platforms:

### Quick Deploy Options:
- **Heroku**: [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/Real_Time_Face_Emotion_Avatar)
- **Railway**: Connect your GitHub repo and deploy automatically
- **Render**: Free hosting with automatic deployments
- **DigitalOcean**: App Platform with easy scaling

### Manual Deployment:
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🎮 Controls

### Desktop App
| Key | Action |
|-----|--------|
| `ESC` | Quit application |
| `S` | Take screenshot |
| `D` | Toggle debug mode |
| `A` | Cycle through avatar styles |

### Web App
- **Start Camera**: Click "Start Camera" button
- **Capture**: Click "Capture" to save current frame
- **Stop**: Click "Stop Camera" to end session

## 🎨 Avatar Styles

- **Mesh**: Full facial mesh with detailed landmarks
- **Points**: Minimal point-based visualization
- **Minimal**: Clean contour-based outline

## 📊 Emotion Detection

The system analyzes various facial features to detect emotions:

- **Happy**: Wide smile with closed eyes
- **Sad**: Drooping eyes with iris positioned lower
- **Angry**: Narrowed eyes with furrowed brows
- **Surprise**: Wide open mouth
- **Fear**: Slightly open mouth with raised eyebrows
- **Disgust**: Tight mouth with wrinkled features
- **Neutral**: Default calm state

## 📁 Project Structure

```
Real_Time_Face_Emotion_Avatar/
├── avatar.py          # Desktop application
├── app.py            # Web application (Flask)
├── templates/        # HTML templates
│   └── index.html    # Main web interface
├── static/           # Static files
│   ├── css/         # Stylesheets
│   └── js/          # JavaScript files
├── config.py         # Configuration settings
├── requirements.txt  # Python dependencies
├── Procfile         # Heroku deployment
├── runtime.txt      # Python version
├── Aptfile          # System dependencies
├── DEPLOYMENT.md    # Deployment guide
└── README.md        # Project documentation
```

## 🔧 Technical Details

- **Face Detection**: MediaPipe Face Mesh for precise facial landmark detection
- **Emotion Analysis**: Custom algorithm based on facial feature ratios
- **Real-time Processing**: Optimized for 30 FPS performance
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Web Framework**: Flask for backend API
- **Frontend**: Modern HTML5, CSS3, and JavaScript
- **Mobile Support**: Responsive design for all devices

## 🎯 Usage Examples

### Desktop Usage
```bash
python avatar.py
```

### Web Usage
1. Start the server: `python app.py`
2. Open browser to `http://localhost:5000`
3. Click "Start Camera" and allow camera access
4. Watch your emotions detected in real-time!

### Development Mode
1. Run the application
2. Press `D` to enable debug mode (desktop)
3. Watch console output for feature analysis

## 🛠️ Customization

### Adjusting Emotion Sensitivity
Modify the threshold values in the `get_emotion()` method to fine-tune emotion detection:

```python
# Example: Make happiness detection more sensitive
if features['mouth_stretch'] > 0.35:  # Lowered from 0.40
    emotion_scores['happy'] = min(1.0, features['mouth_stretch'] * 2)
```

### Adding New Emotions
1. Add emotion definition to `self.emotions` dictionary
2. Implement detection logic in `get_emotion()` method
3. Add corresponding emoji and color

## 📸 Screenshots

The application creates side-by-side screenshots showing both the webcam feed and the emotion avatar visualization.

## 🌐 Live Demo

Try the web version online: [Your deployed URL here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- MediaPipe team for the excellent face mesh solution
- OpenCV community for computer vision tools
- Flask community for the web framework
- All contributors and users of this project

## 🐛 Troubleshooting

### Common Issues

1. **Webcam not detected**: Ensure your webcam is connected and not in use by other applications
2. **Low FPS**: Try reducing camera resolution or closing other applications
3. **Installation errors**: Make sure you have Python 3.7+ and pip installed
4. **Web deployment issues**: Check [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific solutions

### Performance Tips

- Use a good webcam for better detection accuracy
- Ensure adequate lighting for optimal face detection
- Close unnecessary applications to free up system resources
- For web version, use a modern browser with good performance

## 📱 Mobile Support

The web application is fully responsive and works on:
- 📱 Smartphones (iOS/Android)
- 📱 Tablets
- 💻 Desktop computers
- 🖥️ Laptops

## 🔄 Updates

Stay updated with the latest features and improvements by:
- ⭐ Starring this repository
- 🔔 Watching for updates
- 📧 Following release announcements

---

**Enjoy exploring your emotions! 😊**

*Available as both desktop and web applications for maximum accessibility.*

