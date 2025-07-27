"""
Enhanced Dashboard Tab with improved model discovery and download
"""

import gradio as gr
from typing import List, Dict, Any
import subprocess
import threading
import time
from core.hardware_detector import HardwareDetector
from core.ollama_scraper import OllamaModelScraper

class EnhancedDashboardTab:
    """Enhanced dashboard with better model discovery"""
    
    def __init__(self, hardware: HardwareDetector, scraper: OllamaModelScraper):
        self.hardware = hardware
        self.scraper = scraper
        self.download_status = {}
    
    def create_interface(self):
        """Create enhanced dashboard interface"""
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 🔍 Model Discovery")
                
                with gr.Row():
                    search_input = gr.Textbox(
                        label="Search Models",
                        placeholder="Enter model name or description...",
                        scale=3
                    )
                    search_btn = gr.Button("🔍 Search", scale=1)
                
                with gr.Row():
                    category_filter = gr.Dropdown(
                        choices=["All", "Llama Family", "Mistral AI", "Microsoft Phi", 
                                "Google Gemma", "Alibaba Qwen", "Vision Models", 
                                "Code Models", "Embedding Models"],
                        value="All",
                        label="Filter by Category"
                    )
                    refresh_btn = gr.Button("🔄 Refresh")
                
                model_list = gr.HTML()
                
            with gr.Column(scale=1):
                gr.Markdown("### 📊 System Status")
                
                system_info = gr.HTML()
                
                gr.Markdown("### 📥 Downloads")
                download_status = gr.HTML()
        
        # Event handlers
        def refresh_models(category="All", search_query=""):
            """Refresh model list with filtering"""
            models = self.scraper.scrape_models()
            
            if search_query:
                models = self.scraper.search_models(search_query)
            
            if category != "All":
                models = [m for m in models if m["category"] == category]
            
            return self._format_model_list(models)
        
        def get_system_info():
            """Get current system information"""
            info = self.hardware.get_system_info()
            return self._format_system_info(info)
        
        def get_download_status():
            """Get download status"""
            return self._format_download_status()
        
        # Bind events
        search_btn.click(
            fn=refresh_models,
            inputs=[category_filter, search_input],
            outputs=[model_list]
        )
        
        refresh_btn.click(
            fn=refresh_models,
            inputs=[category_filter, search_input],
            outputs=[model_list]
        )
        
        category_filter.change(
            fn=refresh_models,
            inputs=[category_filter, search_input],
            outputs=[model_list]
        )
        
        # Auto-refresh system info
        def auto_refresh():
            return get_system_info(), get_download_status()
        
        # Load initial data
        gr.on(
            triggers=[gr.on.PageLoad],
            fn=lambda: [refresh_models(), get_system_info(), get_download_status()],
            outputs=[model_list, system_info, download_status]
        )
    
    def _format_model_list(self, models: List[Dict[str, Any]]) -> str:
        """Format models as HTML cards"""
        if not models:
            return "<p>No models found. Try refreshing or adjusting filters.</p>"
        
        html_parts = []
        for model in models:
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in model["tags"]])
            
            html_parts.append(f"""
            <div class="model-card">
                <div class="model-title">{model['name']}</div>
                <div class="model-description">{model['description']}</div>
                <div><strong>Size:</strong> {model['size']}</div>
                <div><strong>Category:</strong> {model['category']}</div>
                <div><strong>Popularity:</strong> {'⭐' * model['popularity']}</div>
                <div class="model-tags">{tags_html}</div>
                <div style="margin-top: 10px;">
                    <button onclick="downloadModel('{model['full_name']}')" 
                            class="gr-button gr-button-lg gr-button-secondary">
                        📥 Download
                    </button>
                </div>
            </div>
            """)
        
        return "".join(html_parts)
    
    def _format_system_info(self, info: Dict[str, Any]) -> str:
        """Format system information"""
        return f"""
        <div style="padding: 10px;">
            <h4>System Overview</h4>
            <p><strong>CPU:</strong> {info.get('cpu_name', 'Unknown')}</p>
            <p><strong>RAM:</strong> {info.get('total_ram_gb', 0):.1f} GB</p>
            <p><strong>GPU:</strong> {info.get('gpu_info', 'CPU Only')}</p>
            <p><strong>Platform:</strong> {info.get('platform', 'Unknown')}</p>
            <p><strong>Python:</strong> {info.get('python_version', 'Unknown')}</p>
            <hr>
            <p><strong>Training Mode:</strong> {info.get('training_mode', 'Unknown')}</p>
            <p><strong>Max Memory:</strong> {info.get('max_memory_gb', 0):.1f} GB</p>
        </div>
        """
    
    def _format_download_status(self) -> str:
        """Format download status"""
        if not self.download_status:
            return "<p>No active downloads</p>"
        
        status_html = []
        for model, status in self.download_status.items():
            if status.get("status") == "downloading":
                progress = status.get("progress", 0)
                bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
                status_html.append(f"""
                <div>
                    <strong>{model}</strong><br>
                    {bar} {progress}%
                </div>
                """)
            elif status.get("status") == "completed":
                status_html.append(f"<div>✅ {model} - Downloaded</div>")
            elif status.get("status") == "error":
                status_html.append(f"<div>❌ {model} - Error: {status.get('error')}</div>")
        
        return "".join(status_html)
    
    def download_model(self, model_name: str) -> str:
        """Download model using Ollama"""
        def download_thread():
            try:
                self.download_status[model_name] = {"status": "downloading", "progress": 0}
                
                # Start download
                process = subprocess.Popen(
                    ["ollama", "pull", model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Monitor progress
                for line in process.stdout:
                    if "%" in line:
                        try:
                            progress = int(line.split("%")[0].split()[-1])
                            self.download_status[model_name]["progress"] = progress
                        except:
                            pass
                
                process.wait()
                
                if process.returncode == 0:
                    self.download_status[model_name] = {"status": "completed"}
                else:
                    self.download_status[model_name] = {
                        "status": "error", 
                        "error": process.stderr.read()
                    }
                    
            except Exception as e:
                self.download_status[model_name] = {
                    "status": "error", 
                    "error": str(e)
                }
        
        # Start download in background
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
        
        return f"📥 Started downloading {model_name}"
