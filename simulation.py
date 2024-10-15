from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

# Define the agent class (each person in the crowd)
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = 1

    def step(self):
        # Define movement rules for each person
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

# Define the model (environment and crowd setup)
class CrowdModel(Model):
    def __init__(self, N, width, height):
        # Call the parent Model class' constructor
        super().__init__()  # This line initializes the base Model class

        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create N agents
        for i in range(self.num_agents):
            person = Person(i, self)
            self.schedule.add(person)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(person, (x, y))

    def step(self):
        # Advance the model by one step
        self.schedule.step()

#Create the model instance
crowd = CrowdModel(100, 10, 10)

#Run the simulation for 50 steps
for i in range(50):
    crowd.step()