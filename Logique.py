from matplotlib import pyplot as plt
import MachineLearning 
import random

class LogicGame(object):
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 1000

    def __init__(self, MachineLearning):
        self.obstacle_speed = 10
        self.game_speed = 1
        self.score = 0
        self.ml_score = -1
        self.current_tick = 0
        self.obstacle_interval = random.randint(120, 180)  # en ticks
        self.last_obstacle_tick = 0
        self.dino = LogicDino()
        self.obstacles = []
        self.next_obstacle_id = 0
        self.MachineLearning = MachineLearning
        self.dino.update()

    def spawn_obstacle(self):
        obstacle_count = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05], k=1)[0]
        initial_x = self.SCREEN_WIDTH * 2
        obstacle = LogicObstacle(self.next_obstacle_id, initial_x, self.SCREEN_HEIGHT, self.obstacle_speed, obstacle_count)
        self.obstacles.append(obstacle)
        self.next_obstacle_id += 1
        self.last_obstacle_tick = self.current_tick

    def collide(self):
        for obstacle in self.obstacles:
            if (self.dino.rect["x"] < obstacle.rect["x"] + obstacle.rect["width"] and
                self.dino.rect["x"] + self.dino.rect["width"] > obstacle.rect["x"] and
                self.dino.rect["y"] < obstacle.rect["y"] + obstacle.rect["height"] and
                self.dino.rect["y"] + self.dino.rect["height"] > obstacle.rect["y"]):
                return True
        return False
    
    def MachineLearningUpdate(self, type):
        obstacle_rect = self.obstacles[0].rect if len(self.obstacles) > 0 else {"x": 2000, "y": 0}
        if type == "Dino":
            output = self.MachineLearning.neron_calcul([obstacle_rect["x"], self.obstacle_speed * self.game_speed])
            return output[0]

    def update(self):
        self.dino.mouvement(self.MachineLearningUpdate("Dino"))
        self.dino.update()
        for obstacle in self.obstacles:
            if obstacle.update(game_speed=self.game_speed):
                self.obstacles.remove(obstacle)
        
        self.score += 1
        self.game_speed = 1 + self.score / 500

        if self.collide():
            return False

        # Vérifie si le temps écoulé depuis le dernier obstacle dépasse l'intervalle défini
        self.current_tick += 1
        if self.current_tick - self.last_obstacle_tick >= self.obstacle_interval:
            self.spawn_obstacle()
            self.obstacle_interval = random.uniform(120, 180)  # Redéfinit l'intervalle en secondes
            self.ml_score += 1

        return True

    def get_obstacles(self):
        return self.obstacles


class LogicObstacle(object):
    size = { 
            1 : {"width": 105, "height": 70, "offset_x": 446, "offset_y": 0},
            2 : {"width": 105, "height": 70, "offset_x": 549, "offset_y": 0},
            3 : {"width": 150, "height": 100, "offset_x": 652, "offset_y": 0},
            4 : {"width": 150, "height": 100, "offset_x": 802, "offset_y": 0}
            }

    def __init__(self, id, x, y, speed=10, obstacles_id=1):
        self.id = id
        self.obstacles_id = obstacles_id
        self.speed = speed
        self.rect = {
            "x": x,
            "y": y - LogicObstacle.size[obstacles_id]["height"] - 7,
            "width": LogicObstacle.size[obstacles_id]["width"],
            "height": LogicObstacle.size[obstacles_id]["height"]
        }

    def update(self, **kwargs):
        game_speed = kwargs.get("game_speed", 1)
        self.rect["x"] -= self.speed * game_speed
        return self.rect["x"] < -20

    def getX(self):
        return self.rect["x"]

    def getY(self):
        return self.rect["y"]

    def setX(self, x):
        self.rect["x"] = x

    def setY(self, y):
        self.rect["y"] = y

    def __str__(self):
        return f"Obstacle at x = {self.rect['x']} and y = {self.rect['y']}"

    def __repr__(self):
        return self.__str__()

class LogicDino(object):
    size = {"width": 88, "height": 93}

    def __init__(self):
        self.tile_size = 49
        self.offset = 3
        self.rect = {
            "x": 50,
            "y": LogicGame.SCREEN_HEIGHT - 100,
            "width": LogicDino.size["width"],
            "height": LogicDino.size["height"]
        }
        self.is_jumping = False
        self.jump_speed = -20  # Negative for upward movement
        self.gravity = 1

    def update(self):
        if self.is_jumping:
            self.rect["y"] += self.jump_speed
            self.jump_speed += self.gravity

        if self.rect["y"] >= LogicGame.SCREEN_HEIGHT - 100:
            self.rect["y"] = LogicGame.SCREEN_HEIGHT - 100
            self.is_jumping = False
            self.jump_speed = -20  # Reset jump speed

    def mouvement(self, jump):
        if jump >= 1 and not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = -20
        if jump <= -1 and self.is_jumping:
            self.jump_speed = 20

    def getX(self):
        return self.rect["x"]

    def getY(self):
        return self.rect["y"]

    def setX(self, x):
        self.rect["x"] = x

    def setY(self, y):
        self.rect["y"] = y

    def __str__(self):
        return f"Dino at x = {self.rect['x']} and y = {self.rect['y']}"

    def __repr__(self):
        return self.__str__()
    

