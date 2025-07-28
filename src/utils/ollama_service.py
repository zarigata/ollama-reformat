"""
Ollama Service Manager - Handles starting and checking the Ollama service
"""
import subprocess
import time
import logging
from typing import Optional, Tuple
import psutil
import os

logger = logging.getLogger(__name__)

class OllamaService:
    """Manages the Ollama service for the application"""
    
    def __init__(self):
        self.process = None
        self.port = 11434
        
    def is_running(self) -> bool:
        """Check if Ollama is already running"""
        try:
            # Check if port is in use
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(('localhost', self.port)) == 0
        except Exception as e:
            logger.error(f"Error checking if Ollama is running: {e}")
            return False
    
    def start(self) -> bool:
        """Start the Ollama service if not already running"""
        if self.is_running():
            logger.info("Ollama is already running")
            return True
            
        try:
            # Try to start Ollama in the background
            if os.name == 'nt':  # Windows
                self.process = subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:  # Unix-like
                self.process = subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            
            # Wait a bit for the service to start
            time.sleep(2)
            
            if self.is_running():
                logger.info("Successfully started Ollama service")
                return True
            else:
                logger.error("Failed to start Ollama service")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Ollama: {e}")
            return False
    
    def stop(self):
        """Stop the Ollama service if it was started by us"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("Stopped Ollama service")
            except Exception as e:
                logger.error(f"Error stopping Ollama: {e}")
                try:
                    self.process.kill()
                except:
                    pass
            finally:
                self.process = None

# Global instance
ollama_service = OllamaService()

def ensure_ollama_running() -> Tuple[bool, str]:
    """Ensure Ollama is running, start it if necessary"""
    if ollama_service.is_running():
        return True, "Ollama is already running"
    
    logger.info("Ollama is not running, attempting to start...")
    if ollama_service.start():
        return True, "Successfully started Ollama service"
    else:
        return False, ("Failed to start Ollama. Please make sure Ollama is installed and in your PATH. "
                      "You can download it from https://ollama.ai/download")

def check_ollama_installed() -> bool:
    """Check if Ollama is installed and available in PATH"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, 
                              text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        return result.returncode == 0
    except FileNotFoundError:
        return False
