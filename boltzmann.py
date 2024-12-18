
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa import batch_run

class MarchAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cash = self.model.starting_cash
    def step(self):
        self.move()
        if self.cash == 0:
            pass
        else:
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
            if len(neighbors) > 0:
                other = self.random.choice(neighbors)
                other.cash += 1
                self.cash -= 1
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,
            moore=True)
        place_to_go = self.random.choice(possible_steps)
        if self.model.grid.is_cell_empty(place_to_go):
            self.model.grid.move_agent(self, place_to_go)
    def am_broke(self):
        return not self.cash


class MarchModel(Model):
    def __init__(self, num_agents, dim, starting_cash):
        super().__init__()
        self.num_agents = num_agents
        self.starting_cash = starting_cash
        self.dim = dim
        self.running = True
        self.grid = SingleGrid(dim, dim, torus=True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters = { 'max_wealth': MarchModel.max_wealth,
                'gini': MarchModel.compute_gini },
            #agent_reporters = { 'dun_broke': MarchAgent.am_broke }
        )
        for i in range(num_agents):
            a = MarchAgent(i, self)
            self.schedule.add(a)
            self.grid.move_to_empty(a)
    def max_wealth(self):
        cashes = [ a.cash for a in self.schedule.agents ]
        return max(cashes)
    def step(self):
        self.schedule.step()
        #self.display_grid()
        self.datacollector.collect(self)
    def display_grid(self):
        cells = np.zeros((self.dim, self.dim))
        for a in self.schedule.agents:
            cells[a.pos[0], a.pos[1]] = a.cash + 1
        plt.clf()
        sns.heatmap(cells, square=True, cmap="gray", vmin=0, vmax=8)
        plt.pause(.04)
        plt.show()
    def compute_gini(self):
        agent_wealths = [agent.cash for agent in self.schedule.agents]
        x = sorted(agent_wealths)
        N = self.num_agents
        B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
        return 1 + (1 / N) - 2 * B

aprilmodel = MarchModel(100,25,10)

        
x = batch_run(MarchModel,
    parameters={ 'num_agents':40,'dim':15,'starting_cash':range(10,100,10)},
    number_processes=False, max_steps=500, iterations=100)
x = pd.DataFrame(x)

#aprilmodel = MarchModel(100,25)
#for i in range(80):
#    aprilmodel.step()
#
#cashes = [ a.cash for a in aprilmodel.schedule.agents ]
#print(cashes)
#
#plt.clf()
#plt.plot(aprilmodel.datacollector.get_model_vars_dataframe().max_wealth)
#plt.savefig('max_wealth.png')
#plt.clf()
#plt.plot(aprilmodel.datacollector.get_model_vars_dataframe().gini)
#plt.savefig('gini.png')
#plt.clf()
#plt.plot(aprilmodel.datacollector.get_agent_vars_dataframe().groupby('Step').dun_broke.sum() )
#plt.savefig('dun_broke.png')
