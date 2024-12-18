
import numpy as np
import matplotlib.pyplot as plt

def xtoi(x):
    return x / delta_x

delta_x = 1/7                    # weeks
x = np.arange(0,52*10,delta_x)   # weeks

# Simulation parameters (inputs).
earnings_rate_company1 = .47     # ($earned/$capital)/week
investment_frac_company1 = .32   # $reinvested/$earned
depreciation_rate1 = .1          # ($depreciated/$capital)/week
earnings_rate_company2 = .46     # ($earned/$capital)/week
investment_frac_company2 = .32   # $reinvested/$earned
depreciation_rate2 = .1          # ($depreciated/$capital)/week
economy_cc = 10000               # $/week (in earnings) saturation point


# Stocks. (Create a vector and an initial condition for each.)
C1 = np.empty(len(x))    # $
C1[0] = 450

E1 = np.empty(len(x))    # $/wk
E1[0] = 0

P1 = np.empty(len(x))    # $/wk
P1[0] = 0

C2 = np.empty(len(x))    # $
C2[0] = 450

E2 = np.empty(len(x))    # $/wk
E2[0] = 0

P2 = np.empty(len(x))    # $/wk
P2[0] = 0

for i in range(1,len(x)):

    if i > xtoi(200):
        earnings_rate_company2 = .48     # ($earned/$capital)/week

    logistic_factor = 1 - (E1[i-1]+E2[i-1]) / economy_cc    # unitless

    # Flows.
    E1[i] = C1[i-1] * earnings_rate_company1 * logistic_factor
    investment_company1 = E1[i] * investment_frac_company1
    P1[i] = E1[i] * (1 - investment_frac_company1)
    depreciation_company1 = C1[i-1] * depreciation_rate1
    E2[i] = C2[i-1] * earnings_rate_company2 * logistic_factor
    investment_company2 = E2[i] * investment_frac_company2
    P2[i] = E2[i] * (1 - investment_frac_company2)
    depreciation_company2 = C2[i-1] * depreciation_rate2

    # Primes.
    C1prime = investment_company1 - depreciation_company1
    C2prime = investment_company2 - depreciation_company2

    # Stocks.
    C1[i] = C1[i-1] + C1prime * delta_x
    C2[i] = C2[i-1] + C2prime * delta_x


# Plot and analyze.
plt.clf()
plt.plot(x/52, C1, color="blue", linestyle="solid", linewidth=3,
    label="Dominos capital")
plt.plot(x/52, P1, color="blue", linestyle="solid", linewidth=1,
    label="Dominos profits")
plt.plot(x/52, E1, color="blue", linestyle="dashed", linewidth=1,
    label="Dominos earnings")
plt.plot(x/52, C2, color="red", linestyle="solid", linewidth=3,
    label="Papa John's capital")
plt.plot(x/52, P2, color="red", linestyle="solid", linewidth=1,
    label="Papa John's profits")
plt.plot(x/52, E2, color="red", linestyle="dashed", linewidth=1,
    label="Papa John's earnings")
plt.suptitle("Competitive exclusion")
plt.title(f"Dominos earned \${P1.sum() * delta_x / 1e6:.2f} and PJ got \${P2.sum() * delta_x / 1e6:.2f} million.")
plt.xlabel("years")
plt.ylabel("dollars (or $/week)")
plt.legend()
plt.show()
