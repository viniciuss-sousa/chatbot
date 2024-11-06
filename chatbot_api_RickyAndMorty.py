import customtkinter as ctk
import requests
import unicodedata
import random

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Gasparzinho - Rick and Morty")
        master.geometry("600x500")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Oi! Eu sou o Gasparzinho. Digite o nome de um personagem ou episódio de Rick and Morty e eu te conto tudo sobre ele!\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite o nome de um personagem ou episódio...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="purple", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nVocê: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        # Processar a entrada do usuário
        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nGasparzinho: " + response + "\n")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def normalize_string(self, s):
        # Remover acentos e converter para minúsculas
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()

    def get_response(self, user_input):
        user_input_normalized = self.normalize_string(user_input)

        # Tokens básicos para identificar a pergunta
        prepositions = ["de", "do", "da"]
        tokens = [word for word in user_input_normalized.split() if word not in prepositions]

        if "olá" in tokens or "oi" in tokens:
            return "Olá! Em que posso ajudar?"
        elif "tchau" in tokens or "até logo" in tokens:
            return "Até mais! Se precisar de algo, estou aqui."
        elif "como" in tokens and ("você" in tokens or "está" in tokens):
            return "Estou ótima, obrigada por perguntar!"
        elif "qual" in tokens and "nome" in tokens:
            return "Eu sou o Gasparzinho, seu assistente do universo Rick and Morty."
        elif "ajuda" in tokens or "socorro" in tokens:
            return "Claro! Estou aqui para ajudar. O que você precisa?"

        # Tentando buscar informações de personagens ou episódios
        character_name = None
        episode_name = None

        for token in tokens:
            if token in ["personagem", "personagens", "rick", "morty", "summer", "beth", "jerry"]:
                character_name = token
            if token in ["episódio", "episodios", "temporada"]:
                episode_name = token

        if character_name:
            try:
                response = requests.get(f"https://rickandmortyapi.com/api/character/?name={character_name}")
                if response.status_code == 200:
                    data = response.json()
                    if data['results']:
                        character = data['results'][0]
                        return f"Encontrei o personagem: {character['name']}! \nEspécie: {character['species']} \nStatus: {character['status']} \nOrigem: {character['origin']['name']}"
                    else:
                        return f"Não encontrei nenhum personagem com o nome '{character_name}'."
                else:
                    return "Erro ao tentar acessar a API de personagens. Tente novamente mais tarde."
            except requests.exceptions.RequestException as e:
                return f"Ops, deu problema na conexão com a API: {e}. 😖"
        
        if episode_name:
            try:
                response = requests.get(f"https://rickandmortyapi.com/api/episode/?name={episode_name}")
                if response.status_code == 200:
                    data = response.json()
                    if data['results']:
                        episode = data['results'][0]
                        return f"Episódio: {episode['name']} \nTemporada: {episode['season']} \nData de lançamento: {episode['air_date']}"
                    else:
                        return f"Não encontrei nenhum episódio com o nome '{episode_name}'."
                else:
                    return "Erro ao tentar acessar a API de episódios. Tente novamente mais tarde."
            except requests.exceptions.RequestException as e:
                return f"Ops, deu problema na conexão com a API: {e}. 😖"

        return "Desculpe, não entendi. Poderia reformular a pergunta?"

if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
