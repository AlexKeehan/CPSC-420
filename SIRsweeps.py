import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from mesa import batch_run
from matplotlib.colors import ListedColormap

class SIRAgent(Agent):
	def __init__(self, unique_id, model, state, inf_duration):
		super().__init__(unique_id, model)
		self.state = state
		self.inf_duration = inf_duration
	def step(self):
		if self.state == "infected":
			self.model.any_inf = True
			self.inf_duration = self.inf_duration - 1
			infection_spread = self.model.grid.get_neighborhood(self.pos, moore=False)
			if len(infection_spread) > 0:
				for a in self.model.schedule.agents:
					if a.pos in infection_spread and a.state == "susceptible":
						a.state = "infected"
		if self.state == "infected" and self.inf_duration <= 0:
			self.state = "recovered"
		self.move()
		
	def move(self):
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False)
		place_to_go = self.random.choice(possible_steps)
		if self.model.grid.is_cell_empty(place_to_go):
			self.model.grid.move_agent(self, place_to_go)


class SIRModel(Model):
	def __init__(self, num_agents=20, dim=10, inf_duration=5):
		super().__init__()
		self.num_agents = num_agents
		self.dim = dim
		self.inf_duration = inf_duration
		self.running = True
		self.grid = SingleGrid(dim, dim, torus=True)
		self.schedule = RandomActivation(self)
		self.datacollector = DataCollector(model_reporters = { 'total_inf': SIRModel.total_inf})
		for i in range(num_agents):
			if i == 0:
				a = SIRAgent(i, self, "infected", self.inf_duration)
			else:
				a = SIRAgent(i, self, "susceptible", self.inf_duration)
			self.schedule.add(a)
			self.grid.move_to_empty(a)
	def total_inf(self):
		total_inf = 0
		for a in self.schedule.agents:
			if a.state == "infected" or a.state == "recovered":
				total_inf += 1
		return total_inf
	def num_inf(self):
		num_inf = 0
		for a in self.schedule.agents:
			if a.state == "infected":
				num_inf += 1
		return num_inf
	def num_susc(self):
		num_susc = 0
		for a in self.schedule.agents:
			if a.state == "susceptible":
				num_susc += 1
		return num_susc
	def num_recov(self):
		num_recov = 0
		for a in self.schedule.agents:
			if a.state == "recovered":
				num_recov += 1
		return num_recov
	def step(self):
		self.any_inf = False
		self.schedule.step()
		
		# No animation for this
		#self.display_grid()
		
		if not self.any_inf:
			self.running = False
		self.datacollector.collect(self)
		
	def display_grid(self):
		recov = False
		cells = np.zeros((self.dim, self.dim))
		for a in self.schedule.agents:
			if a.state == "infected":
				cells[a.pos[0], a.pos[1]] = 1
			if a.state == "susceptible":
				cells[a.pos[0], a.pos[1]] = 2
			if a.state == "recovered":
				recov = True
				cells[a.pos[0], a.pos[1]] = 3
		plt.clf()
		plt.ion()
		if not recov:
			cmap = ['white','red','blue']
		else:
			cmap = ['white','red','blue', 'green']
		sns.heatmap(cells, cmap=cmap, cbar=False, square=True)
		plt.legend(labels= ['Susceptible', 'Infected', 'Recovered'], loc="upper left")
		plt.pause(.1)
		plt.show()

num_agents = 20
sweep = batch_run(SIRModel,
parameters={ 'num_agents':num_agents,'dim':10,'inf_duration':range(0,21, 1)},
number_processes=None, max_steps=100, iterations=100)
results = pd.DataFrame(sweep)
plt.clf()
means = results.groupby('inf_duration').total_inf.mean()
plt.plot(means.index, means.values)
plt.ylabel("Total Infected")
plt.xlabel("Infectious Duration")
plt.xlim(0,20)
plt.ylim(0,num_agents + 2)
plt.title("Part 2 Sweep Results")
plt.show()
