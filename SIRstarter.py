import numpy as np
import matplotlib.pyplot as plt

mean_infectious_duration = 2                 # days
transmissibility = .25                       # infections/contact
contact_factor = 5.1                         # (contacts/day)/person
recovery_factor = 1/mean_infectious_duration # 1/day

start_x = 0                                  # days
end_x = 365 / 4                              # days (about one flu season)
delta_x = 1/24                               # days (one sim tick per hour)
x = np.arange(start_x, end_x, delta_x)       # days





#plt.plot(x, S, color="blue", label="S")
#plt.plot(x, I, color="red", label="I")
#plt.plot(x, R, color="green", label="R")
#plt.xlabel("days")
#plt.ylabel("individuals")
#plt.legend()
#plt.show()
