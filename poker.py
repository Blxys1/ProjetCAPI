from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTextEdit, QFormLayout, QInputDialog)
from PyQt5.QtCore import Qt
import sys
import json
from models.players import Player
from models.game import Game

class PokerGameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planning Poker Game")
        self.setGeometry(100, 100, 800, 600)
        self.game = None
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_layout(self.main_layout)
        
        title_label = QLabel("Bienvenue dans l'application Planning Poker", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(title_label)

        new_game_btn = QPushButton("Nouvelle Partie", self)
        new_game_btn.clicked.connect(self.show_new_game_form)
        self.main_layout.addWidget(new_game_btn)

        load_game_btn = QPushButton("Charger une Partie", self)
        load_game_btn.clicked.connect(self.load_game)
        self.main_layout.addWidget(load_game_btn)

        quit_btn = QPushButton("Quitter", self)
        quit_btn.clicked.connect(self.close)
        self.main_layout.addWidget(quit_btn)

    def show_new_game_form(self):
        self.clear_layout(self.main_layout)
        form_layout = QFormLayout()
        
        self.players_input = QLineEdit(self)
        self.players_input.setPlaceholderText("Entrez le nombre de joueurs")
        form_layout.addRow("Nombre de joueurs :", self.players_input)

        self.rule_input = QLineEdit(self)
        self.rule_input.setPlaceholderText("Entrez la règle (strict, average, median, ...)")
        form_layout.addRow("Règle :", self.rule_input)

        self.start_btn = QPushButton("Démarrer la Partie", self)
        self.start_btn.clicked.connect(self.start_game)
        form_layout.addRow(self.start_btn)
        
        self.main_layout.addLayout(form_layout)

    def start_game(self):
        try:
            num_players = int(self.players_input.text())
            rule = self.rule_input.text().strip().lower()
            if num_players < 2:
                raise ValueError("Nombre de joueurs invalide.")
            if rule not in ["strict", "average", "median", "absolute_majority", "relative_majority"]:
                raise ValueError("Règle invalide.")

            self.game = Game(num_players=num_players, rules=rule)
            for i in range(num_players):
                pseudo, ok = QInputDialog.getText(self, "Configuration des joueurs", f"Entrez un pseudonyme pour le joueur {i+1}:")
                if not ok or not pseudo:
                    raise ValueError("Pseudonyme invalide.")
                self.game.players.append(Player(pseudo))
            self.show_voting_interface()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def show_voting_interface(self):
        self.clear_layout(self.main_layout)

        if not self.game.backlog:
            QMessageBox.information(self, "Info", "Aucune tâche dans le backlog.")
            self.show_main_menu()
            return

        feature = self.game.backlog.pop(0)
        self.game.current_feature = feature

        feature_label = QLabel(f"Fonctionnalité actuelle : {feature['description']}", self)
        feature_label.setAlignment(Qt.AlignCenter)
        feature_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(feature_label)

        self.vote_inputs = {}
        form_layout = QFormLayout()
        for player in self.game.players:
            vote_input = QLineEdit(self)
            self.vote_inputs[player.pseudo] = vote_input
            form_layout.addRow(f"Vote de {player.pseudo} :", vote_input)
        
        submit_btn = QPushButton("Soumettre les votes", self)
        submit_btn.clicked.connect(self.submit_votes)
        form_layout.addRow(submit_btn)

        self.main_layout.addLayout(form_layout)

    def submit_votes(self):
        try:
            for player in self.game.players:
                vote = self.vote_inputs[player.pseudo].text()
                player.vote(vote)

            if self.game.process_votes():
                QMessageBox.information(self, "Validation", f"Fonctionnalité '{self.game.current_feature['description']}' validée!")
            else:
                QMessageBox.warning(self, "Revote", "Pas de validation. Re-vote requis.")
                self.game.reset_votes()
                self.show_voting_interface()
                return

            if self.game.backlog:
                self.show_voting_interface()
            else:
                QMessageBox.information(self, "Partie terminée", "Toutes les fonctionnalités sont validées!")
                self.game.save_final_report()
                self.show_main_menu()
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def load_game(self):
        try:
            self.game = Game(num_players=0)
            self.game.load_game_state("data/game_state.json")
            QMessageBox.information(self, "Chargement réussi", "La partie a été chargée avec succès!")
            self.show_voting_interface()
        except FileNotFoundError:
            QMessageBox.warning(self, "Erreur", "Aucune sauvegarde trouvée.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PokerGameUI()
    main_window.show()
    sys.exit(app.exec_())
