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
import matplotlib.patches as mpatches

class SIRAgent(Agent):
	def __init__(self, unique_id, model, state):
		super().__init__(unique_id, model)
		self.state = state
		self.inf_duration = 10
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
	def __init__(self, num_agents, dim):
		super().__init__()
		self.num_agents = num_agents
		self.dim = dim
		self.running = True
		self.grid = SingleGrid(dim, dim, torus=True)
		self.schedule = RandomActivation(self)
        #Uncomment for SIRbasics.png
		#self.datacollector = DataCollector(
		#    model_reporters = { 'num_inf': SIRModel.num_inf, 'num_susc': SIRModel.num_susc, 'num_recov': SIRModel.num_recov})

		for i in range(num_agents):
			if i == 0:
				a = SIRAgent(i, self, "infected")
			else:
				a = SIRAgent(i, self, "susceptible")
			self.schedule.add(a)
			self.grid.move_to_empty(a)
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
        #Comment this out for the SIRbasics.png
		self.display_grid()
		
		if not self.any_inf:
			self.running = False
        #Uncomment this for the SIRbasics.png
		#self.datacollector.collect(self)

	def display_grid(self):
		colors = ['red', 'lightblue', 'green']
		cmap = ['white','red','lightblue', 'green']
		cells = np.zeros((self.dim, self.dim))
		for a in self.schedule.agents:
			if a.state == "infected":
				cells[a.pos[0], a.pos[1]] = 1
			if a.state == "susceptible":
				cells[a.pos[0], a.pos[1]] = 2
			if a.state == "recovered":
				cells[a.pos[0], a.pos[1]] = 3
		plt.clf()
		plt.ion()
		
		cmap = ListedColormap(cmap)
		
		ax = sns.heatmap(cells, cmap=cmap, cbar=False, square=True, vmin=0, vmax=3)
		legend = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, ['Infected', 'Susceptible', 'Recovered'])]
		plt.legend(handles=legend, loc='upper left', bbox_to_anchor=(-.4,1.15))
		plt.pause(.1)
		plt.show()

SIR = SIRModel(40,10)
while SIR.running:
	SIR.step()
counter = 0
for a in SIR.schedule.agents:
	if a.state == "infected" or a.state == "recovered":
		counter += 1

print(f"There are a total of {counter} person(s) infected.")

#Code to produce the SIRbasics.png plot
'''
time = 100
SIR = SIRModel(225,30)
for i in range(time):
        SIR.step()
plt.clf()
inf = SIR.datacollector.get_model_vars_dataframe().num_inf
sus = SIR.datacollector.get_model_vars_dataframe().num_susc
recov = SIR.datacollector.get_model_vars_dataframe().num_recov
print(inf)
delta_x = 1   # hours
start_x = 0      # hours
end_x = time       # hours

x = np.arange(start_x, end_x, delta_x)

plt.plot(x, inf, label="Number Infected", color="red")
plt.plot(x, sus, label="Number Susceptible", color="blue")
plt.plot(x, recov, label="Number Recovered", color="green")
plt.legend()
plt.title("SIRbasics Plot")
plt.show()
'''
