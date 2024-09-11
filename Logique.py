from matplotlib import pyplot as plt
import MachineLearning 
import random
import copy

class LogicGame:
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 1000

    def __init__(self, machine_learning):
        self.obstacle_speed = 10
        self.game_speed = 1
        self.score = 0
        self.ml_score = -1
        self.current_tick = 0
        self.obstacle_interval = random.randint(120, 180)
        self.last_obstacle_tick = 0
        self.dino = LogicDino()
        self.obstacles = []
        self.next_obstacle_id = 0
        self.machine_learning = machine_learning
        self.dino.update()

    def spawn_obstacle(self):
        obstacle_count = random.choices([x for x in range(5)], weights=[0.2, 0.1, 0.1,0.1, 0.5])[0]
        obstacle = LogicObstacle(self.next_obstacle_id, 5000, self.SCREEN_HEIGHT, self.obstacle_speed, obstacle_count)
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

    def machine_learning_update(self):
        if self.obstacles:
            obstacle = self.obstacles[0]
            obstacle_data = [obstacle.rect["x"], obstacle.rect["y"], self.obstacle_speed * self.game_speed, self.dino.rect["y"]]
        else:
            obstacle_data = [5000, 0, -1, self.dino.rect["y"]]
        output = self.machine_learning.neron_calcul(obstacle_data)
        return output[0]

    def update(self):
        self.dino.mouvement(self, self.machine_learning_update)
        self.dino.update()
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.update(game_speed=self.game_speed)]
        self.score += 1
        self.game_speed = 1 + self.score / 500

        if self.collide():
            return False

        self.current_tick += 1
        if self.current_tick - self.last_obstacle_tick >= self.obstacle_interval:
            self.spawn_obstacle()
            self.obstacle_interval = random.uniform(120, 180)
            self.ml_score += 1

        return True

    def get_obstacles(self):
        return self.obstacles
