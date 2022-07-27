# Chess-Tournament

Chess-Tournament est un logiciel de gestion de tournoi.
Il vous permet de créer des tournois, d'y ajouter les
joueurs, créer des rondes de matchs, et sauvergarder les
les résultats pour les visualiser.

## Installation:
  - Créez un fork depuis le dépot github.
  - Installer la dernière version de Python.
  - Installer git bash.
  - Créer un environnement virtuel:
 ```
 python -m venv env
 ```

 1. Activer cet environnemnt:
    - Windows 10:
        - Power Shell:
 		``` 
 		env/Scripts/Activate.ps1
 		```
    	- Ou de préférence si vous avez installé Git(Git Bash MINGW64):
 		```
 		source env/Scripts/activate
 		```
    - Linux Debian 10:
 		```
 		source env/bin/activate
 		```

 2. Installer pip (installation python packages):
    Chess-Tournament requiert certains packages spécifiques.
    Vous devez les installer depuis le fichier requirement.txt.
        commande: pip install -r requirements.txt

 3. Rendez vous dans le dossie racine de l'appli.
    - Windows:
    	```
    	python main.py
    	```
    - Linux:
    	```
    	python3 main.py
    	```

 4. Utilisation:
    - Menu créer un tournoi.
    - Double click sur le tournoi créé.
    - Enregistrer les challengers.
    - Créér une ronde.
    - Ajout des scores à chaques rondes.
    - Visualiser les résultats depuis le menu.

5. Annexe:
    - For view flake8 report:
    	```
    	pip install flake8-html
    	```
    - Then command:
    	```
    	flake8 --format=html --htmldir=flake-report
    	```



                                                                                                                     

