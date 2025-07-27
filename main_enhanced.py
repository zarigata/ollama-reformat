#!/usr/bin/env python3
"""
Enhanced Ollama Reformat 2 - Main Application
Improved with better model discovery, enhanced unlock tools, and VENV support
"""

import gradio as gr
import sys
import os
import platform
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.hardware_detector import HardwareDetector
from core.ollama_scraper import OllamaModelScraper
from core.enhanced_unlocker import EnhancedPromptUnlocker
from core.data_processor import DataProcessor
from interface.tabs.enhanced_dashboard import EnhancedDashboardTab
from interface.tabs.enhanced_data import EnhancedDataTab
from interface.tabs.enhanced_training import EnhancedTrainingTab
from interface.tabs.enhanced_prompt import EnhancedPromptTab
from interface.tabs.enhanced_analytics import EnhancedAnalyticsTab

def create_enhanced_interface():
    """Create the enhanced Gradio interface"""
    
    # Initialize core components
    hardware = HardwareDetector()
    scraper = OllamaModelScraper()
    unlocker = EnhancedPromptUnlocker()
    processor = DataProcessor()
    
    # Get system info
    system_info = {
        'cpu_name': f"{platform.system()} {platform.release()}",
        'total_ram_gb': hardware.memory['total_gb'],
        'gpu_info': hardware.gpu_info['name'] if hardware.gpu_info['available'] else 'CPU Only',
        'platform': platform.system(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'training_mode': hardware.device.upper(),
        'max_memory_gb': hardware.memory['available_gb']
    }
    
    # Create interface tabs
    dashboard = EnhancedDashboardTab(hardware, scraper)
    data_tab = EnhancedDataTab(processor)
    training_tab = EnhancedTrainingTab(hardware, scraper)
    prompt_tab = EnhancedPromptTab(unlocker)
    analytics_tab = EnhancedAnalyticsTab()
    
    # Create interface
    with gr.Blocks(
        title="Ollama Reformat 2 - Enhanced LLM Fine-Tuning Platform",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .tab-button {
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        .model-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            background: #fafafa;
        }
        .model-title {
            font-size: 18px;
            font-weight: bold;
            color: #1976d2;
        }
        .model-description {
            color: #666;
            margin: 8px 0;
        }
        .model-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        """
    ) as app:
        
        gr.Markdown("""
        # 🚀 Ollama Reformat 2 - Enhanced LLM Fine-Tuning Platform
        **Advanced local fine-tuning with enhanced model discovery and prompt unlocking**
        
        ---
        """)
        
        with gr.Tabs():
            # Enhanced Dashboard Tab
            with gr.TabItem("🏠 Dashboard", id="dashboard"):
                dashboard.create_interface()
            
            # Enhanced Data Management Tab
            with gr.TabItem("📁 Data Management", id="data"):
                data_tab.create_interface()
            
            # Enhanced Training Tab
            with gr.TabItem("⚙️ Fine-Tuning", id="training"):
                training_tab.create_interface()
            
            # Enhanced Prompt Unlocking Tab
            with gr.TabItem("🔓 Prompt Unlocking", id="prompts"):
                prompt_tab.create_interface()
            
            # Enhanced Analytics Tab
            with gr.TabItem("📊 Analytics", id="analytics"):
                analytics_tab.create_interface()
        
        gr.Markdown("""
        ---
        **System Information:**
        - **CPU**: {cpu_info}
        - **RAM**: {ram_info}
        - **GPU**: {gpu_info}
        - **Platform**: {platform_info}
        
        **Quick Start:**
        1. 📁 Upload your data files (PDF, TXT, images)
        2. 🔍 Discover and download models from the dashboard
        3. ⚙️ Configure fine-tuning parameters
        4. 🔓 Apply prompt unlocking techniques
        5. 📊 Monitor training progress and results
        """.format(
            cpu_info=system_info.get('cpu_name', 'Unknown'),
            ram_info=f"{system_info.get('total_ram_gb', 0):.1f}GB",
            gpu_info=system_info.get('gpu_info', 'CPU Only'),
            platform_info=system_info.get('platform', 'Unknown')
        ))
    
    return app

def main():
    """Main application entry point"""
    print("🚀 Starting Ollama Reformat 2 - Enhanced Version")
    print("=" * 50)
    
    # Create and launch interface
    app = create_enhanced_interface()
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()
