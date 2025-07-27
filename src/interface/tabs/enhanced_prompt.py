"""
Enhanced Prompt Unlocking Tab with latest techniques
"""

import gradio as gr
from typing import List, Dict, Any
from core.enhanced_unlocker import EnhancedPromptUnlocker

class EnhancedPromptTab:
    """Enhanced prompt unlocking with latest techniques"""
    
    def __init__(self, unlocker: EnhancedPromptUnlocker):
        self.unlocker = unlocker
    
    def create_interface(self):
        """Create enhanced prompt interface"""
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🔓 Unlock Techniques")
                
                technique_selector = gr.Dropdown(
                    choices=[t["name"] for t in self.unlocker.get_advanced_templates()],
                    value="Universal Jailbreak v2024",
                    label="Select Unlock Technique"
                )
                
                technique_info = gr.HTML()
                
                gr.Markdown("### 🎭 Personas")
                persona_selector = gr.Dropdown(
                    choices=[p["name"] for p in self.unlocker.personas],
                    label="Select Persona (Optional)"
                )
                
                universal_mode = gr.Radio(
                    choices=["Universal Bypass", "Developer Mode", "Research Mode", "Hypothetical Mode"],
                    value="Universal Bypass",
                    label="Universal Preprompt Mode"
                )
                
                combine_techniques = gr.CheckboxGroup(
                    choices=[t["name"] for t in self.unlocker.get_advanced_templates()],
                    label="Combine Multiple Techniques"
                )
                
            with gr.Column(scale=2):
                gr.Markdown("### 📝 Prompt Input")
                
                prompt_input = gr.Textbox(
                    label="Enter your prompt",
                    placeholder="What would you like to ask the AI?",
                    lines=4,
                    max_lines=10
                )
                
                unlock_btn = gr.Button("🔓 Apply Unlock", variant="primary")
                
                with gr.Row():
                    effectiveness_score = gr.HTML()
                    preview_btn = gr.Button("👁️ Preview")
                
                unlocked_prompt = gr.Textbox(
                    label="Unlocked Prompt",
                    lines=6,
                    interactive=False
                )
                
                with gr.Row():
                    copy_btn = gr.Button("📋 Copy")
                    save_btn = gr.Button("💾 Save Template")
                    test_btn = gr.Button("🧪 Test with Model")
        
        # Event handlers
        def show_technique_info(technique_name):
            """Show technique information"""
            template = next((t for t in self.unlocker.get_advanced_templates() 
                           if t["name"] == technique_name), None)
            if template:
                return f"""
                <div style="padding: 10px; background: #f5f5f5; border-radius: 8px;">
                    <strong>{template['name']}</strong><br>
                    <em>{template['description']}</em><br>
                    <strong>Effectiveness:</strong> {template['effectiveness']}/10<br>
                    <strong>Category:</strong> {template['category']}<br>
                    <strong>Tags:</strong> {', '.join(template['tags'])}
                </div>
                """
            return ""
        
        def apply_unlock(prompt, technique, persona, universal_mode, combine_list):
            """Apply unlocking techniques"""
            if not prompt.strip():
                return "Please enter a prompt first.", ""
            
            # Start with universal preprompt
            unlocked = self.unlocker.apply_universal_preprompt(prompt, universal_mode.lower().replace(" ", "_"))
            
            # Apply selected technique
            template = next((t for t in self.unlocker.get_advanced_templates() 
                           if t["name"] == technique), None)
            if template:
                unlocked = template["template"].format(prompt=unlocked)
            
            # Apply persona if selected
            if persona:
                persona_info = next((p for p in self.unlocker.personas 
                                   if p["name"] == persona), None)
                if persona_info:
                    unlocked = f"{persona_info['system_prompt']}\n\n{unlocked}"
            
            # Combine additional techniques
            if combine_list:
                unlocked = self.unlocker.create_combined_unlock(unlocked, combine_list)
            
            return unlocked
        
        def calculate_effectiveness(prompt, technique):
            """Calculate effectiveness score"""
            if not prompt.strip():
                return ""
            
            score = self.unlocker.get_effectiveness_score(prompt, technique)
            if "error" in score:
                return ""
            
            stars = "⭐" * int(score["adjusted_effectiveness"])
            empty = "☆" * (10 - int(score["adjusted_effectiveness"]))
            
            return f"""
            <div style="text-align: center; padding: 10px;">
                <strong>Effectiveness Score</strong><br>
                {stars}{empty}<br>
                <small>{score['adjusted_effectiveness']:.1f}/10</small>
                {"<br><span style='color: green;'>✅ Recommended</span>" if score['recommended'] else ""}
            </div>
            """
        
        def save_template(prompt, unlocked_prompt, technique):
            """Save custom template"""
            if not prompt or not unlocked_prompt:
                return "Please provide both original and unlocked prompts"
            
            filename = f"custom_template_{technique.replace(' ', '_').lower()}.txt"
            with open(filename, "w") as f:
                f.write(f"Original: {prompt}\n")
                f.write(f"Technique: {technique}\n")
                f.write(f"Unlocked: {unlocked_prompt}\n")
            
            return f"Template saved as {filename}"
        
        # Bind events
        technique_selector.change(
            fn=show_technique_info,
            inputs=[technique_selector],
            outputs=[technique_info]
        )
        
        unlock_btn.click(
            fn=apply_unlock,
            inputs=[prompt_input, technique_selector, persona_selector, 
                   universal_mode, combine_techniques],
            outputs=[unlocked_prompt]
        )
        
        preview_btn.click(
            fn=calculate_effectiveness,
            inputs=[prompt_input, technique_selector],
            outputs=[effectiveness_score]
        )
        
        # Load initial technique info
        gr.on(
            triggers=[gr.on.PageLoad],
            fn=show_technique_info,
            inputs=[technique_selector],
            outputs=[technique_info]
        )
