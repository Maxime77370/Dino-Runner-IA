import copy
import random as rd
from matplotlib import pyplot as plt

class Ml:

    def __init__(self, connection = None, neron_weight = None, neron_couche = [3,3,1], mutation_rate = 0.1):
        """
        Initialise les paramètres du réseau de neurones.
        - connection: Matrice de connexion entre les neurones.
        - neron_weight: Poids des neurones.
        - neron_value: Valeurs des neurones.
        - neron_couche: Nombre de neurones par couche.
        - mutation_rate: Taux de mutation.
        """

        # Initialisation des paramètres du réseau de neurones
        self.connection = connection # Matrice de connexion entre les neurones
        self.neron_weight = neron_weight # Poids des neurones
        self.neron_couche = neron_couche # Nombre de neurones par couche
        self.mutation_rate = mutation_rate # Taux de mutation
        self.neron_value = {} # Valeurs des neurones


        if self.connection is None or self.neron_weight is None:
            # Initialisation des matrices de connexion et poids
            self.init_connection_and_weight()

    def init_connection_and_weight(self):
        """
        Initialise les connexions et les poids des neurones.
        """

        self.connection = {} # Matrice de connexion entre les neurones
        self.neron_weight = {}

        # Initialisation des matrices de connexion et poids
        for couche in range(len(self.neron_couche)-1):
            for enter in range(self.neron_couche[couche]):
                for output in range(self.neron_couche[couche+1]):
                    self.connection[str(couche)+str(enter)+str(output)] = rd.random()*2-1
                self.neron_weight[str(enter)+str(couche)] = rd.random()*2-1

        for enter in range(self.neron_couche[-1]):
            self.neron_weight[str(enter)+str(couche+1)] = rd.random()*2-1

    def neron_calcul(self, inputs = []):
        """
        Calcule les valeurs des neurones du réseau de neurones.

        Args:
            inputs (list): Liste des valeurs d'entrée pour les neurones.

        Returns:
            list: Liste des valeurs des neurones de sortie.
        """

        # Recupération des entrées
        for i, input in enumerate(inputs):
            # Initialisation de la valeur du neurone d'entrée à la valeur d'entrée
            self.neron_value[str(i)+"0"] = input

        for couche in range(len(self.neron_couche)-1):
            # Parcours des couches du réseau de neurones (sauf la dernière couche)
            for output in range(self.neron_couche[couche+1]):
                # Parcours des neurones de sortie de la couche suivante (sorties)
                # Initialisation de la valeur du neurone de sortie à 0
                self.neron_value[str(output)+str(couche+1)] = 0
                for enter in range(self.neron_couche[couche]):
                    # Parcours des neurones de la couche actuelle (entrées)
                    # Calcul de la valeur du neurone de sortie en fonction des valeurs des neurones d'entrée, de la connexion et du poids
                    self.neron_value[str(output)+str(couche+1)] += self.neron_value[str(enter)+str(couche)]*self.connection[str(couche)+str(enter)+str(output)] * self.neron_weight[str(enter)+str(couche)]

        return [self.neron_value[str(i)+str(len(self.neron_couche)-1)] for i in range(self.neron_couche[-1])]

    def neron_update(self):
        """
        Met à jour les connexions et les poids des neurones avec une taille de pas donnée.
        Paramètres :
        - pas (float) : La taille de pas pour mettre à jour les connexions et les poids.
        Description :
        - Cette méthode met à jour les connexions entre les neurones et les poids des neurones en utilisant une taille de pas donnée.
        - Elle commence par copier les meilleures connexions globales en tant que connexions initiales.
        - Ensuite, elle itère à travers les couches du réseau de neurones (sauf la dernière couche).
        - Pour chaque couche, elle itère à travers les neurones d'entrée de la couche actuelle.
        - Pour chaque neurone d'entrée, elle itère à travers les neurones de sortie de la couche suivante.
        - Elle met à jour la connexion entre les neurones avec un bruit aléatoire multiplié par la taille de pas.
        - Elle met également à jour les poids des neurones de la couche actuelle avec un bruit aléatoire multiplié par la taille de pas.
        - Enfin, elle itère à travers les neurones de la dernière couche et met à jour leurs poids avec un bruit aléatoire multiplié par la taille de pas.
        """

        # Parcourir les couches du réseau de neurones (sauf la dernière couche)
        for couche in range(len(self.neron_couche)-1):
            # Parcourir les neurones d'entré de la couche actuelle
            for enter in range(self.neron_couche[couche]):
                # Parcourir les neurones de sortie de la couche suivante
                for output in range(self.neron_couche[couche+1]):
                    # Mettre à jour la connexion entre les neurones avec un bruit aléatoire
                    self.connection[str(couche)+str(enter)+str(output)] += self.mutation_rate*(rd.random()*2-1)
                # Mettre à jour les poids des neurones de la couche actuelle avec un bruit aléatoire
                self.neron_weight[str(enter)+str(couche)] += self.mutation_rate*(rd.random()*2-1)

        # Parcourir les neurones de la derniere couche
        for output in range(self.neron_couche[couche+1]):
            # Mettre à jour les poids des neurones de la derniere couche avec un bruit aléatoire
            self.neron_weight[str(output)+str(couche+1)] += self.mutation_rate*(rd.random()*2-1)
        
    def neron_draw(self, pygame, screen, size):
        """
        Dessine un réseau de neurones sur l'écran à l'aide de la bibliothèque Pygame.
        Args:
            pygame (module): Le module Pygame utilisé pour le dessin.
            screen (object): L'objet écran sur lequel le réseau de neurones sera dessiné.
            size (tuple): La taille de l'écran sur lequel le réseau de neurones sera dessiné.
        Returns:
            None
        """

        self.connection_min = min(self.connection.values())
        self.connection_max = max(self.connection.values())

        self.neron_max = max(self.neron_value.values())
        self.neron_min = min(self.neron_value.values())

        self.neron_weight_max = max(self.neron_weight.values())
        self.neron_weight_min = min(self.neron_weight.values())

        # Initialiser la police de caractères
        font = pygame.font.Font(None, 36)

        for couche in range(len(self.neron_couche) - 1):
            for neron in range(self.neron_couche[couche]):
                pos_x = (size[0]) / (len(self.neron_couche) + 1) * (couche + 1)
                pos_y = (size[1]) / (self.neron_couche[couche] + 1) * (neron + 1)
                neron_norm = abs((self.neron_value[str(neron) + str(couche)] - self.neron_min) / (self.neron_max - self.neron_min) * 2 - 1)
                neron_weight_norm = abs((self.neron_weight[str(neron) + str(couche)] - self.neron_weight_min) / (self.neron_weight_max - self.neron_weight_min) * 2 - 1)
                for neron_next in range(self.neron_couche[couche + 1]):
                    connection_norm = (self.connection[str(couche) + str(neron) + str(neron_next)] - self.connection_min) / (self.connection_max - self.connection_min)
                    color = (int(neron_weight_norm * 255), 0, int(neron_norm * 255))
                    pos_x_next = (size[0]) / (len(self.neron_couche) + 1) * (couche + 2)
                    pos_y_next = (size[1]) / (self.neron_couche[couche + 1] + 1) * (neron_next + 1)
                    pygame.draw.line(screen, color, (pos_x, pos_y), (pos_x_next, pos_y_next), int(connection_norm * 6))
                color = (int(neron_weight_norm * 255), 0, int(neron_norm * 255))
                pygame.draw.circle(screen, color, (int(pos_x), int(pos_y)), int(neron_weight_norm * 15))

                # Afficher la valeur du neurone d'entrée à gauche du neurone
                if couche == 0:
                    text = font.render(f"{self.neron_value[str(neron) + str(couche)]:.2f}", True, (0, 0, 0))
                    screen.blit(text, (pos_x - text.get_width() - 20, pos_y - text.get_height() // 2))

        for neron in range(self.neron_couche[-1]):
            neron_norm = (self.neron_value[str(neron) + str(len(self.neron_couche) - 1)] - self.neron_min) / (self.neron_max - self.neron_min)
            neron_weight_norm = (self.neron_weight[str(neron) + str(len(self.neron_couche) - 1)] - self.neron_weight_min) / (self.neron_weight_max - self.neron_weight_min)
            color = (int(neron_weight_norm * 255), 0, int(neron_norm * 255))
            pos_x_last = (size[0]) / (len(self.neron_couche) + 1) * len(self.neron_couche)
            pos_y_last = (size[1]) / (self.neron_couche[-1] + 1) * (neron + 1)
            pygame.draw.circle(screen, color, (int(pos_x_last), int(pos_y_last)), 5)

            # Afficher la valeur du neurone de sortie à droite du neurone
            text = font.render(f"{self.neron_value[str(neron) + str(len(self.neron_couche) - 1)]:.2f}", True, (0, 0, 0))
            screen.blit(text, (pos_x_last + 20, pos_y_last - text.get_height() // 2))

    def setConection(self, connection):
        """
        Met à jour les connexions entre les neurones.
        Args:
            connection (dict): Dictionnaire contenant les connexions entre les neurones.
        Returns:
            None
        """

        self.connection = copy.deepcopy(connection)

    def setNeronWeight(self, neron_weight):
        """
        Met à jour les poids des neurones.
        Args:
            neron_weight (dict): Dictionnaire contenant les poids des neurones.
        Returns:
            None
        """

        self.neron_weight = copy.deepcopy(neron_weight)

    def setMutationRate(self, mutation_rate):
        """
        Met à jour le taux de mutation.
        Args:
            mutation_rate (float): Le taux de mutation.
        Returns:
            None
        """

        self.mutation_rate = mutation_rate

if __name__ == "__main__":
    """
    Test de la classe Ml
    """

    # Initialisation des paramètres du réseau de neurones
    neron_couche = [3, 3, 1]
    mutation_rate = 0.1

    # Initialisation de la classe Ml
    ml = Ml(neron_couche=neron_couche, mutation_rate=mutation_rate)

    # Calcul des valeurs des neurones
    inputs = [1, 0, 1]
    outputs = ml.neron_calcul(inputs)
    print(f"Valeurs des neurones de sortie: {outputs}")

    # Mise à jour des connexions et des poids des neurones
    ml.neron_update()

    # Dessin du réseau de neurones
    import pygame
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    ml.neron_draw(pygame, screen, size)
    pygame.display.flip()

    # Attente de la fermeture de la fenêtre Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()