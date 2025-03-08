#!/usr/bin/python3

import os
import sys
import subprocess

class Librarian:
    def __init__(self, env_name='jonso'):
        self.env_name = env_name

    def check_environment(self):
        venv_name = os.environ.get('VIRTUAL_ENV')
        
        if not venv_name or os.path.basename(venv_name) != self.env_name:
            raise Exception("You should run this script inside venv named jonso")


    def install_libraries(self):
        print("Installing libraries")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


    def display_installed_libraires(self):
        print("Installed libraries:")
        
        result = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        
        print(result)


    def save_requirements(self):
        print("Saving list of installed packages into requirements.txt")

        with open("requirements.txt", "w") as file:
            subprocess.check_call([sys.executable, "-m", "pip", "freeze", "-r", "requirements.txt"], stdout=file)


    def archive_env(self):
        env_path = os.environ.get("VIRTUAL_ENV")
        archive_name = f"{self.env_name}_env"

        subprocess.check_call(["tar", "czf", f"{archive_name}.tar.gz", env_path])


if __name__ == '__main__':
    librarian = Librarian()

    try:
        librarian.check_environment()

        librarian.install_libraries()

        librarian.display_installed_libraires()

        # librarian.save_requirements()

        # librarian.archive_env()
    except subprocess.CalledProcessError as e:
        print(f'Error while installing packages: {e}')
    except Exception as e:
        print(f'Error: {e}')
    