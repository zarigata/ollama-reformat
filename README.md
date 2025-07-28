# 🤖 AI Model Fine-Tuning Studio

**The simplest way to fine-tune AI models for Ollama - no technical knowledge required!**

## 🚀 Quick Start (1-Click Setup)

### Windows
1. **Download** this folder
2. **Double-click** `start.bat`
3. **Wait** for setup to complete (5-10 minutes)
4. **Open** your browser to `http://localhost:7860`

### Manual Setup (if needed)
```bash
# Install Python 3.11+ if not already installed
# Then run:
pip install -r requirements.txt
python app.py
```

## 📋 What You Can Do

### 🎯 **For Complete Beginners**
- **Download** popular AI models with one click
- **Upload** your PDFs, documents, or text files
- **Select** a jailbreak prompt (automatically finds the best ones)
- **Click** "Start Training" - that's it!

### 🔧 **Automatic Features**
- **Hardware Detection**: Automatically uses your GPU (NVIDIA/AMD) or CPU
- **Memory Management**: Optimizes for your system
- **Jailbreak Prompts**: Latest techniques auto-applied
- **Model Conversion**: Automatically converts to Ollama format

## 🏠 Interface Overview

| Tab | What It Does |
|-----|---------------|
| **🏠 Home** | Shows your system info and quick stats |
| **📥 Download** | Browse and download popular models |
| **📋 My Models** | See all your installed models |
| **🔓 Jailbreak** | Auto-select jailbreak prompts |
| **📊 Data Import** | Upload your training files |
| **🎯 Fine-Tune** | One-click training |

## 📁 Supported File Types

- **📄 PDF** - Books, documents, papers
- **📝 TXT** - Plain text files
- **📊 DOCX** - Word documents
- **📈 CSV** - Spreadsheets
- **📋 JSON** - Structured data
- **📖 MD** - Markdown files

## ⚡ System Requirements

**Minimum:**
- Windows 10/11, macOS, or Linux
- 4GB RAM
- 2GB free disk space

**Recommended:**
- 8GB+ RAM
- NVIDIA/AMD GPU (optional but faster)
- 10GB+ free disk space

## 🔧 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.11+ from python.org
- Check "Add Python to PATH" during installation

**"CUDA not working"**
- The app will automatically fall back to CPU
- CPU training works fine, just slower

**"Out of memory"**
- Close other programs
- Use smaller models (under 1GB)
- The app automatically adjusts batch sizes

### Get Help
- Check the logs in `hf_finetune.log`
- Restart the app if something goes wrong
- All data is saved in `~/.hf_finetune/` folder

## 🎯 Example Workflow

1. **Download** `microsoft/DialoGPT-small` (350MB)
2. **Upload** your PDF documents
3. **Select** "DAN" jailbreak prompt
4. **Click** "Start Training"
5. **Wait** 30-60 minutes
6. **Use** your custom model in Ollama!

## 📊 What Happens Behind the Scenes

- **Auto-detects** your hardware (GPU/CPU)
- **Downloads** the model automatically
- **Processes** your files into training data
- **Applies** LoRA fine-tuning (efficient)
- **Converts** to Ollama format
- **Saves** everything in organized folders

## 🎨 Customization

All settings are automatically optimized, but you can find advanced options in:
- `~/.hf_finetune/config.json` (user settings)
- `~/.hf_finetune/models/` (downloaded models)
- `~/.hf_finetune/uploads/` (your training data)

## 🆘 Support

This tool is designed to "just work". If you encounter issues:
1. Check the logs
2. Restart the application
3. Try with smaller files/models first
4. All your data is safely stored locally

---

**Made with ❤️ for the AI community**

No APIs, no cloud, everything runs locally on your computer.
