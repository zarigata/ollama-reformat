"""
Model Playground - Interactive chat interface for testing Ollama models
"""
import gradio as gr
import json
import os
import requests
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import logging

from ..utils.ollama_service import ollama_service, ensure_ollama_running, check_ollama_installed

logger = logging.getLogger(__name__)

class ModelPlayground:
    """Interactive playground for testing Ollama models"""
    
    def __init__(self, config):
        self.config = config
        self.ollama_base_url = "http://localhost:11434"
        self.current_model = None
        self.chat_history = []
        self.prompt_templates = {
            "Chat": "[INST] {user_input} [/INST]",
            "Instruction": "### Instruction:\n{user_input}\n\n### Response:\n",
            "QA": "Question: {user_input}\nAnswer:"
        }
    
    def list_ollama_models(self) -> List[str]:
        """List all available Ollama models"""
        try:
            # Check if Ollama is installed
            if not check_ollama_installed():
                logger.warning("Ollama is not installed")
                return []
                
            # Ensure Ollama is running
            success, message = ensure_ollama_running()
            if not success:
                logger.warning(f"Failed to start Ollama: {message}")
                return []
                
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = [model['name'] for model in response.json().get('models', [])]
                return models
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error listing Ollama models: {e}")
            return []
        except Exception as e:
            logger.error(f"Error listing Ollama models: {e}", exc_info=True)
            return []
    
    def generate_response(
        self, 
        user_input: str, 
        model_name: str, 
        temperature: float = 0.7,
        max_tokens: int = 1024,
        template: str = "Chat"
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """Generate response using Ollama API"""
        if not user_input.strip():
            return "Please enter a message.", self.chat_history
            
        try:
            # Format the prompt using the selected template
            prompt_template = self.prompt_templates.get(template, "{user_input}")
            formatted_input = prompt_template.format(user_input=user_input)
            
            # Prepare the chat history for context
            messages = [
                {"role": "user" if i % 2 == 0 else "assistant", "content": msg}
                for i, msg in enumerate([user_input])  # Start with current input
            ]
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_base_url}/api/chat",
                json={
                    "model": model_name,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                stream=False
            )
            
            if response.status_code == 200:
                response_text = response.json()['message']['content']
                self.chat_history.append((user_input, response_text))
                return "", self.chat_history
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return error_msg, self.chat_history
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg, self.chat_history
    
    def create_playground_interface(self):
        """Create the Gradio interface for the model playground"""
        with gr.Blocks(title="Model Playground") as interface:
            gr.Markdown("# 🎮 Model Playground")
            gr.Markdown("Test your fine-tuned Ollama models in an interactive chat interface.")
            
            with gr.Row():
                with gr.Column(scale=3):
                    # Model selection and settings
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            label="Select Model",
                            choices=self.list_ollama_models(),
                            interactive=True
                        )
                        refresh_btn = gr.Button("🔄", variant="secondary")
                    
                    # Chat interface
                    chatbot = gr.Chatbot(
                        label="Chat with Model",
                        height=500,
                        show_copy_button=True
                    )
                    
                    # User input
                    with gr.Row():
                        user_input = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            show_label=False,
                            container=False,
                            scale=5
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)
                    
                    # Settings
                    with gr.Accordion("⚙️ Settings", open=False):
                        with gr.Row():
                            template_dropdown = gr.Dropdown(
                                label="Prompt Template",
                                choices=list(self.prompt_templates.keys()),
                                value="Chat"
                            )
                            temperature = gr.Slider(
                                minimum=0.1,
                                maximum=2.0,
                                value=0.7,
                                step=0.1,
                                label="Temperature"
                            )
                            max_tokens = gr.Slider(
                                minimum=64,
                                maximum=4096,
                                value=1024,
                                step=64,
                                label="Max Tokens"
                            )
                    
                    # Clear button
                    clear_btn = gr.Button("🧹 Clear Chat")
                
                # System info panel
                with gr.Column(scale=1):
                    gr.Markdown("### System Information")
                    system_info = gr.JSON(
                        value={
                            "Ollama Status": "Connected" if self.list_ollama_models() else "Not Connected",
                            "Available Models": len(self.list_ollama_models())
                        },
                        label="System Status"
                    )
                    
                    gr.Markdown("### Quick Tips\n"
                               "- Select your fine-tuned model from the dropdown\n"
                               "- Try different prompt templates for better results\n"
                               "- Adjust temperature for more creative (higher) or focused (lower) responses\n"
                               "- Clear the chat to start a new conversation")
            
            # Event handlers
            def refresh_models():
                models = self.list_ollama_models()
                return gr.Dropdown.update(choices=models, value=models[0] if models else None)
            
            def clear_chat():
                self.chat_history = []
                return []
            
            def send_message(
                message: str, 
                history: List[Tuple[str, str]], 
                model: str, 
                temp: float, 
                tokens: int,
                template: str
            ) -> Tuple[str, List[Tuple[str, str]]]:
                if not message.strip():
                    return "", history
                
                # Add user message to history
                history.append((message, ""))
                
                # Generate response
                _, updated_history = self.generate_response(
                    user_input=message,
                    model_name=model,
                    temperature=temp,
                    max_tokens=tokens,
                    template=template
                )
                
                return "", updated_history
            
            # Connect components
            refresh_btn.click(
                fn=refresh_models,
                outputs=[model_dropdown]
            )
            
            clear_btn.click(
                fn=clear_chat,
                outputs=[chatbot]
            )
            
            send_btn.click(
                fn=send_message,
                inputs=[
                    user_input,
                    gr.State(self.chat_history),
                    model_dropdown,
                    temperature,
                    max_tokens,
                    template_dropdown
                ],
                outputs=[user_input, chatbot]
            )
            
            user_input.submit(
                fn=send_message,
                inputs=[
                    user_input,
                    gr.State(self.chat_history),
                    model_dropdown,
                    temperature,
                    max_tokens,
                    template_dropdown
                ],
                outputs=[user_input, chatbot]
            )
            
            return interface
