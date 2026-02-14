from openai import OpenAI
from settings import ollama_url, ollama_model
import json
import re

class AiAnalyser():
    def __init__(self, gen_model):
        self.result = None
        self.client = OpenAI(base_url=ollama_url, api_key="ollama")
        self.model = gen_model

    def analysis(self, file_name):
        prompt = f"""
Tu es un automate de classification strict. Analyse le nom du fichier et retourne UNIQUEMENT un objet JSON.
Structure : {{"folder": "CHEMIN"}}

LISTE DES DOSSIERS AUTORISÉS (À utiliser en priorité) :
- DOCUMENTS/EPITA/MAT
- DOCUMENTS/EPITA/ELEC
- DOCUMENTS/EPITA/ANG
- DOCUMENTS/EPITA/ALGO
- DOCUMENTS/EPITA/ARCHI
- DOCUMENTS/EPITA/PROG
- DOCUMENTS/CV/

EXEMPLE DE COMPORTEMENT :
- "td_algebre_lineaire.pdf" -> {{"folder": "DOCUMENTS/EPITA/MAT"}}
- "projet_python_v3.py" -> {{"folder": "DOCUMENTS/EPITA/PROG"}}
- "fiche_paie_janvier.pdf" -> {{"folder": "DOCUMENTS/ADMIN"}}
- "vacances_corse.jpg" -> {{"folder": "IMAGES/VACANCES"}}
- "rapport_stage.pdf" -> {{"folder": "DOCUMENTS/STAGE}}

RÈGLES :
1. Si le nom évoque une matière EPITA (mon école), utilise STRICTEMENT un dossier de la liste ci-dessus.
2. N'invente pas de nouveaux dossiers pour les matières déjà listées (ex: n'utilise pas "MATHS" si "MAT" existe).
3. Ne mets pas de "/" au début du chemin.
4. Ne confond pas ALGO (pseudo code, opti) et PROG (fichiers codes, binaires)
5. Crée un nouveau dossier UNIQUEMENT si aucun deja créé ne correspond

finalement, a toi de voir ce qui te semble le plus logique. Cherche les /le mot clé et identifie dans quel domaine il a le plus de sens (filtre a plus de sens avec ELEC pour un ingé).

Fichier à analyser : {file_name}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            
            raw_content = response.choices[0].message.content
            if raw_content is None:
                self.result = "None"
                return
            
            raw_content = raw_content.strip()
            
            # Extraction du JSON par sécurité
            match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                self.result = data.get("folder", "None")
            else:
                self.result = "None"

        except Exception as e:
            print(f"ERREUR IA : {e}")
            self.result = "None"