# Planning Poker Application

## Description
L'application Planning Poker est un outil conçu pour faciliter l'estimation collaborative des fonctionnalités d'un backlog, en suivant les principes agiles. Elle offre une interface utilisateur simple, des règles flexibles de vote, et des fonctionnalités pour sauvegarder et charger les parties en cours.

## Fonctionnalités Principales

### 1. Menu Principal
- **Créer une nouvelle partie** :
  - Saisie du nombre de joueurs.
  - Attribution de pseudonymes.
  - Choix du mode de jeu parmi les options disponibles (strict, moyenne, médiane, majorité absolue, majorité relative).
- **Charger une partie** :
  - Chargement d'un fichier JSON contenant l'état d'une partie sauvegardée.

### 2. Système de Vote
- Modes de jeu disponibles :
  - **Mode Strict** : Vote jusqu'à ce qu'un consensus soit atteint.
  - **Mode Moyenne** : Utilisation de la moyenne des votes après le premier tour.
  - **Mode Médiane** : Calcul de la médiane des votes pour valider une fonctionnalité.
  - **Mode Majorité Absolue** : Validation si plus de 50% des joueurs votent pour la même valeur.
  - **Mode Majorité Relative** : Validation si une valeur obtient plus de votes que les autres.
- Gestion des fonctionnalités non validées pour un nouveau tour de vote.

### 3. Sauvegarde et Chargement
- Sauvegarde automatique après chaque action critique (vote, création de partie).
- Chargement d'une partie depuis un fichier JSON.

### 4. Rapport Final
- Génération automatique du rapport à la fin de la partie.
- Affichage des fonctionnalités validées et des estimations collectées.

## Prérequis
- **Python 3.8+**
- **Bibliothèques Python** :
  - `tkinter`
  - `pytest` (pour les tests unitaires)

## Installation
1. Clonez le dépôt :
   ```bash
   git clone <url-du-repo>
   ```
2. Accédez au répertoire du projet :
   ```bash
   cd planning-poker
   ```
3. Installez les dépendances nécessaires (si applicable).

## Utilisation
1. Lancez l'application :
   ```bash
   python app.py
   ```
2. Suivez les instructions dans l'interface pour commencer une nouvelle partie.

## Tests Unitaires
- Les tests unitaires sont disponibles dans le fichier `test_game.py`.
- Exécutez les tests avec la commande suivante :
  ```bash
  pytest test_game.py
  ```

## Documentation
- La documentation est générée automatiquement avec Doxygen.
- Pour générer la documentation, exécutez :
  ```bash
  doxygen Doxyfile
  ```

## Contributeurs
- Balkis Ferjani
- Yasmine Maddouri




