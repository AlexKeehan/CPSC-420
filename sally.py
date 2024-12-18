
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# "sally" because "sally sells sea schells"

import mesa
from mesa import Agent, Model, batch_run
from mesa.time import RandomActivation
from mesa.space import SingleGrid

class SallyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.color = np.random.choice(["red", "blue"])
    def happiness(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
        if len(neighbors) == 0:
            return 1
        num_blue = 0
        num_red = 0
        for neighbor in neighbors:
            if neighbor.color == "blue":
                num_blue += 1
            else:
                num_red += 1
        if self.color == "blue":
            happiness = num_blue / len(neighbors)
        else:
            happiness = num_red / len(neighbors)
        return happiness
    def step(self):
        if self.happiness() < self.model.threshold:
            #print(f"Agent {self.unique_id} unhappy!! :(")
            self.model.grid.move_to_empty(self)
            self.model.anybody_moved = True
            

class SallyModel(Model):
    def __init__(self, num_agents, dim, threshold):
        super().__init__()
        self.num_agents = num_agents
        self.running = True
        self.dim = dim
        self.threshold = threshold
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(dim, dim, torus=False)
        self.datacollector = mesa.DataCollector(
            model_reporters={ 'avg_seg': SallyModel.avg_seg },
        )
        for i in range(self.num_agents):
            a = SallyAgent(i, self)
            self.schedule.add(a)
            self.grid.move_to_empty(a)
    def avg_seg(self):
        happiness = 0
        for a in self.schedule.agents:
            happiness += a.happiness()
        return happiness / len(self.schedule.agents)
    def step(self):
        self.anybody_moved = False
        self.schedule.step()
        self.display_grid()
        if not self.anybody_moved:
            self.running = False
        self.datacollector.collect(self)
    def display_grid(self):
        cells = np.zeros((self.dim,self.dim))
        for a in self.schedule.agents:
            if a.color == "red":
                cells[a.pos[0], a.pos[1]] = 1
            else:
                cells[a.pos[0], a.pos[1]] = 2
        plt.cl()
        sns.heatmap(cells, cmap=['white','red','blue'], cbar=False,
            square=True)
        plt.pause(.1)
        plt.show()
        
sally = SallyModel(1500, 40, .9)
while sally.running:
    sally.step()
print(f"The segregation is {sally.avg_seg():.5f}")

#results = batch_run(SallyModel, parameters={ 'num_agents': 1000, 'dim': 40,
#    'threshold': np.arange(0,1.05,.05) },
#    number_processes=None, max_steps=20, iterations=10 )
#results = pd.DataFrame(results)
#means = results.groupby('threshold').avg_seg.mean()
#plt.clf()
#plt.plot(means.index, means.values)
#plt.ylim((.5,1))
#plt.savefig('ourplot.png')

