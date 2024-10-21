from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Repræsenterer hver agent i mængden, som flytter sig tilfældigt til en nabocelle for hvert trin.
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = 1  # Hver agent har en hastighedsattribut (selvom den ikke er brugt her)

    def step(self):
        # Definerer bevægelsesregler for hver person
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filtrer mulige skridt, så scenen ikke er inkluderet
        filtered_steps = [pos for pos in possible_steps if not self.model.is_stage(pos)]  # Agenter kan ikke gå til scenen
        
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

            # Tilføjer agenten til en tilfældig position på grid'et, men ikke på scenen
            x = self.random.randrange(1, self.grid.width)  # Start fra række 1 (gulvet), ikke række 0 (scenen)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(person, (x, y))

    def step(self):
        # Avancerer modellen ét trin
        self.schedule.step()

    # Funktion til at afgøre, om en position er på scenen (forbudt område)
    def is_stage(self, pos):
        x, y = pos
        # Definer området for scenen (den sorte boks)
        # Juster disse værdier baseret på scenens faktiske position på dit grid
        stage_area = [
            (0, 1), (0, 2), (0, 3),  # Eksempel: Scenen er i venstre del af gitteret
            # Tilføj flere koordinater, som dækker det sorte område
        ]
        return (x, y) in stage_area

# Funktion til at visualisere grid'et som en koncertsal med baggrundsbillede
def visualize_model_with_background(crowd_model, step_number, background_image):
    grid = np.zeros((crowd_model.grid.width, crowd_model.grid.height))

    # Sætter agenterne på grid'et
    for agent in crowd_model.schedule.agents:
        x, y = agent.pos
        grid[x][y] = 1  # Markér agentens position

    # Indlæs baggrundsbilledet og vis det
    img = Image.open(background_image)
    plt.figure(figsize=(6, 6))
    plt.imshow(img, extent=[0, crowd_model.grid.width, crowd_model.grid.height, 0])  # Extent matcher gridets dimensioner

    # Visualiser agenterne ovenpå baggrunden
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 1:  # Hvis der er en agent
                plt.scatter(y + 0.5, x + 0.5, color='blue', s=100)  # Placer agenterne (justér størrelsen hvis nødvendigt)

    # Tilføj ekstra detaljer som scene og udgange
    plt.title(f"Step {step_number}", fontsize=16)
    plt.grid(True, color="black")  # Tilføj grid-linjer for at vise sektioner
    plt.xticks([])  # Fjern x-aksen
    plt.yticks([])  # Fjern y-aksen
    plt.show(block=False)
    plt.pause(1)
    plt.close()

# Opretter en instans af CrowdModel med 50 agenter og et 10x10 grid
crowd = CrowdModel(50, 10, 10)

# Kører simulationen i 20 trin med visualisering af koncertsal med baggrundsbillede
for i in range(20):
    crowd.step()  # Kører ét trin af simulationen
    visualize_model_with_background(crowd, i + 1, 'lukketvenue.png')  # Sti til dit baggrundsbillede
