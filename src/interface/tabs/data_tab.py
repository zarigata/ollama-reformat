"""
Data management tab for file upload and processing
"""

import gradio as gr
from typing import List, Dict, Any
from ...core.data_processor import DataProcessor

def create_data_tab(data_processor: DataProcessor):
    """Create the data management tab"""
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📁 File Upload")
            
            file_upload = gr.File(
                label="Upload Files",
                file_count="multiple",
                file_types=[".txt", ".md", ".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
            )
            
            upload_btn = gr.Button("📊 Process Files", variant="primary")
            
            with gr.Row():
                chunk_size = gr.Slider(
                    label="Chunk Size (tokens)",
                    minimum=128,
                    maximum=2048,
                    value=512,
                    step=64
                )
                
                preview_chunks = gr.Checkbox(
                    label="Preview chunks",
                    value=True
                )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📊 Processing Results")
            
            processing_summary = gr.JSON(
                label="Summary",
                interactive=False
            )
            
            chunk_preview = gr.Dataframe(
                headers=["Chunk", "Source", "Tokens", "Preview"],
                datatype=["str", "str", "number", "str"],
                interactive=False,
                wrap=True
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 💾 Training Data")
            
            training_data = gr.JSON(
                label="Prepared Dataset",
                interactive=False
            )
            
            save_btn = gr.Button("💾 Save Training Data")
            download_btn = gr.Button("📥 Download Dataset")
    
    # State variables
    processed_data = gr.State([])
    
    def process_uploaded_files(files, chunk_size_val, preview_flag):
        """Process uploaded files"""
        if not files:
            return {}, [], {}
        
        # Process files
        file_paths = [f.name for f in files]
        results = data_processor.process_files(file_paths)
        
        # Chunk data
        chunks = data_processor.chunk_data(results["processed_files"], chunk_size_val)
        
        # Prepare training data
        training_info = data_processor.prepare_training_data(chunks)
        
        # Create preview
        if preview_flag and chunks:
            preview_data = [
                [f"Chunk {i+1}", chunk["source"], chunk["tokens"], chunk["text"][:100] + "..."]
                for i, chunk in enumerate(chunks[:5])
            ]
        else:
            preview_data = []
        
        return results, preview_data, training_info, chunks
    
    def save_training_data(training_info, chunks):
        """Save training data to disk"""
        if not chunks:
            return "No data to save"
        
        # Save as JSONL format for training
        output_file = "training_data.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                training_example = {
                    "instruction": "Continue the following text:",
                    "input": chunk["text"][:200],
                    "output": chunk["text"][200:400] if len(chunk["text"]) > 200 else chunk["text"][200:]
                }
                f.write(json.dumps(training_example) + '\n')
        
        return f"Training data saved to {output_file} ({len(chunks)} examples)"
    
    # Event handlers
    upload_btn.click(
        fn=process_uploaded_files,
        inputs=[file_upload, chunk_size, preview_chunks],
        outputs=[processing_summary, chunk_preview, training_data, processed_data]
    )
    
    save_btn.click(
        fn=save_training_data,
        inputs=[training_data, processed_data],
        outputs=gr.Textbox(label="Status")
    )
