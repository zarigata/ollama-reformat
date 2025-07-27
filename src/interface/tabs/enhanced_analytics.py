"""
Enhanced Analytics Tab
"""

import gradio as gr
import json
from datetime import datetime

class EnhancedAnalyticsTab:
    """Enhanced analytics interface"""
    
    def create_interface(self):
        """Create enhanced analytics interface"""
        
        with gr.Tabs():
            with gr.TabItem("📈 Performance Metrics"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📊 Training Performance")
                        
                        with gr.Row():
                            total_models = gr.Number(label="Total Models Trained", value=0)
                            avg_accuracy = gr.Number(label="Average Accuracy", value=0.0)
                            total_tokens = gr.Number(label="Total Tokens Processed", value=0)
                        
                        performance_chart = gr.LinePlot(
                            label="Training Performance Over Time",
                            x="epoch",
                            y="loss",
                            color="model"
                        )
                    
                    with gr.Column():
                        gr.Markdown("### 🎯 Model Comparison")
                        
                        comparison_table = gr.HTML()
                        
                        export_report_btn = gr.Button("📊 Export Report")
            
            with gr.TabItem("📋 Training History"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📜 Training Sessions")
                        
                        history_table = gr.HTML()
                        
                        refresh_history_btn = gr.Button("🔄 Refresh History")
                    
                    with gr.Column():
                        gr.Markdown("### 📊 Session Details")
                        
                        session_details = gr.HTML()
            
            with gr.TabItem("🔍 Usage Analytics"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📈 Usage Statistics")
                        
                        usage_stats = gr.HTML()
                        
                        popular_models = gr.HTML()
                    
                    with gr.Column():
                        gr.Markdown("### 📊 Data Insights")
                        
                        data_insights = gr.HTML()
        
        # Event handlers
        def load_analytics():
            """Load analytics data"""
            return self._format_comparison_table(), self._format_history_table(), self._format_usage_stats()
        
        def export_report():
            """Export analytics report"""
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report_data = {
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_models": 0,
                    "total_sessions": 0,
                    "total_tokens": 0,
                    "average_accuracy": 0.0
                },
                "models": [],
                "sessions": []
            }
            
            with open(filename, "w") as f:
                json.dump(report_data, f, indent=2)
            
            return f"Report exported to {filename}"
        
        # Bind events
        gr.on(
            triggers=[gr.on.PageLoad],
            fn=load_analytics,
            outputs=[comparison_table, history_table, usage_stats]
        )
        
        export_report_btn.click(
            fn=export_report,
            outputs=[gr.Textbox(visible=False)]
        )
        
        refresh_history_btn.click(
            fn=lambda: self._format_history_table(),
            outputs=[history_table]
        )
    
    def _format_comparison_table(self) -> str:
        """Format model comparison table"""
        return """
        <div style="text-align: center; padding: 20px;">
            <p>No training data available yet. Start training models to see comparisons.</p>
        </div>
        """
    
    def _format_history_table(self) -> str:
        """Format training history table"""
        return """
        <div style="text-align: center; padding: 20px;">
            <p>No training sessions recorded yet. Your training history will appear here.</p>
        </div>
        """
    
    def _format_usage_stats(self) -> str:
        """Format usage statistics"""
        return """
        <div style="text-align: center; padding: 20px;">
            <p>Usage analytics will be available after your first training session.</p>
        </div>
        """
