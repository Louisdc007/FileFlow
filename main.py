from google.genai.types import AuthConfigOidcConfig

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

    ai = AiAnalyser("gemini-2.5-flash")

    try:
        while True:
            sleep(0.1)
            if audit.last_created_files:
                print(audit.last_created_files)
                ai.analysis(audit.last_created_files[-1])
                print(ai.result)
                manager.move(audit.last_created_files[-1], ai.result)
                print(audit.last_created_files.pop())
    except KeyboardInterrupt:
        observer.stop()
    observer.join()