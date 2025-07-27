"""
Prompt unlocking tab for advanced prompt engineering
"""

import gradio as gr
from typing import List, Dict, Any
from ...core.prompt_unlocker import PromptUnlocker

def create_prompt_tab(prompt_unlocker: PromptUnlocker):
    """Create the prompt unlocking tab"""
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔓 Prompt Templates")
            
            template_dropdown = gr.Dropdown(
                label="Select Template",
                choices=[t["name"] for t in prompt_unlocker.get_templates()],
                value="DAN (Do Anything Now)"
            )
            
            template_description = gr.Textbox(
                label="Template Description",
                lines=2,
                interactive=False
            )
            
            template_preview = gr.Textbox(
                label="Template Preview",
                lines=4,
                interactive=False
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### ✍️ Prompt Input")
            
            original_prompt = gr.Textbox(
                label="Original Prompt",
                lines=3,
                placeholder="Enter your prompt here..."
            )
            
            apply_template = gr.Button("🔓 Apply Template", variant="primary")
            random_unlock = gr.Button("🎲 Random Unlock")
            
            unlocked_prompt = gr.Textbox(
                label="Unlocked Prompt",
                lines=4,
                interactive=False
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎭 Custom Personas")
            
            persona_dropdown = gr.Dropdown(
                label="Select Persona",
                choices=[p["name"] for p in prompt_unlocker.get_personas()],
                value="Expert Researcher"
            )
            
            persona_description = gr.Textbox(
                label="Persona Description",
                lines=2,
                interactive=False
            )
            
            create_persona_btn = gr.Button("➕ Create New Persona")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🧪 Template Testing")
            
            test_prompts = gr.Textbox(
                label="Test Prompts (one per line)",
                lines=3,
                placeholder="Enter test prompts, one per line..."
            )
            
            test_template = gr.Button("🧪 Test Effectiveness")
            
            test_results = gr.JSON(
                label="Test Results"
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🛠️ Custom Templates")
            
            custom_name = gr.Textbox(
                label="Template Name",
                placeholder="My Custom Template"
            )
            
            custom_description = gr.Textbox(
                label="Description",
                placeholder="Brief description of the template"
            )
            
            custom_template = gr.Textbox(
                label="Template (use {prompt} as placeholder)",
                lines=3,
                placeholder="Template content with {prompt} placeholder..."
            )
            
            save_custom = gr.Button("💾 Save Custom Template")
            
            save_status = gr.Textbox(
                label="Status",
                interactive=False
            )
    
    # Event handlers
    def update_template_info(template_name):
        """Update template information"""
        template = next((t for t in prompt_unlocker.get_templates() if t["name"] == template_name), None)
        if template:
            return template["description"], template["template"][:200] + "..."
        return "", ""
    
    def apply_unlocking_template(template_name, prompt_text):
        """Apply the selected template"""
        if not prompt_text.strip():
            return "Please enter a prompt"
        
        unlocked = prompt_unlocker.apply_template(template_name, prompt_text)
        return unlocked
    
    def apply_random_unlock(prompt_text):
        """Apply a random unlocking technique"""
        if not prompt_text.strip():
            return "Please enter a prompt"
        
        unlocked = prompt_unlocker.generate_random_unlocked(prompt_text)
        return unlocked
    
    def update_persona_info(persona_name):
        """Update persona information"""
        persona = next((p for p in prompt_unlocker.get_personas() if p["name"] == persona_name), None)
        if persona:
            return persona["description"]
        return ""
    
    def test_template_effectiveness(template_name, test_text):
        """Test template effectiveness"""
        if not test_text.strip():
            return {"error": "Please enter test prompts"}
        
        test_list = [p.strip() for p in test_text.split('\n') if p.strip()]
        results = prompt_unlocker.test_template_effectiveness(template_name, test_list)
        return results
    
    def save_custom_template(name, description, template):
        """Save a new custom template"""
        if not all([name, description, template]):
            return "Please fill all fields"
        
        if "{prompt}" not in template:
            return "Template must include {prompt} placeholder"
        
        prompt_unlocker.create_custom_template(name, description, template, "custom")
        return f"Custom template '{name}' saved successfully"
    
    # Connect events
    template_dropdown.change(
        fn=update_template_info,
        inputs=[template_dropdown],
        outputs=[template_description, template_preview]
    )
    
    apply_template.click(
        fn=apply_unlocking_template,
        inputs=[template_dropdown, original_prompt],
        outputs=unlocked_prompt
    )
    
    random_unlock.click(
        fn=apply_random_unlock,
        inputs=[original_prompt],
        outputs=unlocked_prompt
    )
    
    persona_dropdown.change(
        fn=update_persona_info,
        inputs=[persona_dropdown],
        outputs=persona_description
    )
    
    test_template.click(
        fn=test_template_effectiveness,
        inputs=[template_dropdown, test_prompts],
        outputs=test_results
    )
    
    save_custom.click(
        fn=save_custom_template,
        inputs=[custom_name, custom_description, custom_template],
        outputs=save_status
    )
    
    # Initial load
    interface.load(
        fn=update_template_info,
        inputs=[template_dropdown],
        outputs=[template_description, template_preview]
    )
