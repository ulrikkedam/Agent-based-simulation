from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

#agent-baseret simulation af mennesker i en overfyldt situation, hvor man kan simulere bevægelsen af personer i et gitter (10x10 grid)

#Repræsenterer hver agent i mængden, som flytter sig tilfældigt til en nabocelle for hvert trin.
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = 1  #Hver agent har en hastighedsattribut (selvom den ikke er brugt her)

    def step(self):
        #Definerer bevægelsesregler for hver person
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        #Udskriver agentens nye position
        print(f"Agent {self.unique_id} flyttede til {new_position}")

#Styrer simulationen, opretter et gitter og placerer agenterne i det. Den sørger også for at køre simulationen trin for trin
class CrowdModel(Model):
    def __init__(self, N, width, height):
        super().__init__()  #Kalder den overordnede Model-klasse's konstruktør

        self.num_agents = N  #Antallet af agenter
        self.grid = MultiGrid(width, height, True)  #Opretter et grid med de givne dimensioner (wrap-around = True)
        self.schedule = RandomActivation(self)  #Random scheduler, der vælger agenternes rækkefølge tilfældigt

        #Opret n agenter
        for i in range(self.num_agents):
            person = Person(i, self)  #Opretter en ny agent med unik ID
            self.schedule.add(person)  #Tilføjer agenten til scheduler'en

            #Tilføjer agenten til en tilfældig position på grid'et
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(person, (x, y))

    def step(self):
        #Avancerer modellen ét trin
        self.schedule.step()

#Opretter en instans af CrowdModel med 100 agenter og et 10x10 grid
crowd = CrowdModel(5, 10, 10)

#Kører simulationen i 20 trin
for i in range(20):
    print(f"Trin {i+1}")  #Udskriver trin nummeret
    crowd.step()  #Kører ét trin af simulationen