
import numpy as np
import matplotlib.pyplot as plt
import math

def itox(i):
    return start_x + delta_x * i   # hours

dose = 1.5 * 325 * 1000    # ug
dose_interval = 3       # hours

delta_x = 5/60   # hours
start_x = 0      # hours
end_x = 48       # hours

x = np.arange(start_x, end_x, delta_x)

half_life = 3.2  # hours
plasma_volume = 3 * 1000   # ml
elimination_constant = math.log(2)/half_life   # 1/hr

D = np.zeros(len(x))     # ug
D[0] = dose * .20

for i in range(1, len(x)):
    elimination = D[i-1] * elimination_constant  # ug/hr
    D_prime = -elimination  # ug/hr
    D[i] = D[i-1] + delta_x * D_prime
    if math.isclose(itox(i) % dose_interval, 0):
        D[i] += dose
    

plasma_concentration = D / plasma_volume   # array  ug/ml

plt.plot(x, plasma_concentration, label="plasma conc", color="purple")
plt.axhline(150, color="green", label="MEC")
plt.axhline(300, color="red", label="MTC")
plt.legend()
plt.ylabel("ug/ml")
plt.xlabel("hours")
plt.ylim((0,max(330,plasma_concentration.max())))
plt.show()
