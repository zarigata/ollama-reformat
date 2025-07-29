"""
Model Playground - Interactive chat interface for testing Ollama models
"""
import gradio as gr
import json
import logging
import os
import psutil
import requests
from typing import Dict, List, Tuple, Any, Optional, Generator
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
    
    def stream_response(
        self,
        user_input: str,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        template: str = "Chat",
        chat_history: List[Tuple[str, str]] = None
    ) -> Generator[Tuple[str, List[Tuple[str, str]]], None, None]:
        """Stream response from Ollama API"""
        if not user_input.strip():
            yield "Please enter a message.", chat_history or []
            return
            
        try:
            # Use provided chat history or fallback to instance history
            if chat_history is None:
                chat_history = self.chat_history
            
            # Format the prompt using the selected template
            prompt_template = self.prompt_templates.get(template, "{user_input}")
            formatted_input = prompt_template.format(user_input=user_input)
            
            # Add user message to chat history
            chat_history = chat_history + [(user_input, "")]
            
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
                'stream': True
            }, indent=2)}")
            
            # Call Ollama API with streaming enabled
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
                        "stream": True
                    },
                    stream=True,
                    timeout=120  # Increased timeout to 120 seconds
                )
                
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            if 'message' in chunk and 'content' in chunk['message']:
                                content = chunk['message']['content']
                                if content:
                                    full_response += content
                                    # Update the last message in chat history with the current response
                                    updated_history = chat_history[:-1] + [(chat_history[-1][0], full_response)]
                                    yield "", updated_history
                        except json.JSONDecodeError:
                            continue
                
                # Final update with the complete response
                chat_history[-1] = (chat_history[-1][0], full_response)
                self.chat_history = chat_history  # Update instance history
                return
                
            except requests.exceptions.RequestException as re:
                error_msg = f"Request error: {str(re)}"
                logger.error(f"{error_msg}", exc_info=True)
                yield error_msg, chat_history
                return
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"{error_msg}", exc_info=True)
            yield error_msg, chat_history
            return
    
    def create_playground_interface(self):
        """Create a ChatGPT-like interface for the model playground"""
        
        # Custom CSS for ChatGPT-like styling with colored avatars
        css = """
        /* Avatar styles */
        .user-avatar {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #10a37f;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
            margin-right: 12px;
        }
        
        .bot-avatar {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #6e6e80;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
            margin-right: 12px;
        }
        
        /* Message styles */
        .message {
            display: flex;
            padding: 16px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        
        .message:last-child {
            border-bottom: none;
        }
        
        .message-content {
            flex: 1;
            padding-right: 20px;
        }
        
        /* Typing animation */
        @keyframes typing {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        
        .typing-indicator {
            display: inline-flex;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #888;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        /* Main chat styles */
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
        }
        .header-bar {
            background: #f7f7f8;
            border-bottom: 1px solid #e5e5e5;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .model-selector {
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }
        .chat-messages {
            height: calc(100vh - 200px);
            overflow-y: auto;
            padding: 20px;
        }
        .input-container {
            border-top: 1px solid #e5e5e5;
            padding: 20px;
            background: #ffffff;
        }
        .input-row {
            display: flex;
            align-items: flex-end;
            gap: 12px;
            max-width: 800px;
            margin: 0 auto;
        }
        .message-input {
            flex: 1;
            min-height: 44px;
            max-height: 200px;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 16px;
            resize: none;
            outline: none;
        }
        .send-button {
            background: #10a37f;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 16px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            min-width: 60px;
        }
        .send-button:hover {
            background: #0d8f6f;
        }
        .send-button:disabled {
            background: #d1d5db;
            cursor: not-allowed;
        }
        .settings-panel {
            position: fixed;
            right: 20px;
            top: 20px;
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            width: 280px;
        }
        .new-chat-btn {
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            cursor: pointer;
        }
        .new-chat-btn:hover {
            background: #f9fafb;
        }
        """
        
        with gr.Blocks(
            title="ChatGPT Clone - Ollama",
            css=css,
            theme=gr.themes.Default(
                primary_hue="emerald",
                secondary_hue="gray",
                neutral_hue="gray",
                font=["system-ui", "sans-serif"]
            )
        ) as interface:
            
            # Store chat history in the session state
            chat_history = gr.State([])
            
            # Header with model selection
            with gr.Row(elem_classes="header-bar"):
                with gr.Column(scale=1):
                    gr.HTML("<h2 style='margin: 0; font-size: 18px; font-weight: 600;'>ChatGPT Clone</h2>")
                
                with gr.Column(scale=1):
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            choices=self.list_ollama_models(),
                            value=self.list_ollama_models()[0] if self.list_ollama_models() else None,
                            label="",
                            show_label=False,
                            container=False,
                            elem_classes="model-selector",
                            scale=3
                        )
                        
                        clear_btn = gr.Button(
                            "+ New chat",
                            variant="secondary",
                            elem_classes="new-chat-btn",
                            scale=1
                        )
            
            # Main chat area
            with gr.Column(elem_classes="chat-container"):
                # Chat messages with custom avatars
                chatbot = gr.Chatbot(
                    value=[],
                    height=650,
                    show_label=False,
                    show_copy_button=True,
                    bubble_full_width=False,
                    placeholder="How can I help you today?",
                    container=False,
                    type="messages",
                    elem_classes="chat-messages",
                    avatar_images=(
                        "<div class='user-avatar'>U</div>",  # User avatar
                        "<div class='bot-avatar'>AI</div>"   # Bot avatar
                    )
                )
                
                # Add typing indicator to the chat
                typing_indicator = gr.HTML(
                    "<div class='typing-indicator' style='display: none; padding: 10px 0;'>"
                    "<div class='typing-dot'></div>"
                    "<div class='typing-dot'></div>"
                    "<div class='typing-dot'></div>"
                    "</div>"
                )
            
            # Input area
            with gr.Column(elem_classes="input-container"):
                with gr.Row(elem_classes="input-row"):
                    user_input = gr.Textbox(
                        placeholder="Message ChatGPT Clone...",
                        show_label=False,
                        container=False,
                        scale=6,
                        max_lines=6,
                        elem_classes="message-input",
                        autofocus=True
                    )
                    
                    send_btn = gr.Button(
                        "Send",
                        variant="primary",
                        elem_classes="send-button",
                        scale=1
                    )
            
            # Settings panel (collapsible)
            with gr.Accordion("⚙️ Settings", open=False, elem_classes="settings-panel"):
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
                    label="Temperature",
                    info="Controls randomness"
                )
                
                max_tokens = gr.Slider(
                    minimum=128,
                    maximum=4096,
                    value=2048,
                    step=128,
                    label="Max tokens",
                    info="Maximum response length"
                )
                
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Refresh Models", size="sm")
                
                # System status
                system_info = gr.JSON(
                    value={
                        "Status": "🟢 Connected" if self.list_ollama_models() else "🔴 Disconnected",
                        "Models": len(self.list_ollama_models()),
                        "Memory": f"{psutil.Process().memory_info().rss / 1024 / 1024:.0f}MB"
                    },
                    label="System Status",
                    show_label=True
                )
            
            # Event handlers
            def refresh_models():
                models = self.list_ollama_models()
                status = {
                    "Status": "🟢 Connected" if models else "🔴 Disconnected",
                    "Models": len(models),
                    "Memory": f"{psutil.Process().memory_info().rss / 1024 / 1024:.0f}MB"
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
            ) -> Generator[Tuple[str, List[Dict[str, str]]], None, None]:
                if not message.strip():
                    yield "", history
                    return
                
                try:
                    # Convert history to the format expected by stream_response
                    chat_history = []
                    for msg in history:
                        if msg["role"] == "user":
                            chat_history.append((msg["content"], ""))
                        elif msg["role"] == "assistant" and chat_history:
                            chat_history[-1] = (chat_history[-1][0], msg["content"])
                    
                    # Add current message
                    chat_history.append((message, ""))
                    
                    # Stream the response
                    for _, updated_history in self.stream_response(
                        user_input=message,
                        model_name=model,
                        temperature=temp,
                        max_tokens=tokens,
                        template=template,
                        chat_history=chat_history
                    ):
                        # Convert to the format expected by the Chat component
                        new_history = []
                        for user_msg, bot_msg in updated_history:
                            if user_msg:
                                new_history.append({"role": "user", "content": user_msg})
                            if bot_msg:
                                new_history.append({"role": "assistant", "content": bot_msg})
                        
                        yield "", new_history
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    logger.error(f"Error in process_message: {error_msg}", exc_info=True)
                    history.append({"role": "assistant", "content": error_msg})
                    yield "", history
            
            # Connect components
            refresh_btn.click(
                fn=refresh_models,
                outputs=[model_dropdown, system_info]
            )
            
            clear_btn.click(
                fn=clear_chat,
                outputs=[chatbot, chat_history]
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
                outputs=[user_input, chatbot]
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
                outputs=[user_input, chatbot]
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
                outputs=[model_dropdown, system_info]
            )
            
            return interface
