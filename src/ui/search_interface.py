"""
Google-like search interface for model discovery
Modern, clean interface with real search functionality
"""

import gradio as gr
import time
from typing import List, Dict, Any

class SearchInterface:
    """Google-like search interface for models"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    def create_search_interface(self):
        """Create Google-like search interface"""
        
        css = """
        .search-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .search-box {
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .search-box:focus {
            border-color: #667eea;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        .search-results {
            margin-top: 20px;
        }
        
        .model-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .model-card:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .model-title {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .model-url {
            color: #4ade80;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .model-description {
            color: #d1d5db;
            margin-bottom: 10px;
            line-height: 1.5;
        }
        
        .model-stats {
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 15px;
        }
        
        .model-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .tag {
            background: #374151;
            color: #d1d5db;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        
        .download-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .download-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }
        
        .download-btn:disabled {
            background: #374151;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #9ca3af;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #9ca3af;
        }
        """
        
        def search_models(query, progress=gr.Progress()):
            """Search models with progress"""
            if not query.strip():
                return format_search_results(self.model_manager.get_popular_models())
            
            progress(0.2, "Searching Hugging Face...")
            results = self.model_manager.search_models_real(query)
            progress(1.0, "Search complete!")
            
            return format_search_results(results)
        
        def format_search_results(results: List[Dict[str, Any]]) -> str:
            """Format search results as HTML cards"""
            if not results:
                return """
                <div class="no-results">
                    <h3>🔍 No models found</h3>
                    <p>Try different keywords or check popular models below</p>
                </div>
                """
            
            html_parts = []
            for model in results:
                tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in model.get('tags', [])])
                
                download_btn_text = "✅ Downloaded" if model.get('is_downloaded', False) else "📥 Download"
                download_disabled = "disabled" if model.get('is_downloaded', False) else ""
                
                html_parts.append(f"""
                <div class="model-card">
                    <div class="model-title">{model['name']}</div>
                    <div class="model-url">by {model['author']} • {model['size']}</div>
                    <div class="model-description">{model['description']}</div>
                    <div class="model-stats">
                        <span>👥 {model['downloads']:,} downloads</span>
                        <span>❤️ {model['likes']} likes</span>
                    </div>
                    <div class="model-tags">{tags_html}</div>
                    <button class="download-btn" {download_disabled} onclick="downloadModel('{model['id']}')">
                        {download_btn_text}
                    </button>
                </div>
                """)
            
            return ''.join(html_parts)
        
        def download_model_handler(model_id):
            """Handle model download"""
            if not model_id:
                return "❌ No model selected"
            
            result = self.model_manager.download_model_real(model_id)
            
            if result["success"]:
                return f"✅ Successfully downloaded {model_id} to {result['path']}"
            else:
                return f"❌ Download failed: {result['error']}"
        
        with gr.Blocks(css=css, theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            <div style="text-align: center; margin-bottom: 30px;">
                <h1>🔍 Model Search</h1>
                <p style="color: #9ca3af;">Discover and download AI models from Hugging Face</p>
            </div>
            """)
            
            with gr.Column(elem_classes=["search-container"]):
                # Search box
                search_input = gr.Textbox(
                    label="",
                    placeholder="Search for models like 'chatbot', 'code generation', 'translation'...",
                    elem_classes=["search-box"]
                )
                
                # Search button
                search_btn = gr.Button("🔍 Search", variant="primary", size="lg")
                
                # Results
                results_html = gr.HTML()
                
                # Hidden components for download
                model_id_hidden = gr.Textbox(visible=False)
                download_status = gr.Textbox(label="Download Status", interactive=False)
            
            # Event handlers
            search_btn.click(
                search_models,
                inputs=[search_input],
                outputs=[results_html]
            )
            
            search_input.submit(
                search_models,
                inputs=[search_input],
                outputs=[results_html]
            )
            
            # Load popular models on startup
            interface.load(
                lambda: format_search_results(self.model_manager.get_popular_models()),
                outputs=[results_html]
            )
        
        return interface
