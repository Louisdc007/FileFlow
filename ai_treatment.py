from google import genai
from settings import api_key

class AiAnalyser():
    def __init__(self, gen_model):
        self.result = None
        self.client = genai.Client(api_key=api_key)
        self.model = gen_model

    def analysis(self, file_name):
        prompt = f"""
Tu es un classificateur de fichier, tu ne devras retourner que les noms suivant en majuscules en fonction de ce que tu analyses sur le nom du fichier :
- DOCUMENTS/EPITA/MAT
- DOCUMENTS/EPITA/ELEC
- DOCUMENTS/EPITA/ANG
- DOCUMENTS/EPITA/ALGO
- DOCUMENTS/EPITA/ARCHI
- DOCUMENTS/EPITA/PROG
- None

 Tu te situes à la racine /, a toi de voir si tu as un document (ou une image ou autre) et donc de construire le chemin pour le classer. Tu as ici tous les dossiers deja créé, a utiliser en priorité, tous représente une matière que j'ai en cours. Répond 'None' si tu ne sais pas quoi faire du fichier. Tu peux créer un dossier si tu le veux, pour cela retourne juste le nom du dossier, exemple : tu veux classer le fichier conjugaison_italien.pdf, alors retourne DOCUMENTS/COURS/ITALIEN

voila le fichier à analyser : {file_name}.
"""
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            self.result = response.text.strip().upper()

        except Exception as e:
            print(f"ERREUR IA : {e}")