import matplotlib.pyplot as plt
import random

class LogicSimulation(object):
    def __init__(self, generations_num=100, population_num=100, neron_couche=[2,4,4,1], mutation_rate=0.1):
        self.generations_num = generations_num
        self.population_num = population_num
        self.mutation_rate = mutation_rate
        self.population = { x : MachineLearning.Ml(
            neron_couche=neron_couche,
            mutation_rate=mutation_rate
        ) for x in range(population_num)}
        self.game_population = { x : LogicGame(pop) for x, pop in self.population.items()}
        self.score = { x : 0 for x in range(population_num)}
        self.score_best = 0
        self.best_ML = self.population[0]

        self.score_history = {
            "best_scores": [],
            "average_scores": [],
            "all_scores": []
        }

        # Initialiser le graphique
        self.init_plot()

        self.new_generation()

    def init_plot(self):
        # Configurer les graphiques en temps réel
        plt.ion()  # Mode interactif on
        self.fig, (self.ax_main, self.ax_small) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

        # Ligne pour les meilleurs scores et les scores moyens
        self.best_scores_line, = self.ax_main.plot([], [], label="Best Score")
        self.avg_scores_line, = self.ax_main.plot([], [], label="Average Score")

        # Configuration du graphique principal
        self.ax_main.set_xlim(0, self.generations_num)
        self.ax_main.set_xlabel("Generation")
        self.ax_main.set_ylabel("Score")
        self.ax_main.legend()

        # Configuration du petit graphique secondaire
        self.ax_small.set_xlim(0, self.generations_num)
        self.ax_small.set_xlabel("Generation")
        self.ax_small.set_ylabel("All Scores")
        self.ax_small.set_title("All Scores per Generation")

    def update_plot(self):
        # Mettre à jour les données du graphique principal
        self.best_scores_line.set_xdata(range(len(self.score_history["best_scores"])))
        self.best_scores_line.set_ydata(self.score_history["best_scores"])
        self.avg_scores_line.set_xdata(range(len(self.score_history["average_scores"])))
        self.avg_scores_line.set_ydata(self.score_history["average_scores"])

        # Mise à jour du petit graphique secondaire
        for i, gen_scores in enumerate(self.score_history["all_scores"]):
            self.ax_small.scatter([i] * len(gen_scores), gen_scores, color='blue', s=1)

        # Réajuster les limites et rafraîchir les affichages
        self.ax_main.relim()
        self.ax_main.autoscale_view()
        self.ax_small.relim()
        self.ax_small.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self):
        game_to_remove = []

        for index in range(len(self.game_population)):
            if self.game_population[index] is not None and self.game_population[index].update() == False:
                game_to_remove.append(index)
                self.score[index] = self.game_population[index].ml_score

        for index in sorted(game_to_remove, reverse=True):
            self.game_population[index] = None

        if all(game is None for game in self.game_population.values()):
            local_best, local_index = max((value, index) for index, value in self.score.items())
            if local_best >= self.score_best:
                self.score_best = local_best
                self.best_ML = self.population[local_index]
            print(f"Best score: {self.score_best}")
            avg_score = sum(self.score.values()) / len(self.score)
            print(f"Average score: {avg_score}")

            # Enregistrer les scores dans l'historique
            self.score_history["best_scores"].append(self.score_best)
            self.score_history["average_scores"].append(avg_score)
            self.score_history["all_scores"].append(list(self.score.values()))

            self.update_plot()  # Mettre à jour les graphiques après chaque génération

            self.new_generation()

            if self.generations_num == 0:
                return False
            else:
                self.generations_num -= 1
        return True

    def new_generation(self):
        self.score = { x : 0 for x in range(self.population_num)}
        for id, child in self.population.items():
            child.setConection(self.best_ML.connection)
            child.setNeronWeight(self.best_ML.neron_weight)
            child.neron_update()
            self.game_population[id] = LogicGame(child)

        print(f"Generation {self.generations_num} created with {len(self.game_population)} games")

    def get_game(self):
        return LogicGame(self.best_ML)


if __name__ == "__main__":
    sim = LogicSimulation( generations_num=100, population_num=500, neron_couche=[2,4,4,1], mutation_rate=0.1)
    while True:
        if sim.update() == False:
            break