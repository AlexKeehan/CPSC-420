import numpy as np
import matplotlib.pyplot as plt

mean_infectious_duration = 5                 # days
transmissibility = .1                       # infections/contact
contact_factor = 4                         # (contacts/day)/person
recovery_factor = 1/mean_infectious_duration # 1/day

start_x = 0                                  # days
end_x = 365 / 4                              # days (about one flu season)
delta_x = 1/24                               # days (one sim tick per hour)
x = np.arange(start_x, end_x, delta_x)       # days

S = np.empty(len(x))     # individuals
I = np.empty(len(x))     # individuals
R = np.empty(len(x))     # individuals
S[0] = 20000             # individuals in Fredericksburg
I[0] = 1                 # individuals (start with one sick dude)
R[0] = 0                 # individuals

for i in range(1,len(x)):

    # Flows.
    frac_susc = S[i-1]/(S[i-1] + I[i-1] + R[i-1])    # unitless
    SI_contact_rate = frac_susc * contact_factor * I[i-1] # contacts/day
    infection = SI_contact_rate * transmissibility   # infections/day
    recovery = I[i-1] * recovery_factor              # recoveries/day

    # Primes.
    S_prime = -infection
    I_prime = infection - recovery
    R_prime = recovery

    # Stocks.
    S[i] = S[i-1] + S_prime * delta_x
    I[i] = I[i-1] + I_prime * delta_x
    R[i] = R[i-1] + R_prime * delta_x

plt.plot(x, S, color="blue", label="S")
plt.plot(x, I, color="red", label="I")
plt.plot(x, R, color="green", label="R")
plt.xlabel("days")
plt.ylabel("individuals")
plt.legend()
plt.show()
