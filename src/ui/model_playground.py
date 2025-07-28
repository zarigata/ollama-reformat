"""
Model Playground - Interactive chat interface for testing Ollama models
"""
import gradio as gr
import json
import logging
import os
import psutil
import requests
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

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
    
    def check_ollama_health(self) -> Tuple[bool, str]:
        """Check if Ollama API is healthy and responding"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                return True, "Ollama is running and responding"
            return False, f"Ollama API returned status code {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Failed to connect to Ollama: {str(e)}"
    
    def list_ollama_models(self) -> List[str]:
        """List all available Ollama models"""
        try:
            # Check if Ollama is installed
            if not check_ollama_installed():
                logger.warning("Ollama is not installed")
                return []
                
            # Check Ollama health
            is_healthy, health_msg = self.check_ollama_health()
            if not is_healthy:
                logger.warning(f"Ollama health check failed: {health_msg}")
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
        template: str = "Chat",
        chat_history: List[Tuple[str, str]] = None
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """Generate response using Ollama API"""
        if not user_input.strip():
            return "Please enter a message.", chat_history or []
            
        try:
            # Use provided chat history or fallback to instance history
            if chat_history is None:
                chat_history = self.chat_history
            
            # Format the prompt using the selected template
            prompt_template = self.prompt_templates.get(template, "{user_input}")
            formatted_input = prompt_template.format(user_input=user_input)
            
            # Add user message to chat history
            chat_history.append((user_input, ""))
            
            # Prepare the chat history for context in the format Ollama expects
            messages = []
            for i, (user_msg, bot_msg) in enumerate(chat_history):
                if user_msg:
                    messages.append({"role": "user", "content": user_msg})
                if bot_msg and i < len(chat_history) - 1:  # Don't include the empty bot message we just added
                    messages.append({"role": "assistant", "content": bot_msg})
            
            # Log the request being sent to Ollama
            logger.debug(f"Sending request to Ollama API: {json.dumps({
                'model': model_name,
                'messages': [{'role': m['role'], 'content': f"{m['content'][:50]}..." if len(m['content']) > 50 else m['content']} for m in messages],
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens
                },
                'stream': False
            }, indent=2)}")
            
            # Call Ollama API with streaming disabled first
            try:
                response = requests.post(
                    f"{self.ollama_base_url}/api/chat",
                    json={
                        "model": model_name,
                        "messages": messages,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        },
                        "stream": False
                    },
                    timeout=120  # Increased timeout to 120 seconds
                )
                
                # Log raw response for debugging
                logger.debug(f"Ollama API response: {response.status_code} - {response.text[:500]}")
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if 'message' in response_data and 'content' in response_data['message']:
                            response_text = response_data['message']['content']
                            # Update the last message in chat history with the response
                            if chat_history:
                                chat_history[-1] = (user_input, response_text)
                                self.chat_history = chat_history  # Update instance history
                            return "", chat_history
                        else:
                            error_msg = "Unexpected response format from Ollama API"
                            logger.error(f"{error_msg}: {response_data}")
                            # Try to extract any error message from the response
                            if 'error' in response_data:
                                error_msg = f"Ollama API error: {response_data['error']}"
                            return error_msg, chat_history
                    except json.JSONDecodeError as je:
                        logger.error(f"JSON decode error. Raw response: {response.text}")
                        # Try to extract error message if response is not valid JSON
                        if 'error' in response.text:
                            error_msg = f"Ollama error: {response.text}"
                        else:
                            error_msg = f"Invalid response from Ollama (non-JSON): {response.text[:200]}"
                        return error_msg, chat_history
                else:
                    error_msg = f"Error {response.status_code} from Ollama API"
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            error_msg += f": {error_data['error']}"
                    except:
                        error_msg += f": {response.text}"
                    logger.error(error_msg)
                    return error_msg, chat_history
                    
            except requests.exceptions.RequestException as re:
                error_msg = f"Request error: {str(re)}"
                logger.error(f"{error_msg}", exc_info=True)
                return error_msg, chat_history
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(f"{error_msg}", exc_info=True)
            return error_msg, chat_history
        except json.JSONDecodeError as e:
            error_msg = f"Error decoding Ollama API response: {str(e)}"
            logger.error(f"{error_msg}", exc_info=True)
            return error_msg, chat_history
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"{error_msg}", exc_info=True)
            return error_msg, chat_history
    
    def create_playground_interface(self):
        """Create the Gradio interface for the model playground"""
        with gr.Blocks(
            title="AI Chat Playground",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="indigo",
                neutral_hue="slate",
                spacing_size="sm",
                radius_size="md"
            )
        ) as interface:
            gr.Markdown("""
            # 💬 AI Chat Playground
            Chat with any Ollama model in a clean, responsive interface.
            """)
            
            # Store chat history in the session state
            chat_history = gr.State([])
            
            with gr.Row(equal_height=True):
                # Left sidebar for settings
                with gr.Column(scale=1, min_width=300):
                    gr.Markdown("### ⚙️ Settings")
                    
                    with gr.Group():
                        model_dropdown = gr.Dropdown(
                            label="Model",
                            choices=self.list_ollama_models(),
                            value=self.list_ollama_models()[0] if self.list_ollama_models() else None,
                            interactive=True,
                            scale=2
                        )
                        
                        with gr.Row():
                            refresh_btn = gr.Button("🔄 Refresh Models", variant="secondary")
                            clear_btn = gr.Button("🧹 New Chat", variant="secondary")
                    
                    with gr.Accordion("Advanced Settings", open=False):
                        template_dropdown = gr.Dropdown(
                            label="Prompt Style",
                            choices=list(self.prompt_templates.keys()),
                            value="Chat",
                            interactive=True
                        )
                        
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=1.5,
                            value=0.7,
                            step=0.1,
                            label="Creativity (Temperature)",
                            info="Higher values make output more random"
                        )
                        
                        max_tokens = gr.Slider(
                            minimum=128,
                            maximum=4096,
                            value=2048,
                            step=128,
                            label="Max Response Length",
                            info="Maximum number of tokens to generate"
                        )
                    
                    gr.Markdown("### System Status")
                    system_info = gr.JSON(
                        value={
                            "Status": "🟢 Connected" if self.list_ollama_models() else "🔴 Disconnected",
                            "Available Models": len(self.list_ollama_models()),
                            "Memory Usage": f"{psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB"
                        },
                        label="System Status"
                    )
                
                # Main chat area
                with gr.Column(scale=3):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        value=[],
                        height=600,
                        show_label=False,
                        show_copy_button=True,
                        avatar_images=(
                            "https://i.imgur.com/8BQzOGW.png",  # User avatar
                            "https://i.imgur.com/7L4sINW.png"   # Bot avatar
                        ),
                        bubble_full_width=False,
                        placeholder="Start chatting with the AI...",
                        container=True,
                        show_share_button=True,
                        type="messages"
                    )
                    
                    # User input area
                    with gr.Row():
                        user_input = gr.Textbox(
                            label="",
                            placeholder="Type your message here...",
                            show_label=False,
                            container=False,
                            scale=5,
                            min_width=0,
                            max_lines=5,
                            autofocus=True
                        )
                        
                        with gr.Column(scale=1, min_width=100):
                            send_btn = gr.Button("Send", variant="primary", size="lg")
                            stop_btn = gr.Button("⏹️", variant="stop", size="sm")
                    
                    # Quick action buttons
                    with gr.Row():
                        gr.Examples(
                            examples=[
                                "Explain quantum computing in simple terms",
                                "Write a Python function to sort a list",
                                "What are the latest AI trends?"
                            ],
                            inputs=user_input,
                            label="Try these examples:",
                            examples_per_page=3
                        )
                    
                    # Footer with model info
                    gr.Markdown("""
                    ---
                    <div style="text-align: center; color: #666; font-size: 0.9em;">
                        <p>Powered by Ollama • All processing happens locally on your machine</p>
                    </div>
                    """)
            
            # Event handlers
            def refresh_models():
                models = self.list_ollama_models()
                status = {
                    "Status": "🟢 Connected" if models else "🔴 Disconnected",
                    "Available Models": len(models),
                    "Memory Usage": f"{psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB"
                }
                return [
                    gr.update(choices=models, value=models[0] if models else None),
                    status
                ]
            
            def clear_chat():
                return [], []
            
            def process_message(
                message: str, 
                history: List[Dict[str, str]], 
                model: str, 
                temp: float, 
                tokens: int,
                template: str
            ) -> Tuple[str, List[Dict[str, str]]]:
                if not message.strip():
                    return "", history
                
                # Add user message to history
                history = history + [{"role": "user", "content": message}]
                
                try:
                    # Generate response (streaming would be better here)
                    _, updated_history = self.generate_response(
                        user_input=message,
                        model_name=model,
                        temperature=temp,
                        max_tokens=tokens,
                        template=template,
                        chat_history=history
                    )
                    
                    # Get the last message pair
                    if updated_history and len(updated_history) >= 2:
                        last_user_msg, last_bot_msg = updated_history[-2:]
                        history = history[:-1]  # Remove the placeholder
                        history.extend([
                            {"role": "user", "content": last_user_msg[0]},
                            {"role": "assistant", "content": last_bot_msg[1]}
                        ])
                    
                    return "", history
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    logger.error(f"Error in process_message: {error_msg}", exc_info=True)
                    if history and history[-1]["role"] == "user":
                        history[-1] = {"role": "user", "content": message}
                    history.append({"role": "assistant", "content": error_msg})
                    return "", history
            
            # Connect components
            refresh_btn.click(
                fn=refresh_models,
                outputs=[model_dropdown, system_info],
                show_progress="minimal"
            )
            
            clear_btn.click(
                fn=clear_chat,
                inputs=[],
                outputs=[chatbot, chat_history],
                show_progress="minimal"
            )
            
            # Handle send button click
            msg = send_btn.click(
                fn=process_message,
                inputs=[
                    user_input,
                    chat_history,
                    model_dropdown,
                    temperature,
                    max_tokens,
                    template_dropdown
                ],
                outputs=[user_input, chatbot],
                show_progress="minimal"
            )
            
            # Handle enter key in textbox
            msg_event = user_input.submit(
                fn=process_message,
                inputs=[
                    user_input,
                    chat_history,
                    model_dropdown,
                    temperature,
                    max_tokens,
                    template_dropdown
                ],
                outputs=[user_input, chatbot],
                show_progress="minimal"
            )
            
            # Stop generation button
            stop_btn.click(
                fn=None,
                inputs=None,
                outputs=None,
                cancels=[msg, msg_event]
            )
            
            # Update chat history state
            def update_chat_history(history):
                return history
            
            chatbot.change(
                fn=update_chat_history,
                inputs=chatbot,
                outputs=chat_history
            )
            
            # Auto-refresh models on load
            interface.load(
                fn=refresh_models,
                outputs=[model_dropdown, system_info],
                show_progress="hidden"
            )
            
            return interface
