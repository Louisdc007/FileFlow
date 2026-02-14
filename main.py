from file_manager import *
from watchdog.observers import Observer
from settings import *
from time import sleep
from ai_treatment import *

if __name__ == '__main__':
    observer = Observer()
    audit = AuditHandler()
    manager = Manager(observed_folder, sorting_folder)

    observer.schedule(audit, path=observed_folder, recursive=True)
    observer.start()

    ai = AiAnalyser(ollama_model)

    try:
        while True:
            sleep(0.1)
            if audit.last_created_files:
                current_file = audit.last_created_files.pop(0)
                print(f"Analyse : {current_file}")
                
                if str(current_file).endswith('.c') or str(current_file).endswith('.h'):
                    ai.result = 'DOCUMENTS/EPITA/PROG'
                    print("-> Prog sans IA")
                elif any(i in str(current_file).lower() for i in ['cv', 'lm', 'lettre de motivation', 'lettre motivation', 'motivation', 'lettredemotivation', 'lettre_de_motivation']):
                    ai.result = 'DOCUMENTS/CV'
                    print("-> CV sans IA")
                elif any(i in str(current_file) for i in ['elec', 'tension', 'courant', 'ohm', 'circuit']):
                    ai.result = "DOCUMENTS/EPITA/ELEC"
                    print("-> CV sans IA")
# --- BLOCS MATIÈRES EPITA ---

                elif any(i in str(current_file).lower() for i in ['algo', 'tri', 'graphe', 'complexite']):
                    ai.result = "DOCUMENTS/EPITA/ALGO"
                    print("-> ALGO sans ia")

                elif any(i in str(current_file).lower() for i in ['mat', 'analyse', 'algebre', 'proba', 'geometrie']):
                    ai.result = "DOCUMENTS/EPITA/MAT"
                    print("-> MAT sans ia")

                elif any(i in str(current_file).lower() for i in ['elec', 'tension', 'courant', 'ohm', 'signal']):
                    ai.result = "DOCUMENTS/EPITA/ELEC"
                    print("-> ELEC sans ia")

                elif any(i in str(current_file).lower() for i in ['prog', 'exercice', 'tp_', 'rendu', 'code']):
                    ai.result = "DOCUMENTS/EPITA/PROG"
                    print("-> PROG sans ia")

                elif any(i in str(current_file).lower() for i in ['archi', 'assembleur', 'asm', 'processeur', 'logique']):
                    ai.result = "DOCUMENTS/EPITA/ARCHI"
                    print("-> ARCHI sans ia")

                elif any(i in str(current_file).lower() for i in ['ang', 'english', 'toeic', 'vocabulaire']):
                    ai.result = "DOCUMENTS/EPITA/ANG"
                    print("-> ANG sans ia")
                else:
                    ai.analysis(current_file)
                    print(f"Résultat IA : {ai.result}")
                
                if ai.result and ai.result.upper() != "NONE":
                    manager.move(current_file, ai.result)
                    print(f"Déplacé vers : {ai.result}")
                
                    send_notification(
        title="FileFlow - Tri Automatique",
        message=f"{current_file} ➜ {ai.result}"
    )
                
    except KeyboardInterrupt:
        observer.stop()
    observer.join()