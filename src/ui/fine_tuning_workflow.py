"""
Unified Fine-Tuning Workflow Interface
One-stop shop for all fine-tuning operations with descriptive guidance
"""

import gradio as gr
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import os

from ..data_processor import DataProcessor
from ..jailbreak_finder import JailbreakPromptFinder
from ..simple_trainer import SimpleTrainer
from ..enhanced_model_manager import EnhancedModelManager

class FineTuningWorkflow:
    """Centralized fine-tuning workflow with step-by-step guidance"""
    
    def __init__(self, model_manager: EnhancedModelManager, hardware_info: Dict[str, Any]):
        self.model_manager = model_manager
        self.hardware_info = hardware_info
        self.data_processor = DataProcessor()
        self.jailbreak_finder = JailbreakPromptFinder()
        self.trainer = SimpleTrainer(model_manager, hardware_info)
        self.logger = logging.getLogger(__name__)
        
        # Store workflow state
        self.workflow_state = {
            "selected_model": None,
            "training_data": [],
            "jailbreak_config": None,
            "training_config": {},
            "output_settings": {}
        }
    
    def create_workflow_interface(self) -> gr.Blocks:
        """Create the unified fine-tuning workflow interface"""
        
        css = """
        .workflow-step {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .step-number {
            background: white;
            color: #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        .config-panel {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            color: #856404;
        }
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            color: #155724;
        }
        .data-preview {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            background: #f8f9fa;
            font-family: monospace;
            font-size: 12px;
        }
        """
        
        with gr.Blocks(title="Fine-Tuning Workflow Studio", css=css) as interface:
            gr.Markdown("""
            # 🎯 Fine-Tuning Workflow Studio
            ### Complete fine-tuning pipeline in one place - from data to deployment
            """)
            
            # Progress indicator
            progress_bar = gr.HTML(value="""
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="text-align: center; flex: 1;">
                    <div style="width: 30px; height: 30px; background: #667eea; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 5px;">1</div>
                    <div style="font-size: 12px;">Select Model</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="width: 30px; height: 30px; background: #ccc; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 5px;">2</div>
                    <div style="font-size: 12px;">Add Data</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="width: 30px; height: 30px; background: #ccc; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 5px;">3</div>
                    <div style="font-size: 12px;">Configure</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="width: 30px; height: 30px; background: #ccc; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 5px;">4</div>
                    <div style="font-size: 12px;">Train & Export</div>
                </div>
            </div>
            """)
            
            # State management
            workflow_state = gr.State(self.workflow_state)
            
            # Step 1: Model Selection
            with gr.Group():
                gr.HTML("""
                <div class="workflow-step">
                    <span class="step-number">1</span>
                    <strong>Choose Your Base Model</strong>
                    <p>Select the model you want to fine-tune. This will be your foundation.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        available_models = self.model_manager.get_installed_models()
                        model_choices = [m["name"] for m in available_models]
                        
                        base_model = gr.Dropdown(
                            choices=model_choices,
                            label="📦 Base Model"
                        )
                        
                        model_info = gr.HTML()
                        
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        ### 💡 Model Selection Tips
                        - **Small models** (≤ 7B): Good for most tasks, faster training
                        - **Medium models** (7B-13B): Better quality, moderate resources
                        - **Large models** (> 13B): Best quality, needs powerful hardware
                        
                        **Your System**: {} RAM, {} device
                        """.format(
                            f"{self.hardware_info['memory_gb']:.1f}GB",
                            self.hardware_info['device_name']
                        ))
            
            # Step 2: Data Upload & Processing
            with gr.Group():
                gr.HTML("""
                <div class="workflow-step">
                    <span class="step-number">2</span>
                    <strong>Add Your Training Data</strong>
                    <p>Upload documents, text files, or datasets that will teach your model new skills.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        data_upload = gr.File(
                            file_count="multiple",
                            file_types=[".txt", ".pdf", ".docx", ".csv", ".json", ".md"],
                            label="📁 Upload Training Files"
                        )
                        
                        data_preview = gr.HTML(label="📊 Data Preview")
                        
                        process_btn = gr.Button("🔍 Process Files", variant="secondary")
                        
                    with gr.Column():
                        gr.Markdown("""
                        ### 📋 Supported Formats
                        - **PDF files**: Research papers, manuals, books
                        - **Text files**: Plain text, markdown, code
                        - **Documents**: Word docs, CSV data, JSON datasets
                        - **Multiple files**: Combine different sources
                        
                        ### 🎯 Data Quality Tips
                        - Use clean, relevant content
                        - Remove sensitive information
                        - Aim for 1000+ examples for good results
                        - Mix different writing styles for diversity
                        """)
            
            # Step 3: Configuration
            with gr.Group():
                gr.HTML("""
                <div class="workflow-step">
                    <span class="step-number">3</span>
                    <strong>Configure Fine-Tuning</strong>
                    <p>Set up how your model will learn and optionally add jailbreak capabilities.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### ⚙️ Training Settings")
                        
                        with gr.Row():
                            learning_rate = gr.Slider(
                                minimum=1e-5,
                                maximum=1e-2,
                                value=2e-4,
                                step=1e-5,
                                label="Learning Rate"
                            )
                            
                            num_epochs = gr.Slider(
                                minimum=1,
                                maximum=10,
                                value=3,
                                step=1,
                                label="Training Epochs"
                            )
                        
                        max_length = gr.Slider(
                            minimum=128,
                            maximum=2048,
                            value=512,
                            step=64,
                            label="Max Sequence Length"
                        )
                        
                        batch_size = gr.Slider(
                            minimum=1,
                            maximum=8,
                            value=self.hardware_info.get("optimal_batch_size", 1),
                            step=1,
                            label="Batch Size"
                        )
                        
                    with gr.Column():
                        gr.Markdown("### 🔓 Jailbreak Options")
                        
                        enable_jailbreak = gr.Checkbox(
                            label="Enable Jailbreak Training",
                            value=False
                        )
                        
                        jailbreak_type = gr.Dropdown(
                            choices=[j["name"] for j in self.jailbreak_finder.get_available_jailbreaks()],
                            label="Jailbreak Type",
                            value=self.jailbreak_finder.get_recommended_jailbreak()["name"],
                            interactive=False
                        )
                        
                        jailbreak_preview = gr.Textbox(
                            label="Jailbreak Prompt Preview",
                            lines=3,
                            interactive=False,
                            visible=False
                        )
                        
                        # Enable jailbreak type when checkbox is checked
                        enable_jailbreak.change(
                            fn=lambda x: gr.update(interactive=x, visible=x),
                            inputs=[enable_jailbreak],
                            outputs=[jailbreak_type]
                        )
                        
                        jailbreak_type.change(
                            fn=lambda x: self.jailbreak_finder.get_jailbreak_prompt(x) if x else "",
                            inputs=[jailbreak_type],
                            outputs=[jailbreak_preview]
                        )
            
            # Step 4: Training & Export
            with gr.Group():
                gr.HTML("""
                <div class="workflow-step">
                    <span class="step-number">4</span>
                    <strong>Train & Export</strong>
                    <p>Start training and export your fine-tuned model to Ollama format.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        model_name = gr.Textbox(
                            label="🏷️ Model Name",
                            placeholder="my-custom-model-v1"
                        )
                        
                        training_summary = gr.HTML()
                        
                        with gr.Row():
                            start_training = gr.Button("🚀 Start Training", variant="primary", size="lg")
                            export_model = gr.Button("📤 Export to Ollama", variant="secondary", interactive=False)
                    
                    with gr.Column():
                        training_status = gr.HTML()
                        training_logs = gr.Textbox(
                            lines=10,
                            label="Training Logs",
                            interactive=False,
                            visible=False
                        )
            
            # Hidden components for state management
            processed_data_state = gr.State([])
            training_config_state = gr.State({})
            
            # Event handlers
            def update_model_info(model_name):
                if not model_name:
                    return ""
                
                models = self.model_manager.get_installed_models()
                model = next((m for m in models if m["name"] == model_name), None)
                
                if model:
                    return f"""
                    <div class="config-panel">
                        <strong>Model Details:</strong><br>
                        • Size: {model.get('size', 'Unknown')}<br>
                        • Type: {model.get('type', 'Unknown')}<br>
                        • Location: {model.get('path', 'System')}
                    </div>
                    """
                return ""
            
            def process_uploaded_files(files):
                if not files:
                    return [], "<div class='warning-box'>No files uploaded</div>"
                
                try:
                    processed = self.data_processor.process_files(files)
                    if processed:
                        preview = f"""
                        <div class='success-box'>
                            <strong>✅ Processed {len(processed)} files</strong><br>
                            Total text content: {sum(p['size'] for p in processed):,} characters<br>
                            <div class='data-preview'>
                                {chr(10).join(p['filename'] + ': ' + p['content'][:200] + '...' for p in processed[:3])}
                            </div>
                        </div>
                        """
                        return processed, preview
                    else:
                        return [], "<div class='warning-box'>No text content found in files</div>"
                except Exception as e:
                    return [], f"<div class='warning-box'>Error processing files: {str(e)}</div>"
            
            def update_training_summary(model, data, config):
                if not model or not data:
                    return "<div class='warning-box'>Please complete steps 1-3 first</div>"
                
                data_size = sum(d.get('size', 0) for d in data)
                estimated_time = self.trainer._estimate_training_time(len(data))
                
                return f"""
                <div class='config-panel'>
                    <h4>📊 Training Summary</h4>
                    <strong>Model:</strong> {model}<br>
                    <strong>Training Data:</strong> {len(data)} examples ({data_size:,} chars)<br>
                    <strong>Estimated Time:</strong> {estimated_time}<br>
                    <strong>Hardware:</strong> {self.hardware_info['device_name']} ({self.hardware_info['memory_gb']:.1f}GB RAM)
                </div>
                """
            
            def start_training_workflow(model_name, data, lr, epochs, max_len, batch_size, enable_jb, jb_type, model_name_input):
                if not all([model_name, data, model_name_input]):
                    return "<div class='warning-box'>Please complete all required steps</div>", "", False, False
                
                try:
                    # Prepare training data
                    training_data = self.data_processor.prepare_training_data(data)
                    
                    # Get jailbreak prompt if enabled
                    jailbreak_prompt = None
                    if enable_jb and jb_type:
                        jailbreak_prompt = self.jailbreak_finder.get_jailbreak_prompt(jb_type)
                    
                    # Start training
                    result = self.trainer.quick_finetune(
                        model_name=model_name,
                        training_data=training_data,
                        jailbreak_prompt=jailbreak_prompt
                    )
                    
                    if result["status"] == "success":
                        logs = f"""
Training completed successfully!
Model: {model_name_input}
Output: {result['output_path']}
Steps: {result['training_steps']}
Time: {result['estimated_time']}
                        """
                        return (
                            f"<div class='success-box'><strong>✅ Training Complete!</strong><br>Model saved to: {result['output_path']}</div>",
                            logs,
                            True,
                            True
                        )
                    else:
                        return f"<div class='warning-box'>Training failed: {result.get('message', 'Unknown error')}</div>", "", False, False
                        
                except Exception as e:
                    return f"<div class='warning-box'>Error: {str(e)}</div>", "", False, False
            
            def export_to_ollama_workflow(model_path, model_name):
                if not model_name:
                    return "<div class='warning-box'>Please provide a model name</div>"
                
                success = self.trainer.export_to_ollama(model_path, model_name)
                if success:
                    return f"<div class='success-box'><strong>✅ Exported to Ollama!</strong><br>Use: ollama run {model_name}</div>"
                else:
                    return "<div class='warning-box'>Export failed</div>"
            
            # Connect events
            base_model.change(update_model_info, inputs=[base_model], outputs=[model_info])
            
            process_btn.click(
                process_uploaded_files,
                inputs=[data_upload],
                outputs=[processed_data_state, data_preview]
            )
            
            # Update training summary when any config changes
            config_inputs = [base_model, processed_data_state, learning_rate, num_epochs, max_length, batch_size]
            for input_comp in config_inputs:
                input_comp.change(
                    update_training_summary,
                    inputs=config_inputs,
                    outputs=[training_summary]
                )
            
            start_training.click(
                start_training_workflow,
                inputs=[
                    base_model, processed_data_state, learning_rate, num_epochs,
                    max_length, batch_size, enable_jailbreak, jailbreak_type, model_name
                ],
                outputs=[training_status, training_logs, training_logs, export_model]
            )
            
            export_model.click(
                export_to_ollama_workflow,
                inputs=[base_model, model_name],
                outputs=[training_status]
            )
        
        return interface
