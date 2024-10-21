import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Opret en grid-repræsentation af crowd density i koncertsalen
class CrowdFlowModel:
    def __init__(self, width, height, num_people):
        self.grid = np.zeros((width, height))  # Gitter, der repræsenterer tætheden af mennesker
        self.num_people = num_people

        #Placér folk tilfældigt i grid'et
        for _ in range(num_people):
            x = np.random.randint(1, width)  #Undgå at placere på scenen (række 0)
            y = np.random.randint(0, height)
            self.grid[x, y] += 1  #Tilføj en person til en tilfældig celle

        #Markér scenen som uoverkommelig
        self.grid[0, :] = 0  #Scene-række (øverste række)

    #Simuler crowd flow ved at flytte folk mod udgangene
    def step(self):
        new_grid = np.zeros_like(self.grid)

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x, y] > 0:  # Hvis der er mennesker i cellen
                    # Hvis agenten er på scenen (række 0), skal de ikke bevæge sig
                    if x == 0:
                        new_grid[x, y] += self.grid[x, y]
                    else:
                        # Tæl hvor tæt agenten er på scenen og udgangene
                        distance_to_stage = x
                        distance_to_exit_left = (self.grid.shape[0] - 1) - x + y
                        distance_to_exit_right = (self.grid.shape[0] - 1) - x + (self.grid.shape[1] - 1 - y)

                        # Beregn sandsynlighed for at bevæge sig mod scenen vs. udgange
                        move_to_stage_prob = 1 / (distance_to_stage + 1)
                        move_to_exit_prob = (1 / (distance_to_exit_left + 1) + 1 / (distance_to_exit_right + 1))

                        total_prob = move_to_stage_prob + move_to_exit_prob

                        # Normaliser sandsynlighederne
                        move_to_stage_prob /= total_prob
                        move_to_exit_prob /= total_prob

                        # Vælg en retning baseret på sandsynlighederne
                        if np.random.rand() < move_to_stage_prob:
                            # Forsøg at bevæge sig mod scenen (én celle op)
                            if x > 1:
                                new_grid[x - 1, y] += self.grid[x, y]  # Flyt mod scenen
                        else:
                            # Forsøg at bevæge sig mod en udgang (én celle ned)
                            if x < self.grid.shape[0] - 1:
                                new_grid[x + 1, y] += self.grid[x, y]  # Flyt mod udgangen

        # Opdater grid'et
        self.grid = new_grid

# Funktion til at visualisere grid'et med et koncertsalbillede som baggrund
def visualize_flow_with_background(model, step_number, background_img_path):
    # Load koncertsalbilledet som baggrund
    img = mpimg.imread(background_img_path)

    # Skab et subplot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Vis baggrundsbilledet af koncertsalen
    ax.imshow(img, extent=[0, model.grid.shape[1], model.grid.shape[0], 0])

    # Tegn agenterne som cirkler
    for x in range(model.grid.shape[0]):
        for y in range(model.grid.shape[1]):
            density = model.grid[x, y]  # Tætheden i den nuværende celle
            if density > 0:
                size = density * 0.5  # Juster størrelsen på cirklen (fx: 0.5 gange tætheden)
                circle = plt.Circle((y, x), size, color='blue', alpha=0.5)
                ax.add_patch(circle)  # Tilføj cirklen til plot

    # Titlen til visualiseringen
    plt.title(f"Crowd Flow - Step {step_number}")
    plt.xlim(0, model.grid.shape[1])  # Indstil aksegrænser
    plt.ylim(model.grid.shape[0], 0)  # Omvendt y-akse
    plt.grid(False)  # Fjern grid-linjer for at vise billedet tydeligere
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()

# Opretter en instans af flow-modellen med 50 personer i et 10x10 grid
crowd_model = CrowdFlowModel(10, 10, 100)

# Kør simulationen i 10 trin og visualiser crowd flow ovenpå en koncertsal baggrund
for i in range(20):
    crowd_model.step()  # Kør ét trin af flow-modellen
    visualize_flow_with_background(crowd_model, i + 1, 'lukketvenue.png')  # Path til koncertsal billede
