
import numpy as np
import matplotlib.pyplot as plt

delta_x = 1/60   # hour
start_x = 0      # hour
end_x = 48       # hour

x = np.arange(start_x, end_x, delta_x)

smidge = 1       # degF
heater_on = np.empty(len(x), dtype=bool)
furnace_power = 1    # degF/hr
thermostat = 70      # degF
outside_temp = 45    # degF
insulation_loss_factor = .00001    # (degF/hr)/degF

T = np.zeros(len(x))
T[0] = 45    # degF
heater_on[0] = False

for i in range(1,len(T)):
    
    if T[i-1] < thermostat - smidge  and  heater_on[i-1] == False:
        heater_on[i] = True
        heating = furnace_power    # degF/hr

    elif T[i-1] > thermostat + smidge  and  heater_on[i-1] == True:
        heater_on[i] = False
        heating = 0                # degF/hr

    else:
        heater_on[i] = heater_on[i-1]

    discrepancy = outside_temp - T[i-1]    # degF   (neg for cold outside)
    leakage = -(discrepancy * insulation_loss_factor)    # degF/hr  (pos for)

    T_prime = heating - leakage
    T[i] = T[i-1] + T_prime * delta_x
    
plt.plot(x, T, color="brown", label="room temp")
plt.plot(x, heater_on * 10, color="red", label="furnace")
plt.axhline(outside_temp, color="blue", label="outside temp")
plt.axhline(thermostat, color="black", linestyle="dotted", label="thermostat")
plt.axhline(thermostat + smidge, color="gray", linestyle="dotted")
plt.axhline(thermostat - smidge, color="gray", linestyle="dotted")
plt.xlabel('hours') 
plt.ylabel('deg F') 
plt.legend()
plt.show()


print(f"The furnace was on {heater_on.mean() * 100:.2f}% of the day.")
