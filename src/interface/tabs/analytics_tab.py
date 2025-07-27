"""
Analytics tab for performance metrics and model comparison
"""

import gradio as gr
import pandas as pd
import numpy as np

def create_analytics_tab():
    """Create the analytics tab"""
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📊 Performance Metrics")
            
            with gr.Row():
                model_selector = gr.Dropdown(
                    label="Select Model to Analyze",
                    choices=["Current Model", "Base Model", "Comparison"],
                    value="Current Model"
                )
                
                refresh_metrics = gr.Button("🔄 Refresh")
            
            metrics_display = gr.JSON(
                label="Model Performance",
                interactive=False
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📈 Training History")
            
            training_history = gr.LinePlot(
                label="Loss Over Time",
                x="Step",
                y="Loss",
                height=300
            )
            
            accuracy_plot = gr.LinePlot(
                label="Accuracy Over Time",
                x="Step",
                y="Accuracy",
                height=300
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔍 Model Comparison")
            
            compare_models = gr.Dropdown(
                label="Models to Compare",
                choices=["Model A", "Model B", "Model C"],
                multiselect=True,
                value=["Model A", "Model B"]
            )
            
            comparison_table = gr.Dataframe(
                headers=["Model", "Loss", "Accuracy", "Size", "Training Time"],
                datatype=["str", "number", "number", "str", "str"],
                interactive=False
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📋 Reports")
            
            generate_report = gr.Button("📊 Generate Full Report")
            
            report_output = gr.HTML(
                label="Training Report"
            )
    
    def generate_sample_metrics():
        """Generate sample metrics for demonstration"""
        return {
            "model_name": "llama3.1-finetuned",
            "training_loss": 0.85,
            "validation_loss": 1.2,
            "accuracy": 0.92,
            "perplexity": 15.3,
            "training_time": "2h 34m",
            "epochs_completed": 3,
            "samples_processed": 15420
        }
    
    def generate_training_history():
        """Generate sample training history"""
        steps = list(range(1, 101))
        loss = [2.5 - (i * 0.02) + np.random.normal(0, 0.1) for i in range(100)]
        accuracy = [0.3 + (i * 0.006) + np.random.normal(0, 0.05) for i in range(100)]
        
        return pd.DataFrame({
            "Step": steps,
            "Loss": loss,
            "Accuracy": [min(1.0, max(0.0, acc)) for acc in accuracy]
        })
    
    def generate_comparison_data():
        """Generate sample comparison data"""
        return pd.DataFrame({
            "Model": ["Base Llama3.1", "Fine-tuned v1", "Fine-tuned v2"],
            "Loss": [1.8, 0.85, 0.75],
            "Accuracy": [0.75, 0.92, 0.94],
            "Size": ["8B", "8B", "8B"],
            "Training Time": ["0h", "2h 34m", "3h 12m"]
        })
    
    def generate_training_report():
        """Generate a comprehensive training report"""
        report_html = """
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h2>📊 Fine-Tuning Training Report</h2>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>🎯 Summary</h3>
                <p><strong>Model:</strong> llama3.1-finetuned</p>
                <p><strong>Training Duration:</strong> 2h 34m</p>
                <p><strong>Final Loss:</strong> 0.85</p>
                <p><strong>Accuracy:</strong> 92%</p>
                <p><strong>Improvement:</strong> +17% over base model</p>
            </div>
            
            <div style="background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>📈 Key Metrics</h3>
                <ul>
                    <li><strong>Perplexity:</strong> 15.3 (↓ from 45.2)</li>
                    <li><strong>Validation Loss:</strong> 1.2</li>
                    <li><strong>Training Efficiency:</strong> 94%</li>
                    <li><strong>Memory Usage:</strong> 6.2GB / 8GB</li>
                </ul>
            </div>
            
            <div style="background: #f0f8e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>🔍 Recommendations</h3>
                <ul>
                    <li>Consider increasing LoRA rank to 32 for better performance</li>
                    <li>Training data shows good diversity - no overfitting detected</li>
                    <li>Model ready for deployment in production environment</li>
                </ul>
            </div>
        </div>
        """
        return report_html
    
    # Event handlers
    refresh_metrics.click(
        fn=generate_sample_metrics,
        outputs=metrics_display
    )
    
    compare_models.change(
        fn=generate_comparison_data,
        outputs=comparison_table
    )
    
    generate_report.click(
        fn=generate_training_report,
        outputs=report_output
    )
    
    # Initial load
    interface.load(
        fn=generate_sample_metrics,
        outputs=metrics_display
    )
    
    interface.load(
        fn=generate_training_history,
        outputs=training_history
    )
    
    interface.load(
        fn=generate_comparison_data,
        outputs=comparison_table
    )
