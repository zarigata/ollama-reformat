"""
Dashboard tab for the Gradio interface
"""

import gradio as gr
from typing import List, Dict, Any
import time
from ..core.model_discovery import ModelDiscovery
from ..core.hardware_detector import HardwareDetector

def create_dashboard_tab(model_discovery: ModelDiscovery):
    """Create the dashboard tab with model discovery and system info"""
    
    hardware = HardwareDetector()
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🔍 Model Discovery")
            
            with gr.Row():
                task_input = gr.Textbox(
                    label="Describe your use case",
                    placeholder="e.g., 'medical question answering' or 'code generation'",
                    lines=2
                )
                
                discover_btn = gr.Button("🔍 Find Models", variant="primary")
            
            model_results = gr.Dataframe(
                headers=["Model", "Size", "Use Case", "Performance", "Download"],
                datatype=["str", "str", "str", "str", "str"],
                interactive=False,
                wrap=True
            )
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh Models")
                download_btn = gr.Button("📥 Download Selected")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🖥️ System Status")
            
            device_info = gr.Textbox(
                label="Hardware Detection",
                value=f"Device: {hardware.device.upper()}\n"
                      f"RAM: {hardware.memory['total_gb']} GB\n"
                      f"Available: {hardware.memory['available_gb']} GB\n"
                      f"Threads: {hardware.threads}",
                lines=4,
                interactive=False
            )
            
            training_config = gr.JSON(
                label="Optimized Training Config",
                value=hardware.get_training_config()
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📈 Quick Actions")
            
            quick_actions = [
                gr.Button("🚀 Start Quick Fine-Tune"),
                gr.Button("📊 View Recent Models"),
                gr.Button("⚙️  System Settings")
            ]
    
    # Event handlers
    def discover_models(task_description):
        """Discover models based on task description"""
        if not task_description.strip():
            return [["No task specified", "-", "-", "-", "-"]]
        
        models = model_discovery.find_models_for_task(task_description)
        return [[
            m["name"],
            m["size"],
            m["use_case"],
            m["performance"],
            "Ready" if m["available"] else "Download"
        ] for m in models[:10]]
    
    def refresh_model_list():
        """Refresh the model list"""
        models = model_discovery.get_available_models()
        return [[
            m["name"],
            m["size"],
            m["use_case"],
            m["performance"],
            "Ready" if m["available"] else "Download"
        ] for m in models]
    
    # Connect events
    discover_btn.click(
        fn=discover_models,
        inputs=[task_input],
        outputs=[model_results]
    )
    
    refresh_btn.click(
        fn=refresh_model_list,
        outputs=[model_results]
    )
    
    # Initial load
    interface.load(
        fn=refresh_model_list,
        outputs=[model_results]
    )
