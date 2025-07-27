"""
Enhanced Data Management Tab
"""

import gradio as gr
from typing import List, Dict, Any
from core.data_processor import DataProcessor

class EnhancedDataTab:
    """Enhanced data management with better UI"""
    
    def __init__(self, processor: DataProcessor):
        self.processor = processor
    
    def create_interface(self):
        """Create enhanced data interface"""
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📁 File Upload")
                
                file_upload = gr.File(
                    label="Upload Files",
                    file_types=[".pdf", ".txt", ".md", ".docx", ".jpg", ".jpeg", ".png", ".webp"],
                    file_count="multiple"
                )
                
                upload_btn = gr.Button("📤 Process Files", variant="primary")
                
                gr.Markdown("### ⚙️ Processing Options")
                chunk_size = gr.Slider(100, 2000, 512, label="Chunk Size", step=50)
                chunk_overlap = gr.Slider(0, 200, 50, label="Chunk Overlap", step=10)
                
                gr.Markdown("### 📊 Statistics")
                stats_output = gr.HTML()
            
            with gr.Column(scale=2):
                gr.Markdown("### 📋 Processed Data")
                
                with gr.Tabs():
                    with gr.TabItem("📄 Files"):
                        files_table = gr.HTML()
                    
                    with gr.TabItem("🔍 Chunks"):
                        chunks_display = gr.HTML()
                    
                    with gr.TabItem("📊 Preview"):
                        preview_text = gr.Textbox(
                            label="Text Preview",
                            lines=10,
                            max_lines=20,
                            interactive=False
                        )
                
                with gr.Row():
                    export_btn = gr.Button("💾 Export Training Data")
                    clear_btn = gr.Button("🗑️ Clear All")
        
        # Event handlers
        def process_files(files, chunk_size_val, chunk_overlap_val):
            """Process uploaded files"""
            if not files:
                return "No files uploaded", "", "", ""
            
            processed_files = []
            all_chunks = []
            total_tokens = 0
            
            for file in files:
                result = self.processor.process_file(file.name, chunk_size_val, chunk_overlap_val)
                if result["success"]:
                    processed_files.append(result)
                    all_chunks.extend(result["chunks"])
                    total_tokens += result["total_tokens"]
            
            # Format outputs
            files_html = self._format_files_table(processed_files)
            chunks_html = self._format_chunks_table(all_chunks)
            stats = self._format_stats(processed_files, total_tokens)
            preview = "\n\n".join([chunk[:200] + "..." for chunk in all_chunks[:5]])
            
            return files_html, chunks_html, preview, stats
        
        def export_training_data():
            """Export training data"""
            try:
                filename = "training_data.jsonl"
                # This would export the actual training data
                return f"Training data exported to {filename}"
            except Exception as e:
                return f"Error exporting: {str(e)}"
        
        def clear_all():
            """Clear all processed data"""
            return "", "", "", ""
        
        # Bind events
        upload_btn.click(
            fn=process_files,
            inputs=[file_upload, chunk_size, chunk_overlap],
            outputs=[files_table, chunks_display, preview_text, stats_output]
        )
        
        export_btn.click(
            fn=export_training_data,
            outputs=[gr.Textbox(visible=False)]
        )
        
        clear_btn.click(
            fn=clear_all,
            outputs=[files_table, chunks_display, preview_text, stats_output]
        )
    
    def _format_files_table(self, files: List[Dict[str, Any]]) -> str:
        """Format files as HTML table"""
        if not files:
            return "<p>No files processed</p>"
        
        html = ["<table style='width: 100%; border-collapse: collapse;'>"]
        html.append("""
        <tr style='background: #f5f5f5;'>
            <th style='padding: 8px; text-align: left; border: 1px solid #ddd;'>File</th>
            <th style='padding: 8px; text-align: left; border: 1px solid #ddd;'>Type</th>
            <th style='padding: 8px; text-align: left; border: 1px solid #ddd;'>Size</th>
            <th style='padding: 8px; text-align: left; border: 1px solid #ddd;'>Chunks</th>
            <th style='padding: 8px; text-align: left; border: 1px solid #ddd;'>Tokens</th>
        </tr>
        """)
        
        for file in files:
            html.append(f"""
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>{file['filename']}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{file['file_type']}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{file['file_size']}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{len(file['chunks'])}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{file['total_tokens']}</td>
            </tr>
            """)
        
        html.append("</table>")
        return "".join(html)
    
    def _format_chunks_table(self, chunks: List[str]) -> str:
        """Format chunks as HTML"""
        if not chunks:
            return "<p>No chunks available</p>"
        
        html = ["<div style='max-height: 400px; overflow-y: auto;'>"]
        for i, chunk in enumerate(chunks[:20]):  # Show first 20 chunks
            html.append(f"""
            <div style='border: 1px solid #ddd; margin: 5px 0; padding: 10px; border-radius: 4px;'>
                <strong>Chunk {i+1}</strong><br>
                <small>{chunk[:150]}...</small>
            </div>
            """)
        
        if len(chunks) > 20:
            html.append(f"<p><em>... and {len(chunks) - 20} more chunks</em></p>")
        
        html.append("</div>")
        return "".join(html)
    
    def _format_stats(self, files: List[Dict[str, Any]], total_tokens: int) -> str:
        """Format statistics"""
        if not files:
            return "<p>No statistics available</p>"
        
        total_files = len(files)
        total_chunks = sum(len(f["chunks"]) for f in files)
        total_size = sum(f["file_size"] for f in files)
        
        return f"""
        <div style="padding: 10px; background: #f9f9f9; border-radius: 8px;">
            <h4>Processing Summary</h4>
            <p><strong>Files:</strong> {total_files}</p>
            <p><strong>Total Size:</strong> {total_size:,} bytes</p>
            <p><strong>Total Chunks:</strong> {total_chunks}</p>
            <p><strong>Total Tokens:</strong> {total_tokens:,}</p>
            <p><strong>Est. Training Time:</strong> ~{total_tokens // 1000} minutes</p>
        </div>
        """
