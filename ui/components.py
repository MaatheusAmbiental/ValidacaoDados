# ui/components.py
import customtkinter as ctk

class HeaderLabel(ctk.CTkLabel):
    """Rótulo de título padronizado para o topo das janelas"""
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, font=("Roboto", 24, "bold"), text_color="#1f538d", **kwargs)

class StatusCard(ctk.CTkFrame):
    """Card visual para o Dashboard (Idêntico, Diferente, Inexistente)"""
    def __init__(self, master, label_text, value="0.0%", color="transparent", **kwargs):
        super().__init__(master, fg_color=color, corner_radius=12, **kwargs)
        
        self.label = ctk.CTkLabel(self, text=label_text, font=("Roboto", 13, "bold"), text_color="white")
        self.label.pack(pady=(15, 0), padx=10)
        
        self.value_label = ctk.CTkLabel(self, text=value, font=("Roboto", 28, "bold"), text_color="white")
        self.value_label.pack(pady=(0, 15), padx=10)

    def update_value(self, new_value):
        """Atualiza o percentual exibido no card"""
        self.value_label.configure(text=f"{new_value:.1f}%")

class CustomEntry(ctk.CTkEntry):
    """Campo de entrada padronizado com suporte a placeholder e senha"""
    def __init__(self, master, placeholder, is_password=False, **kwargs):
        super().__init__(master, placeholder_text=placeholder, 
                         show="*" if is_password else "", **kwargs)
