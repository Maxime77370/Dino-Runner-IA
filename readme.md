# 🦖 Simulation de Jeu Dino Runner avec IA et Machine Learning

## Table des matières
1. [Description du Projet](#description-du-projet)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Structure du Projet](#structure-du-projet)
6. [Simulation avec ou sans Interface Graphique](#simulation-avec-ou-sans-interface-graphique)
7. [Algorithmes d'Apprentissage](#algorithmes-dapprentissage)
8. [Contributions](#contributions)
9. [Licence](#licence)
10. [Contact](#contact)

---

## Description du Projet

Ce projet est une **simulation de jeu Dino Runner** où une intelligence artificielle est entraînée à jouer grâce à des techniques d'apprentissage automatique. L'IA contrôle un dinosaure qui doit éviter des obstacles dans un environnement similaire au célèbre jeu **Google Dino**. Ce projet inclut des algorithmes de **réseaux de neurones artificiels** pour que l'IA améliore ses performances au fil des générations. Une version sans interface graphique permet également d'accélérer l'entraînement.

---

## Fonctionnalités

- **IA autonome** : Le dinosaure est contrôlé par une IA qui prend des décisions en temps réel.
- **Réseaux de neurones** : Utilisation de réseaux de neurones pour le traitement des données d'entrée.
- **Apprentissage par génération** : L'IA améliore ses performances en suivant un processus d'évolution générationnelle.
- **Simulation avec interface graphique** : Visualisation en temps réel de la progression du jeu.
- **Simulation sans interface graphique** : Version optimisée pour un entraînement rapide de l'IA sans afficher le jeu.
- **Suivi des performances** : Graphiques en temps réel des progrès de l'IA au fil des générations.

---

## Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/Maxime77370/Dino-Runner-IA.git
   cd dino-runner-ia
   ```

2. **Installer les dépendances :**
   Assurez-vous d'avoir Python 3.x et installez les bibliothèques nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer l'environnement :**
   - Placez les ressources graphiques dans le dossier `assets/`.
   - Configurez les paramètres d'entraînement dans le fichier `config.py` selon vos besoins.

---

## Utilisation

### 1. Lancer la simulation avec interface graphique :
Pour voir le jeu en temps réel avec l'IA qui joue, utilisez la commande suivante :
```bash
python main.py --gui
```

### 2. Lancer la simulation sans interface graphique :
Si vous souhaitez entraîner l'IA plus rapidement sans afficher le jeu :
```bash
python main.py --no-gui
```

### 3. Suivi des performances :
Les graphiques des performances sont mis à jour en temps réel lorsque la simulation est active. Vous pouvez les visualiser dans la fenêtre ou en utilisant un outil de visualisation de logs.

---

## Structure du Projet

Le projet est organisé comme suit :

```
dino-runner-ia/
│
├── assets/                 # Fichiers et ressources graphiques
├── components/             # Composants supplémentaires comme les sliders et polices
├── save/                   # Sauvegardes des données d'entraînement
├── Dinosaur.py             # Classe gérant les mouvements du dinosaure
├── Logique.py              # Logique du jeu et de la simulation
├── MachineLearning.py      # Algorithmes d'apprentissage et IA
├── main.py                 # Script principal pour lancer la simulation
├── requirements.txt        # Bibliothèques Python requises
└── README.md               # Fichier README
```

- **`Dinosaur.py`** : Gère le dinosaure (position, mouvement, sauts).
- **`Logique.py`** : Contient la logique du jeu et les règles (collisions, obstacles, score).
- **`MachineLearning.py`** : Contient les algorithmes de réseaux de neurones et la logique d'apprentissage.
- **`assets/`** : Contient les fichiers graphiques nécessaires pour la version avec interface.

---

## Simulation avec ou sans Interface Graphique

Le projet propose deux modes d'entraînement pour l'IA :

1. **Avec Interface Graphique** : 
   - Permet de visualiser en temps réel le dinosaure qui saute les obstacles. 
   - Plus lente, car elle affiche chaque étape du jeu.
   
2. **Sans Interface Graphique** : 
   - Permet d’entraîner l'IA en arrière-plan sans afficher la simulation.
   - Idéale pour des entraînements plus rapides, car elle se concentre uniquement sur le calcul des performances.

Pour changer de mode, il suffit de passer l’option `--gui` ou `--no-gui` lors de l'exécution du script principal.

---

## Algorithmes d'Apprentissage

Le projet utilise un **réseau de neurones** simple pour déterminer si le dinosaure doit sauter ou non en fonction de la position des obstacles et de la vitesse du jeu.

- **Entraînement par renforcement** : L'IA apprend de ses erreurs en ajustant les poids des connexions neuronales.
- **Mutation** : À la fin de chaque génération, les meilleures IA sont sélectionnées pour générer une nouvelle population en appliquant de légères mutations aux poids des neurones, favorisant l'amélioration continue.

---

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez proposer des améliorations ou signaler des problèmes, veuillez ouvrir une **issue** ou soumettre une **pull request**.

---

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

---

## Contact

Si vous avez des questions ou souhaitez discuter du projet, n'hésitez pas à me contacter via LinkedIn ou par email à [maxime.carpentier@epitech.eu](mailto:maxime.carpentier@epitech.eu).

---

**Merci de votre intérêt pour ce projet !** 😊

