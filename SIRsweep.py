import numpy as np
import matplotlib.pyplot as plt

def runsim(mean_infectious_duration = 3,                 # days
    transmissibility = .20,                      # infections/contact
    contact_factor = 2.1,                        # (contacts/day)/person
    plot=False):

    recovery_factor = 1/mean_infectious_duration # 1/day

    # inf/person
    R0 = mean_infectious_duration * transmissibility * contact_factor

    start_x = 0                             # days
    end_x = 365                             # days (about one flu season)
    delta_x = 1/24                          # days (one sim tick per hour)
    x = np.arange(start_x, end_x, delta_x)  # days

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

    frac_ever_sick = (R[-1] + I[-1]) / (S[-1] + I[-1] + R[-1])

    if plot:
        plt.clf()
        plt.title(f"R0 = {R0}")
        plt.plot(x, S, color="blue", label="S")
        plt.plot(x, I, color="red", label="I")
        plt.plot(x, R, color="green", label="R")
        plt.xlabel("days")
        plt.ylabel("individuals")
        plt.legend()
        plt.show()

    return frac_ever_sick


contact_factors = np.arange(0,5,.05)

frac_ever_sicks = np.zeros(len(contact_factors))
for i in range(len(contact_factors)):
    frac_ever_sicks[i] = runsim(contact_factor=contact_factors[i])

plt.clf()
plt.plot(contact_factors, frac_ever_sicks, color="purple")
plt.xlabel("contact factor (contacts/day)/person")
plt.ylabel("fraction of people who got sick")
plt.show()
