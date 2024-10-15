from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
import numpy as np

# Repræsenterer hver agent i mængden, som flytter sig tilfældigt til en nabocelle for hvert trin.
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = 1  # Hver agent har en hastighedsattribut (selvom den ikke er brugt her)

    def step(self):
        # Definerer bevægelsesregler for hver person
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filtrer mulige skridt, så scenen (række 0) ikke er inkluderet
        filtered_steps = [pos for pos in possible_steps if pos[0] != 0]  # Agenter kan ikke gå til række 0 (scenen)
        
        if filtered_steps:  # Kun flyt, hvis der er mulige skridt tilbage
            new_position = self.random.choice(filtered_steps)
            self.model.grid.move_agent(self, new_position)

# Styrer simulationen, opretter et gitter og placerer agenterne i det. Den sørger også for at køre simulationen trin for trin.
class CrowdModel(Model):
    def __init__(self, N, width, height):
        super().__init__()

        self.num_agents = N  # Antallet af agenter
        self.grid = MultiGrid(width, height, True)  # Opretter et grid med de givne dimensioner (wrap-around = True)
        self.schedule = RandomActivation(self)  # Random scheduler, der vælger agenternes rækkefølge tilfældigt

        # Opret n agenter
        for i in range(self.num_agents):
            person = Person(i, self)  # Opretter en ny agent med unik ID
            self.schedule.add(person)  # Tilføjer agenten til scheduler'en

            # Tilføjer agenten til en tilfældig position på grid'et, men ikke på scenen (række 0)
            x = self.random.randrange(1, self.grid.width)  # Start fra række 1 (gulvet), ikke række 0 (scenen)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(person, (x, y))

    def step(self):
        # Avancerer modellen ét trin
        self.schedule.step()

# Funktion til at visualisere grid'et som en koncertsal
def visualize_model(crowd_model, step_number):
    grid = np.zeros((crowd_model.grid.width, crowd_model.grid.height))

    # Sætter agenterne på grid'et
    for agent in crowd_model.schedule.agents:
        x, y = agent.pos
        grid[x][y] = 1  # Markér agentens position

    # Opret en koncertsal med en scene (øverst) og udgange (hjørner)
    concert_hall = np.zeros_like(grid)

    # Markerer scenen (øverste række, bredt som hele gitteret)
    concert_hall[0, :] = 0.5  # Lys grå farve for scenen

    # Markerer udgange (hjørner)
    concert_hall[-1, 0] = 0.75  # Udgang i nederste venstre hjørne (lysere grå)
    concert_hall[-1, -1] = 0.75  # Udgang i nederste højre hjørne

    # Kombiner koncertsalen og crowdens bevægelser
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 1:  # Hvis der er en agent
                concert_hall[x, y] = 1  # Farv den som en agent (mørk blå)

    # Visualiser grid'et
    plt.figure(figsize=(6, 6))
    plt.imshow(concert_hall, interpolation='nearest', cmap='Blues')  # Brug farveskemaet Blues
    plt.title(f"Step {step_number}", fontsize=16)
    plt.grid(True, color="black")  # Tilføj grid-linjer for at vise sektioner
    plt.xticks([])  # Fjern x-aksen
    plt.yticks([])  # Fjern y-aksen
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()

# Opretter en instans af CrowdModel med 50 agenter og et 10x10 grid
crowd = CrowdModel(50, 10, 10)

# Kører simulationen i 20 trin med visualisering af koncertsal
for i in range(20):
    crowd.step()  # Kører ét trin af simulationen
    visualize_model(crowd, i + 1)  # Visualiser grid'et for hvert trin med trin nummer