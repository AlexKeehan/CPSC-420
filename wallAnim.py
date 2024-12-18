import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import math
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
		self.inf_duration = 5
	def step(self):
		if self.state == "infected":
			if self.model.first_run:
				death = random.choices(['infected', 'dead'], weights=(100, 0))
			else:
				death = random.choices(['infected', 'dead'], weights=(95, 5))
			if death[0] == 'dead':
				self.state = 'dead'
			else:
				self.model.any_inf = True
				self.inf_duration = self.inf_duration - 1
				inf_spread = self.model.grid.get_neighborhood(self.pos, moore=False)
				infection_spread = ()
				for square in inf_spread:
					if square not in self.model.wall:
						infection_spread = infection_spread + ((square),)
				if len(infection_spread) > 0:
					for a in self.model.schedule.agents:
						if a.pos in infection_spread and a.state == "susceptible":
							a.state = "infected"
		elif self.state == "susceptible":
			vaccine = random.choices(['susceptible', 'vaccinated'], weights=(98,2))
			if vaccine[0] == 'vaccinated':
				self.state = 'vaccinated'
		if self.state == "infected" and self.inf_duration <= 0:
			self.state = "recovered"
		if self.state != 'dead':
			self.move()
		
	def move(self):
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False)
		steps = []
		#print("POSSIBLE STEPS", possible_steps)
		#print("WALL", self.model.wall)
		for step in possible_steps:
			#print(step)
			#print(self.model.wall[0])
			if step not in self.model.wall:
				steps.append(step)
		#print("STEPS", steps)
		place_to_go = self.random.choice(steps)
		if self.model.grid.is_cell_empty(place_to_go):
			self.model.grid.move_agent(self, place_to_go)


class SIRModel(Model):
	def __init__(self, num_agents, dim, gap):
		super().__init__()
		self.num_agents = num_agents
		self.dim = dim
		self.running = True
		self.gap = gap
		self.first_run = True
		self.middle = int(dim / 2)
		self.wall = self.build_wall()
		self.wall_grid = self.build_grid_with_wall()
		self.grid = SingleGrid(dim, dim, torus=False)
		self.schedule = RandomActivation(self)
		#self.datacollector = DataCollector(
			#model_reporters = { 'num_inf': SIRModel.num_inf, 'num_susc': SIRModel.num_susc, 'num_recov': SIRModel.num_recov}
		    #agent_reporters = { 'dun_broke': MarchAgent.am_broke }
		#)
		for i in range(num_agents):
			if i == 0:
				a = SIRAgent(i, self, "infected")
			else:
				a = SIRAgent(i, self, "susceptible")
			self.schedule.add(a)
			non_empty_grid = ()
			for i in self.wall_grid:
				if self.grid.is_cell_empty(i):
					non_empty_grid = non_empty_grid + ((i),)
			self.grid.move_agent_to_one_of(a, non_empty_grid, selection="random")
			
	def build_wall(self):
		wall = ()
		for i in range(self.dim):
			wall = wall + ((i, self.middle),)
		wall = self.build_gap_in_wall(wall)
		return wall
	
	def build_gap_in_wall(self, wall):
		new_wall = ()
		middle = (self.middle, self.middle)
		if self.gap == self.dim:
			return new_wall
		elif self.gap % 2 == 0:
			top = (self.middle + int(self.gap / 2), self.middle)
			bottom = (self.middle - int(self.gap / 2), self.middle)
		else:
			top = (self.middle + int(math.floor(self.gap / 2)), self.middle)
			bottom = (self.middle - int(math.ceil(self.gap / 2)), self.middle)
		for i in wall:
			if i[0] < top[0] and i[1] == top[1] and i[0] >= bottom[0] and i[1] == bottom[1]:
				pass
			else:
				new_wall = new_wall + ((i),)
		return new_wall
		
	
	def build_grid_with_wall(self):
		grid = ()
		for i in range(self.dim):
			for j in range(self.dim):
				grid = grid + ((i, j),)
		wall_grid = ()
		for i in grid:
			if i not in self.wall:
				wall_grid = wall_grid + ((i),)
		return wall_grid
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
		self.first_run = False
		self.display_grid()
		if not self.any_inf:
			self.running = False
		#self.datacollector.collect(self)

	def display_grid(self):
		cells = np.zeros((self.dim, self.dim))
		cmap = ['white', 'red', 'lightblue', 'green', 'black', 'purple', 'brown']
		legend_labels = ['Infected', 'Susceptible', 'Recovered', 'Dead', 'Vaccinated', 'Wall']
		colors = ['red', 'lightblue', 'green', 'black', 'purple', 'brown']
		for a in self.schedule.agents:
			if a.state == "infected":
				cells[a.pos[0], a.pos[1]] = 1
			elif a.state == "susceptible":
				cells[a.pos[0], a.pos[1]] = 2
			elif a.state == "recovered":
				cells[a.pos[0], a.pos[1]] = 3
			elif a.state == "dead":
				cells[a.pos[0], a.pos[1]] = 4
			elif a.state == "vaccinated":
				cells[a.pos[0], a.pos[1]] = 5
				
		for brick in self.wall:
			cells[brick[0], brick[1]] = 6
		plt.clf()
		plt.ion()
			
		cmap = ListedColormap(cmap)
		
		ax = sns.heatmap(cells, cmap=cmap, cbar=False, square=True, vmin=0, vmax=6)
		
		legend = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, legend_labels)]
		plt.legend(handles=legend, loc='upper left', bbox_to_anchor=(-.4,1.15))
		plt.pause(.1)
		plt.show()

SIR = SIRModel(40,10,2)
while SIR.running:
	SIR.step()

counter = 0
recovered = 0
dead = 0
vaccines = 0
for a in SIR.schedule.agents:
	if a.state == "infected" or a.state == "recovered" or a.state == "dead":
		counter += 1
	if a.state == "recovered":
		recovered += 1
	if a.state == "dead":
		dead += 1
	if a.state == "vaccinated":
		vaccines += 1

print(f"There was a total of {counter} people who got infected.")
print(f"{recovered} person(s) recovered from the disease")
print(f"{dead} people died.")
print(f"There were {vaccines} vaccines")
