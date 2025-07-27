# Ollama Model Fine-Tuning UI

A modern web interface for fine-tuning and managing Ollama language models with support for CUDA, CPU, and ZLUDA.

![Ollama Model Fine-Tuning UI](screenshot.png)

## Features

- **Model Management**: View, download, and manage Ollama models
- **Fine-Tuning**: Fine-tune models with custom datasets
- **Hardware Detection**: Automatic detection of CUDA, CPU, and ZLUDA capabilities
- **Modern UI**: Clean, responsive interface built with FastAPI and Tailwind CSS
- **Easy Installation**: Simple setup with Python and pip

## Prerequisites

- Python 3.8+
- Ollama installed and running (https://ollama.ai/)
- pip (Python package manager)
- Node.js and npm (for frontend development, optional)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zarigata/ollama-finetune-ui.git
   cd ollama-finetune-ui
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   # On Windows
   python -m venv venv
   .\\venv\\Scripts\\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with the following content:
   ```
   DEBUG=true
   SECRET_KEY=your-secret-key-here
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## Usage

1. **Start the development server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Open your browser and navigate to**:
   ```
   http://localhost:8000
   ```

## Project Structure

```
ollama-finetune-ui/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── models/            # Model management
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── utils/             # Utility functions
│   ├── config.py          # Configuration settings
│   └── __init__.py        # Package initialization
├── .env                  # Environment variables
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Development

### Frontend Development

The frontend uses Tailwind CSS for styling. To make changes to the CSS:

1. Install Node.js and npm if you haven't already
2. Install the required dependencies:
   ```bash
   cd static
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
3. Edit the `static/css/input.css` file to customize styles
4. Rebuild the CSS:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --watch
   ```

### Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Add your feature"
   ```
3. Push to the branch and create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ollama](https://ollama.ai/) for the amazing language models
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Alpine.js](https://alpinejs.dev/) for the minimal JavaScript framework

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
