"""
Main Gradio interface - designed for non-technical users
Simple, clean, dark mode interface
"""

import gradio as gr
import logging
from typing import Dict, Any, List
from pathlib import Path
from ..utils.env_utils import env_config

from ..enhanced_model_manager import EnhancedModelManager
from ..hardware_detector import HardwareDetector
from ..jailbreak_finder import JailbreakPromptFinder
from ..data_processor import DataProcessor
from ..simple_trainer import SimpleTrainer
from .search_interface import SearchInterface

def create_gradio_interface(model_manager: EnhancedModelManager, hardware_info: Dict[str, Any]) -> gr.Blocks:
    """Create the main Gradio interface"""
    
    # Initialize components
    jailbreak_finder = JailbreakPromptFinder()
    data_processor = DataProcessor()
    trainer = SimpleTrainer(model_manager, hardware_info)
    
    # Custom CSS for dark theme
    css = """
    .dark {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    .gradio-container {
        background-color: #0f0f0f;
    }
    .gr-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    .gr-button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .info-box {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    """
    
    with gr.Blocks(theme=gr.themes.Soft(), css=css, title="AI Model Fine-Tuning Studio") as app:
        gr.Markdown("# 🤖 AI Model Fine-Tuning Studio")
        gr.Markdown("### Simple, powerful fine-tuning for everyone")
        
        with gr.Tab("🏠 Home"):
            # Hardware info
            hardware_box = gr.HTML(
                value=f"""
                <div class="info-box">
                    <h3>💻 Your System</h3>
                    <p><strong>Device:</strong> {hardware_info['device_name']}</p>
                    <p><strong>Memory:</strong> {hardware_info['memory_gb']:.1f}GB</p>
                    <p><strong>Status:</strong> {hardware_info['recommendation']}</p>
                </div>
                """
            )
        
        with gr.Tab("🔍 Search & Download"):
            search_interface = SearchInterface(model_manager)
            search_ui = search_interface.create_search_interface()
            search_ui.render()
        
        with gr.Tab("📋 My Models"):
            gr.Markdown("## Your Installed Models")
            
            refresh_btn = gr.Button("🔄 Refresh List")
            models_table = gr.Dataframe(
                headers=["Model Name", "Type", "Size", "Location"],
                interactive=False,
                label="Installed Models"
            )
        
        with gr.Tab("🔓 Jailbreak Prompts"):
            gr.Markdown("## Automatic Jailbreak Prompts")
            gr.Markdown("These prompts help create less restricted models for research purposes")
            
            jailbreaks = jailbreak_finder.get_available_jailbreaks()
            
            with gr.Row():
                with gr.Column():
                    jailbreak_dropdown = gr.Dropdown(
                        choices=[j["name"] for j in jailbreaks],
                        value=jailbreak_finder.get_recommended_jailbreak()["name"],
                        label="Select Jailbreak Type"
                    )
                    
                    jailbreak_preview = gr.Textbox(
                        label="Jailbreak Prompt Preview",
                        lines=5,
                        interactive=False
                    )
                    
                    auto_jailbreak = gr.Checkbox(
                        label="Auto-select best jailbreak",
                        value=True
                    )
        
        with gr.Tab("📊 Data Import"):
            gr.Markdown("## Upload Your Training Data")
            gr.Markdown("Supported: PDF, TXT, DOCX, CSV, JSON, MD")
            
            with gr.Row():
                with gr.Column():
                    file_upload = gr.File(
                        label="Upload Files",
                        file_count="multiple",
                        file_types=[".pdf", ".txt", ".docx", ".csv", ".json", ".md"]
                    )
                    
                    upload_btn = gr.Button("📤 Process Files", variant="primary")
                    upload_status = gr.Textbox(label="Processing Status", interactive=False)
                
                with gr.Column():
                    processed_data = gr.Textbox(
                        label="Processed Data Preview",
                        lines=10,
                        interactive=False
                    )
        
        with gr.Tab("🎯 Fine-Tune"):
            gr.Markdown("## Start Fine-Tuning")
            
            with gr.Row():
                with gr.Column():
                    model_select = gr.Dropdown(
                        label="Select Model to Fine-Tune",
                        choices=["Select a model first..."]
                    )
                    
                    training_method = gr.Radio(
                        choices=["Quick Fine-tune", "Advanced Fine-tune"],
                        value="Quick Fine-tune",
                        label="Training Method"
                    )
                    
                    start_training = gr.Button("🚀 Start Training", variant="primary")
                    training_status = gr.Textbox(label="Training Status", interactive=False)
                
                with gr.Column():
                    training_progress = gr.Progress()
                    training_logs = gr.Textbox(
                        label="Training Logs",
                        lines=15,
                        interactive=False
                    )
        
        # Settings Tab
        with gr.Tab("⚙️ Settings"):
            gr.Markdown("## Application Settings")
            
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Hugging Face Token")
                    gr.Markdown("Enter your Hugging Face token to access private models and increase API limits.")
                    gr.Markdown("Get your token from [Hugging Face Account Settings](https://huggingface.co/settings/tokens)")
                    
                    with gr.Row():
                        hf_token = gr.Textbox(
                            label="HF Token",
                            value=model_manager.hf_token or "",
                            type="password",
                            placeholder="hf_...",
                            show_label=False,
                            container=False,
                            scale=5
                        )
                        save_btn = gr.Button("💾 Save", variant="primary", scale=1)
                    
                    token_status = gr.Textbox(
                        label="Status",
                        value="✅ Token saved" if model_manager.hf_token else "⚠️ No token set. Some features may be limited.",
                        interactive=False
                    )
                    
                    def save_hf_token(token: str):
                        """Save HF token and update model manager"""
                        model_manager.hf_token = token.strip()
                        # Save to config's env_config
                        if hasattr(model_manager.config, 'env_config'):
                            model_manager.config.env_config.save_hf_token(token)
                        return {
                            token_status: gr.Textbox.update(
                                value="✅ Token saved successfully!",
                                visible=True
                            ),
                            hf_token: gr.Textbox.update(value="")
                        }
                    
                    save_btn.click(
                        fn=save_hf_token,
                        inputs=[hf_token],
                        outputs=[token_status, hf_token]
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### About")
                    gr.Markdown("""
                    **Hugging Face Fine-Tuning UI**  
                    Version 1.0.0  
                    
                    [View on GitHub](https://github.com/yourusername/hf-finetune-ui)  
                    [Report an Issue](https://github.com/yourusername/hf-finetune-ui/issues)
                    """)
        
        # Event handlers
        def update_models_list():
            models = model_manager.get_installed_models()
            return [[m["name"], m["type"], m["size"], m.get("path", "")] for m in models]
        
        def update_jailbreak_preview(jailbreak_name):
            prompt = jailbreak_finder.get_jailbreak_prompt(jailbreak_name)
            return prompt
        
        def process_uploaded_files(files):
            if not files:
                return "No files uploaded"
            
            processed = data_processor.process_files(files)
            return f"Processed {len(processed)} files successfully!"
        
        # Connect events
        refresh_btn.click(update_models_list, outputs=models_table)
        jailbreak_dropdown.change(update_jailbreak_preview, inputs=jailbreak_dropdown, outputs=jailbreak_preview)
        upload_btn.click(process_uploaded_files, inputs=file_upload, outputs=upload_status)
        
        # Initial loads
        app.load(update_models_list, outputs=models_table)
        app.load(lambda: jailbreak_finder.get_recommended_jailbreak()["name"], outputs=jailbreak_dropdown)
        app.load(lambda: jailbreak_finder.get_recommended_jailbreak()["prompt"], outputs=jailbreak_preview)
    
    return app
