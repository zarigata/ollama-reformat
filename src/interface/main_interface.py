"""
Main Gradio interface for Ollama LLM Reformat 2
"""

import gradio as gr
from typing import List, Dict, Any
import os
import sys

from .tabs.dashboard_tab import create_dashboard_tab
from .tabs.data_tab import create_data_tab
from .tabs.training_tab import create_training_tab
from .tabs.prompt_tab import create_prompt_tab
from .tabs.analytics_tab import create_analytics_tab
from ..core.model_discovery import ModelDiscovery
from ..core.data_processor import DataProcessor
from ..core.prompt_unlocker import PromptUnlocker

def create_interface() -> gr.Blocks:
    """Create the main Gradio interface"""
    
    # Initialize core components
    model_discovery = ModelDiscovery()
    data_processor = DataProcessor()
    prompt_unlocker = PromptUnlocker()
    
    # CSS styling
    css = """
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .tab-content {
        padding: 1rem;
    }
    .model-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
    }
    """
    
    with gr.Blocks(
        title="Ollama LLM Reformat 2 - Fine-Tuning Platform",
        theme=gr.themes.Soft(),
        css=css
    ) as interface:
        
        # Header
        gr.Markdown(
            """
            # 🚀 Ollama LLM Reformat 2
            ## Advanced Fine-Tuning & Prompt Unlocking Platform
            """
        )
        
        # Main tabs
        with gr.Tabs():
            
            # Dashboard Tab
            with gr.TabItem("🏠 Dashboard", id=0):
                create_dashboard_tab(model_discovery)
            
            # Data Management Tab
            with gr.TabItem("📁 Data Management", id=1):
                create_data_tab(data_processor)
            
            # Fine-Tuning Tab
            with gr.TabItem("⚙️ Fine-Tuning", id=2):
                create_training_tab()
            
            # Prompt Unlocking Tab
            with gr.TabItem("🔓 Prompt Unlocking", id=3):
                create_prompt_tab(prompt_unlocker)
            
            # Analytics Tab
            with gr.TabItem("📊 Analytics", id=4):
                create_analytics_tab()
        
        # Footer with system info
        gr.Markdown(
            """
            ---
            **System Status**: Ready | **Hardware**: Auto-detected | **Mode**: Local Only
            """
        )
    
    return interface
