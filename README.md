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

- **PDF** (`.pdf`) — Books, documents, papers
- **Text** (`.txt`) — Plain text files
- **Word** (`.docx`) — Word documents
- **CSV** (`.csv`) — Spreadsheets
- **JSON** (`.json`) — Structured data
- **Markdown** (`.md`) — Notes, documentation, etc.

---

## ⚡ System Requirements

**Minimum:**
- Windows 10/11, macOS, or Linux
- 4GB RAM
- 2GB free disk space

**Recommended:**
- 8GB+ RAM
- NVIDIA/AMD GPU (optional, but much faster)
- 10GB+ free disk space

---

## 🛠️ Troubleshooting & FAQ

### Common Issues

- **"Python not found"**: Install Python 3.11+ from [python.org](https://python.org) and check "Add Python to PATH" during installation.
- **"CUDA not working"**: The app will use CPU automatically if GPU is unavailable. CPU is slower but works fine.
- **"Out of memory"**: Close other programs, use smaller models (<1GB), or let the app auto-adjust batch sizes.
- **Other issues**: Check logs in `hf_finetune.log`, restart the app, or try smaller files/models.

### Where is my data stored?
All data is saved locally in `~/.hf_finetune/` (config, models, uploads, logs).

### How do I use my custom model?
After training, your model is automatically converted to Ollama format for instant use with the Ollama server or compatible apps.

---

## 🧑‍💻 Example Workflow

1. **Download** a base model (e.g., `microsoft/DialoGPT-small`)
2. **Upload** your PDF or text data
3. **Pick** a jailbreak prompt (e.g., "DAN")
4. **Click** "Start Training"
5. **Wait** for training (30–60 minutes typical)
6. **Use** your custom model in Ollama!

---

## 🔬 What Happens Behind the Scenes?

- **Detects** your hardware (GPU/CPU)
- **Downloads** and prepares the base model
- **Processes** your files into training-ready data
- **Applies** LoRA fine-tuning (efficient, fast)
- **Converts** the result to Ollama format
- **Organizes** everything in accessible folders

---

## 🎨 Customization

All settings are optimized by default, but advanced users can tweak:
- `~/.hf_finetune/config.json` — User settings
- `~/.hf_finetune/models/` — Downloaded models
- `~/.hf_finetune/uploads/` — Your training data

---

## 🙏 Credits & Acknowledgements

### Ollama
This project is powered by [Ollama](https://ollama.com/) — **the BEST open-source LLM endpoint**. Huge thanks to the Ollama creators for building an incredible, privacy-first, local-first AI platform. Their work makes it possible for everyone to run state-of-the-art language models on their own hardware, with maximum freedom and control.

### Hugging Face
Massive gratitude to [Hugging Face](https://huggingface.co/) — the most awesome website and community for open-source AI models, datasets, and research. Their platform is the backbone of modern AI development and sharing.

### Community
Thank you to the open-source AI community for inspiration, feedback, and support. Made with ❤️ for everyone who believes in accessible, ethical, and open AI.

---

## 🆘 Support

If you need help:
- Check the logs in `hf_finetune.log`
- Restart the app
- Try with smaller files or models
- All your data is always stored locally
- [Open an issue](https://github.com/your-repo/issues) or reach out to the community

---

## 📜 License

This project is open-source under the MIT License. See [LICENSE](LICENSE) for details.

---

**No APIs, no cloud, no vendor lock-in — everything runs locally on your computer.**

---

> **Made possible by the open-source AI movement.**
