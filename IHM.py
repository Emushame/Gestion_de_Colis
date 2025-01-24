import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox
)
import requests

API_URL = "http://127.0.0.1:5000"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Colis et Livraisons")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.container = QWidget()
        self.setCentralWidget(self.container)
        layout = QVBoxLayout()

        # Boutons de navigation
        self.btn_utilisateurs = QPushButton("Gérer les Utilisateurs")
        self.btn_utilisateurs.clicked.connect(self.show_utilisateurs)
        layout.addWidget(self.btn_utilisateurs)

        self.btn_colis = QPushButton("Gérer les Colis")
        self.btn_colis.clicked.connect(self.show_colis)
        layout.addWidget(self.btn_colis)

        self.btn_livraisons = QPushButton("Gérer les Livraisons")
        self.btn_livraisons.clicked.connect(self.show_livraisons)
        layout.addWidget(self.btn_livraisons)

        self.container.setLayout(layout)

    def show_utilisateurs(self):
        self.utilisateurs_window = UtilisateursWindow()
        self.utilisateurs_window.show()

    def show_colis(self):
        self.colis_window = ColisWindow()
        self.colis_window.show()

    def show_livraisons(self):
        self.livraisons_window = LivraisonWindow()
        self.livraisons_window.show()


class UtilisateursWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Utilisateurs")
        self.setGeometry(150, 150, 800, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Liste des Utilisateurs")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Email", "Rôle"])
        layout.addWidget(self.table)

        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.clicked.connect(self.load_utilisateurs)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)
        self.load_utilisateurs()

    def load_utilisateurs(self):
        try:
            response = requests.get(f"{API_URL}/utilisateurs/get_utilisateurs")
            if response.status_code == 200:
                utilisateurs_list = response.json()
                self.table.setRowCount(len(utilisateurs_list))
                for row, user in enumerate(utilisateurs_list):
                    self.table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
                    self.table.setItem(row, 1, QTableWidgetItem(user["nom"]))
                    self.table.setItem(row, 2, QTableWidgetItem(user["email"]))
                    self.table.setItem(row, 3, QTableWidgetItem(user["role"]))
            else:
                QMessageBox.critical(self, "Erreur", "Impossible de charger les utilisateurs.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de connexion : {str(e)}")


class ColisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Colis")
        self.setGeometry(150, 150, 800, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Liste des Colis")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Identifiant", "Description", "Etat"])
        layout.addWidget(self.table)

        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.clicked.connect(self.load_colis)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)
        self.load_colis()

    def load_colis(self):
        try:
            response = requests.get(f"{API_URL}/colis")
            if response.status_code == 200:
                colis_list = response.json()
                self.table.setRowCount(len(colis_list))
                for row, colis in enumerate(colis_list):
                    self.table.setItem(row, 0, QTableWidgetItem(str(colis["id"])))
                    self.table.setItem(row, 1, QTableWidgetItem(colis["identifiant_unique"]))
                    self.table.setItem(row, 2, QTableWidgetItem(colis["description"]))
                    self.table.setItem(row, 3, QTableWidgetItem(colis["etat"]))
            else:
                QMessageBox.critical(self, "Erreur", "Impossible de charger les colis.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de connexion : {str(e)}")


class LivraisonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Livraisons")
        self.setGeometry(150, 150, 800, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Liste des Livraisons")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Colis ID", "Livreur ID", "Statut"])
        layout.addWidget(self.table)

        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.clicked.connect(self.load_livraisons)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)
        self.load_livraisons()

    def load_livraisons(self):
        try:
            response = requests.get(f"{API_URL}/livraisons")
            if response.status_code == 200:
                livraison_list = response.json()
                self.table.setRowCount(len(livraison_list))
                for row, livraison in enumerate(livraison_list):
                    self.table.setItem(row, 0, QTableWidgetItem(str(livraison["id"])))
                    self.table.setItem(row, 1, QTableWidgetItem(str(livraison["colis_id"])))
                    self.table.setItem(row, 2, QTableWidgetItem(str(livraison["livreur_id"])))
                    self.table.setItem(row, 3, QTableWidgetItem(livraison["status"]))
            else:
                QMessageBox.critical(self, "Erreur", "Impossible de charger les livraisons.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de connexion : {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
