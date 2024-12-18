
import numpy as np
import matplotlib.pyplot as plt

bat_fertility = 1.2   # (bats/month)/bat
bat_death_rate = 2.0  # (bats/month)/bat
nutrition_factor = 3 # bats/kill
kill_ratio = .05 # kills/encounter
encounter_frequency = 3  # encounters/(month*bat*mouse)
mouse_fertility = 1.2 # (mice/month)/mouse
mouse_death_rate = 1.1 # (mice/month)/mouse

delta_x = 1/30   # months
start_x = 0      # months
end_x = 12*20        # months
x = np.arange(start_x, end_x, delta_x)

B = np.empty(len(x))
M = np.empty(len(x))
B[0] = 10
M[0] = 30

for i in range(1,len(x)):
    # flows
    bat_births = bat_fertility * B[i-1]    # bats/month
    mouse_births = mouse_fertility * M[i-1]    # mice/month

    encounter_rate = encounter_frequency * M[i-1] * B[i-1]  # enc/month
    kill_rate = kill_ratio * encounter_rate    # kills/month

    bat_deaths = bat_death_rate * B[i-1] - (nutrition_factor * kill_rate)
    mouse_deaths = mouse_death_rate * M[i-1] + kill_rate

    # primes
    Bprime = bat_births - bat_deaths
    Mprime = mouse_births - mouse_deaths

    # stocks
    B[i] = B[i-1] + Bprime * delta_x
    M[i] = M[i-1] + Mprime * delta_x


plt.plot(x,M,color="brown",linestyle="dotted",linewidth=2,label="mice")
plt.plot(x,B,color="black",linestyle="solid",linewidth=1,label="bats")
plt.legend()
plt.show()
