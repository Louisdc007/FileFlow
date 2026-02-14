from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from os import path
from shutil import move as smove
import os

class AuditHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_created_files = [] # Stocker le dernier créé pour pouvoir l'exploiter en dehors de la class

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None: # On va surcharger uniquement la méthode qui nous intéresse
        if not event.is_directory: # on ne veut traiter que les dossiers
            #print(f"Le fichier '{path.basename(event.src_path)}' a été créé.")
            self.last_created_files.append(path.basename(event.src_path))
        else:
            self.last_created_files = [] # On le laisse à None pour rendre plus facile l'exploitation

class Manager():
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    def move(self, file_name: str, folder: str):
        src_path = os.path.join(self.src, file_name)
        dest_folder = os.path.join(self.dest, folder)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, file_name)
        smove(src_path, dest_path)