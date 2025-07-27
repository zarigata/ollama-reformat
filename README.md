# Ollama Fine-Tuning Studio

A modern, clean web interface for fine-tuning Ollama models with advanced features including jailbreak prompts, data import from PDFs/documents, and comprehensive model management.

## Features

- **Modern UI**: Clean, responsive interface built with React + Tailwind CSS
- **Model Management**: Browse installed models, search popular models, and download new ones
- **Fine-Tuning**: Multiple fine-tuning modes including jailbreak prompts and data import
- **Data Import**: Upload and process PDF, TXT, MD, and DOCX files for training
- **Real-time Progress**: Monitor training progress with live updates
- **GitHub Integration**: Connect with your GitHub account for model sharing
- **Virtual Environment**: Python virtual environment support

## 🚀 One-Click Setup & Run

### Prerequisites
- Python 3.11+
- Node.js 16+
- Ollama installed and running (`ollama serve`)

### 🎯 Super Quick Start (Choose One)

#### **Option 1: Cross-Platform Python Script** ⭐ (Recommended)
```bash
# Windows, macOS, Linux - One command does everything
python start_all.py
```

#### **Option 2: Windows Batch Script**
```cmd
# Double-click or run in Command Prompt
start_all.bat
```

#### **Option 3: Windows PowerShell**
```powershell
# Run in PowerShell
.\start_all.ps1
```

#### **Option 4: Manual Setup (Advanced)**
If you prefer manual control:

1. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Start services separately**
   ```bash
   # Terminal 1: Backend
   python -m uvicorn backend.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   npm run dev
   ```

### 📁 Virtual Environment Location
The Python virtual environment is created automatically in:
```
ollama-fine-tuning-studio/
├── venv/                 # Python virtual environment
├── backend/
├── src/
├── start_all.py         # One-click startup (cross-platform)
├── start_all.bat        # Windows batch script
├── start_all.ps1        # PowerShell script
└── ...
```

## Usage

### Model Management
- View installed models on the **Models** page
- Search for new models using the built-in search
- Download models directly from Ollama
- Remove unused models to free up space

### Fine-Tuning
- Select a model to fine-tune
- Choose your fine-tuning type:
  - **General**: Improve model with custom data
  - **Jailbreak**: Add latest jailbreak techniques
  - **Data Import**: Train with uploaded documents
- Monitor training progress in real-time

### Data Import
- Upload PDF, TXT, MD, or DOCX files
- Configure text extraction and chunking options
- Process documents for training data
- Review processed data before training

## Development

### Project Structure
```
ollama-fine-tuning-studio/
├── backend/
│   └── main.py          # FastAPI backend
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page components
│   ├── App.jsx         # Main app component
│   └── main.jsx        # React entry point
├── package.json        # Frontend dependencies
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS, React Router
- **Backend**: FastAPI, Python 3.11, Ollama Python SDK
- **Styling**: Tailwind CSS with custom dark theme
- **Icons**: Lucide React

### API Endpoints
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/models/installed` - List installed models
- `GET /api/models/popular` - List popular models
- `GET /api/models/search` - Search models
- `POST /api/models/download` - Download a model
- `POST /api/data/process` - Process uploaded documents
- `GET/POST /api/settings` - Application settings

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and test thoroughly
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub or contact the maintainer.

---

**Made with ❤️ by [zarigata](https://github.com/zarigata)**
