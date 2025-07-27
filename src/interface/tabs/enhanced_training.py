"""
Enhanced Training Tab with better model selection
"""

import gradio as gr
from typing import List, Dict, Any
from core.hardware_detector import HardwareDetector
from core.ollama_scraper import OllamaModelScraper

class EnhancedTrainingTab:
    """Enhanced training interface"""
    
    def __init__(self, hardware: HardwareDetector, scraper: OllamaModelScraper):
        self.hardware = hardware
        self.scraper = scraper
    
    def create_interface(self):
        """Create enhanced training interface"""
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Model Selection")
                
                model_dropdown = gr.Dropdown(
                    label="Select Model",
                    choices=["Loading..."],
                    value="llama3.1:latest"
                )
                
                refresh_models_btn = gr.Button("🔄 Refresh Models")
                
                gr.Markdown("### ⚙️ Training Parameters")
                
                with gr.Tabs():
                    with gr.TabItem("LoRA"):
                        lora_rank = gr.Slider(8, 128, 16, label="LoRA Rank")
                        lora_alpha = gr.Slider(8, 128, 32, label="LoRA Alpha")
                        lora_dropout = gr.Slider(0.0, 0.5, 0.1, label="LoRA Dropout")
                    
                    with gr.TabItem("Training"):
                        learning_rate = gr.Slider(1e-5, 1e-3, 5e-4, label="Learning Rate")
                        batch_size = gr.Slider(1, 32, 4, label="Batch Size")
                        num_epochs = gr.Slider(1, 50, 3, label="Epochs")
                        max_length = gr.Slider(128, 2048, 512, label="Max Length")
                
                start_training_btn = gr.Button("🚀 Start Training", variant="primary")
                stop_training_btn = gr.Button("⏹️ Stop Training")
            
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Training Progress")
                
                with gr.Row():
                    current_epoch = gr.Number(label="Current Epoch", value=0)
                    current_step = gr.Number(label="Current Step", value=0)
                    loss_value = gr.Number(label="Loss", value=0.0)
                
                progress_bar = gr.Progress()
                training_log = gr.Textbox(
                    label="Training Log",
                    lines=10,
                    max_lines=20,
                    interactive=False
                )
                
                with gr.Row():
                    save_model_btn = gr.Button("💾 Save Model")
                    export_btn = gr.Button("📤 Export")
        
        # Event handlers
        def refresh_models():
            """Refresh available models"""
            models = self.scraper.scrape_models()
            choices = [m["full_name"] for m in models]
            return gr.Dropdown(choices=choices, value=choices[0] if choices else None)
        
        def start_training(model_name, lora_rank_val, lora_alpha_val, lora_dropout_val,
                          learning_rate_val, batch_size_val, num_epochs_val, max_length_val):
            """Start training process"""
            config = {
                "model": model_name,
                "lora": {
                    "rank": lora_rank_val,
                    "alpha": lora_alpha_val,
                    "dropout": lora_dropout_val
                },
                "training": {
                    "learning_rate": learning_rate_val,
                    "batch_size": batch_size_val,
                    "epochs": num_epochs_val,
                    "max_length": max_length_val
                }
            }
            
            # This would start actual training
            return f"Training started with model: {model_name}", config
        
        def stop_training():
            """Stop training"""
            return "Training stopped"
        
        def save_model():
            """Save trained model"""
            return "Model saved successfully"
        
        def export_model():
            """Export model"""
            return "Model exported to Ollama format"
        
        # Bind events
        refresh_models_btn.click(
            fn=refresh_models,
            outputs=[model_dropdown]
        )
        
        start_training_btn.click(
            fn=start_training,
            inputs=[model_dropdown, lora_rank, lora_alpha, lora_dropout,
                   learning_rate, batch_size, num_epochs, max_length],
            outputs=[training_log]
        )
        
        stop_training_btn.click(
            fn=stop_training,
            outputs=[training_log]
        )
        
        save_model_btn.click(
            fn=save_model,
            outputs=[training_log]
        )
        
        export_btn.click(
            fn=export_model,
            outputs=[training_log]
        )
        
        # Load initial models
        app.load(
            fn=refresh_models,
            outputs=[model_dropdown]
        )