class LogicObstacle:
    size = { 
        0 : {"width": 105, "height": 70, "offset_x": 446, "offset_y": 0},
        1 : {"width": 105, "height": 70, "offset_x": 549, "offset_y": 0},
        2 : {"width": 150, "height": 100, "offset_x": 652, "offset_y": 0},
        3 : {"width": 150, "height": 100, "offset_x": 802, "offset_y": 0},
        4 : {"width": 92, "height": 80, "offset_x": 259, "offset_y": 2}
        }

    def __init__(self, id, x, y, speed=10, obstacle_id=1):
        self.id = id
        self.obstacle_id = obstacle_id
        self.speed = speed
        size = LogicObstacle.size[obstacle_id]
        self.rect = {
            "x": x,
            "y": y - size["height"] - 130 if obstacle_id == 4 else y - size["height"],
            "width": size["width"],
            "height": size["height"]
        }

    def update(self, **kwargs):
        game_speed = kwargs.get("game_speed", 1)
        self.rect["x"] -= self.speed * game_speed
        return self.rect["x"] < -self.rect["width"]

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
class LogicDino:
    size = {"width": 88, "height": 93}

    def __init__(self):
        self.rect = {
            "x": 50,
            "y": LogicGame.SCREEN_HEIGHT - 100,
            "width": self.size["width"],
            "height": self.size["height"]
        }
        self.is_jumping = False
        self.jump_speed = -20
        self.gravity = 1

    def update(self):
        if self.is_jumping:
            self.rect["y"] += self.jump_speed
            self.jump_speed += self.gravity
        if self.rect["y"] >= LogicGame.SCREEN_HEIGHT - 100:
            self.rect["y"] = LogicGame.SCREEN_HEIGHT - 100
            self.is_jumping = False
            self.jump_speed = -20

    def mouvement(self, logic, machine_learning_update):
        jump = machine_learning_update()
        if jump >= 2/3 and not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = -20
        elif jump <= -2/3 and self.is_jumping:
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
class LogicSimulation:
    def __init__(self, generations_num=100, population_num=100, population_same_num=1, neron_couche=[4, 4, 4, 1], mutation_rate=0.1):
        self.generations_num = generations_num
        self.generations_count = 0
        self.population_num = population_num
        self.population_same_num = population_same_num
        self.mutation_rate = mutation_rate

        # Initialisation des populations et jeux
        self.population = self.initialize_population(neron_couche, mutation_rate)
        self.game_population = self.initialize_games()
        self.score = self.initialize_scores()

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

    def initialize_population(self, neron_couche, mutation_rate):
        """Initialise la population avec les paramètres donnés."""
        return {x: MachineLearning.Ml(neron_couche=neron_couche, mutation_rate=mutation_rate) for x in range(self.population_num)}

    def initialize_games(self):
        """Initialise plusieurs jeux pour chaque IA de la population."""
        game_population = {}
        for x, pop in self.population.items():
            for i in range(self.population_same_num):
                game_population[f"{x}_{i}"] = LogicGame(pop)
        print(f"Initialised {len(game_population)} games across {self.population_num} IA models")
        return game_population

    def initialize_scores(self):
        """Initialise les scores pour chaque IA, avec plusieurs instances."""
        return {f"{x}_{i}": 0 for x in range(self.population_num) for i in range(self.population_same_num)}

    def init_plot(self):
        """Configure les graphiques pour suivre les performances de l'IA en temps réel."""
        plt.ion()  # Mode interactif on
        self.fig, (self.ax_main, self.ax_small) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

        # Graphiques des scores
        self.best_scores_line, = self.ax_main.plot([], [], label="Best Score")
        self.avg_scores_line, = self.ax_main.plot([], [], label="Average Score")

        self.ax_main.set_xlim(0, self.generations_num)
        self.ax_main.set_xlabel("Generation")
        self.ax_main.set_ylabel("Score")
        self.ax_main.legend()

        self.ax_small.set_xlim(0, self.generations_num)
        self.ax_small.set_xlabel("Generation")
        self.ax_small.set_ylabel("All Scores")
        self.ax_small.set_title("All Scores per Generation")

    def update_plot(self):
        """Met à jour les graphiques en temps réel."""
        self.best_scores_line.set_xdata(range(len(self.score_history["best_scores"])))
        self.best_scores_line.set_ydata(self.score_history["best_scores"])
        self.avg_scores_line.set_xdata(range(len(self.score_history["average_scores"])))
        self.avg_scores_line.set_ydata(self.score_history["average_scores"])

        for i, gen_scores in enumerate(self.score_history["all_scores"]):
            self.ax_small.scatter([i] * len(gen_scores), gen_scores, color='blue', s=1)

        self.ax_main.relim()
        self.ax_main.autoscale_view()
        self.ax_small.relim()
        self.ax_small.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self):
        """Met à jour la simulation en vérifiant les jeux et en créant de nouvelles générations si nécessaire."""
        game_to_remove = [index for index in self.game_population if self.game_population[index] and not self.game_population[index].update()]

        for index in game_to_remove:
            self.score[index] = self.game_population[index].ml_score
            self.game_population[index] = None

        if all(game is None for game in self.game_population.values()):
            self.process_generation_end()
            self.new_generation()
            if self.generations_num == self.generations_count:
                return False
            self.generations_count += 1
        return True

    def process_generation_end(self):
        """Traite la fin d'une génération en trouvant les meilleurs scores et en mettant à jour l'historique."""
        # Calculer le score moyen par IA
        aggregated_scores = {}
        variance = {}
        for x in range(self.population_num):
            scores_for_ia = [self.score[f"{x}_{i}"] for i in range(self.population_same_num)]
            aggregated_scores[x] = sum(scores_for_ia) / len(scores_for_ia)
            variance[x] = sum((score - aggregated_scores[x]) ** 2 for score in scores_for_ia) / len(scores_for_ia)
            aggregated_scores[x] = aggregated_scores[x]

        local_best, local_index = max((value, index) for index, value in aggregated_scores.items())

        if local_best >= self.score_best:
            self.score_best = local_best
            self.best_ML = copy.deepcopy(self.population[local_index])

        avg_score = sum(aggregated_scores.values()) / len(aggregated_scores)
        print(f"Best score: {self.score_best}")
        print(f"Average score: {avg_score}")

        self.score_history["best_scores"].append(self.score_best)
        self.score_history["average_scores"].append(avg_score)
        self.score_history["all_scores"].append(list(aggregated_scores.values()))

        self.update_plot()

    def new_generation(self):
        """Crée une nouvelle génération basée sur la meilleure IA de la génération précédente."""
        self.score = self.initialize_scores()

        for id, child in self.population.items():
            child.setConection(self.best_ML.connection)
            child.setNeronWeight(self.best_ML.neron_weight)
            child.neron_update()
            for i in range(self.population_same_num):
                self.game_population[f"{id}_{i}"] = LogicGame(child)

        print(f"Generation {self.generations_num} created with {len(self.game_population)} games")

    def get_game(self):
        """Retourne une copie du jeu avec la meilleure IA."""
        return copy.deepcopy(LogicGame(self.best_ML))

if __name__ == "__main__":
    sim = LogicSimulation( generations_num=100, population_num=500, neron_couche=[4,4,4,1], mutation_rate=0.1)
    while True:
        if sim.update() == False:
            break