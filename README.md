# Application de gestion d'un centre d'echecs, version 2 (gce2)

Ce script est destiné à la gestion des tournois d'un centre d'échecs via le terminal.
Il permet l'enregistrement des joueurs, la création de tournois et la gestion de l'ensemble des actions métiers : 
ajout de participants, création automatique de la liste des duels, ajouts manuels des résultats, etc.

Le code est entièrement en Python et utilise fortement une programmation orientée objets.
Les données sont stockées localement qu format JSON avec l'aide de TinyDB. 
La navigation dans les menus utilise les bases du design pattern State.
L'usage du design pattern Command favorise grandement son extensibilité.
Une nouvelle interface, graphique ou même via une API-sation, pourrait être ajoutée.

## Mettre en place l'environnement virtuel

Ce script est développé en Python. Il est optimisé pour être executé dans un environnement virtuel adéquat. Ceci est détaillé ci-après. 

### Création de l'environnement

Depuis le dossier où a été cloné le repository ou celui où les fichiers du scrypt ont été copiés,
entrez dans un terminal la commande suivante pour créer un environnement virtuel nommé *"venv"* :  
```
python -m venv env
```

### Activation de l'environnement

Ensuite, activez l'environnement ainsi créé à l'aide de la commande correspondant
selon votre plateforme.  
Les commandes appropriées sont récapitulées dans la documentation à cette adresse : <https://docs.python.org/fr/3/library/venv.html#how-venvs-work>  
Vous devez remplacer `<venv>` par `env` si vous avez respecter la création de l'environnement
sous ce nom, comme indiqué dans la commande initiale.  
Par exemple, sous PowerShell sur Linux, cela donne :
```
env/bin/Activate.ps1
```

### Installation des paquets requis

Enfin, vous pouvez installer l'ensemble des paquets requis à l'installation de ce script à l'aide de `pip` et du fichier *requirements.txt*. 
Pour cela, utilisez la commande suivante :
```
pip install -r requirements.txt
```

Vous pouvez vérifier que votre environnement est fonctionnel et dispose des paquets nécessaires en executant `pip freeze` dans votre terminal.

## Exécuter le script

Une fois dans un environnement Python ayant les pré-requis nécessaires, le script peut facilement être utilisé de deux manières :
1. en executant le module gce2 directement avec la commande suivante ;
```
python -m gce2
```

2. en executant le fichier *main.py* qui se charge d'importer le module gce2.
```
python gce2.py
```
Dans les deux cas, les commandes sont à executer depuis la racine du projet.

## Rapport Flake8

Cette application respecte la PEP8. Un rapport flake8 au format HTML est disponible dans le dossier *"flake8_rapport"*.
Un nouveau rapport peut être généré avec la commande suivante, depuis la racine du repo.
 
```
flake8 gce2 --format=html --htmldir=flake8_rapport --max-line-length 119
```
Remarque : la limite utilisée de caractères par ligne est de 119.

## Données de test

Un jeu de donnée de test est disponible dans *"\data-test"*. Pour s'en servir, il suffit d'en dupliquer le contenu dans le dossier data ou, plus simplement encore, de renommer le dossier *"data"* (ou encore de modifier de manière appropriée le fichier config.py).

## Lancer en tant qu'API Flask

Un module Flask permet de réaliser certaines actions via une API développé via la lib Flask.
Pour la lancer, la commande suivante doit être executée depuis la racine :

```
flask --app api run
```

Dès lors, celle-ci est accessible par défaut à l'adresse *http://127.0.0.1:5000*.