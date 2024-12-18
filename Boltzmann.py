import mesa
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy

class MoneyAgent(mesa.Agent):
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
		self.cash = 1
		
	def step(self):
		if self.cash > 0:
			other = self.random.choice(self.model.schedule.agents)
			if other is not None and other.unique_id != self.unique_id:
				other.cash += 1
				self.cash -= 1
		#print(f"Hi, I am agent {str(self.unique_id)}")
		
class MoneyModel(mesa.Model):
	def __init__(self, N):
		super().__init__()
		self.num_agents = N
		self.schedule = mesa.time.RandomActivation(self)
		
		for i in range(self.num_agents):
			a = MoneyAgent(i, self)
			self.schedule.add(a)
			
	def step(self):
		self.schedule.step()
		
numagents = 50
model = MoneyModel(numagents)

for i in range(150):
	model.step()
	

agent_cash = [a.cash for a in model.schedule.agents]

histogram = sns.histplot(agent_cash, discrete=True)
histogram.set(title="Cash Distribution", xlabel="Cash", ylabel="Num Agents");
plt.plot()
plt.show()
plt.clear()
