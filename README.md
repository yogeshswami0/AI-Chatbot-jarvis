# AI-Chatbot-jarvis


# JARVIS AI Assistant

A modern, interactive AI assistant built with React and Python, featuring voice interaction capabilities and a beautiful user interface.

## 🌟 Features

- 🤖 AI-powered chat interface using Google's Gemini AI
- 🎤 Voice input and output capabilities
- 🎨 Modern, animated UI with responsive design
- 🔄 Real-time chat updates
- 🖼️ Image generation capabilities
- 📱 Mobile-friendly interface
- 🔒 Secure API key management

## 🛠️ Tech Stack

### Frontend
- React.js
- Modern CSS with animations
- WebSocket for real-time communication
- Speech Recognition API
- Web Speech API for text-to-speech

### Backend
- Python Flask
- Google Generative AI (Gemini)
- Speech Recognition
- Flask-SocketIO for real-time updates
- Python-dotenv for environment management

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14.0 or higher
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yogeshswami0/AI-Chatbot-jarvis.git
cd AI-Chatbot-jarvis
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_api_key_here
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

## 🎨 UI Features

- Smooth animations for all interactions
- Modern color scheme with:
  - Primary: Indigo (#6366f1)
  - Secondary: Emerald (#10b981)
  - Accent: Amber (#f59e0b)
- Responsive design for all screen sizes
- Interactive chat bubbles with animations
- Loading indicators and status messages
- Voice input/output controls

## 🔧 Configuration

The application can be configured through the following files:

- `backend/.env`: API keys and environment variables
- `backend/user_config.py`: User preferences and settings
- `frontend/src/App.js`: Frontend configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI capabilities
- The React community for excellent tools and libraries
- The Python community for robust backend solutions

## 📞 Support

For support, please open an issue in the GitHub repository.

## 🔄 Updates

- Version 1.0.0: Initial release with basic chat and voice capabilities
- Version 1.1.0: Added image generation features
- Version 1.2.0: Enhanced UI with modern animations and responsive design

---

Made with ❤️
