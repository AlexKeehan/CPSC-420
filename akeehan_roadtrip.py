
import numpy as np
import matplotlib.pyplot as plt

# We'll measure speed, distance, etc, once every (this increment).

#Change delta_x to adjust for speed samples being taken every minute
delta_x = .017  # hrs

# Make a record of the speeds Stephen drove each hour.
#s = np.array([30,70,75,75,75,70,0,70,30])  # mph

# Just for gigs, roll 9 hours of random driving speeds.
s = np.random.uniform(0,100,540)  # mph



# We're going to integrate the speed to get the total cumulative distance
# traveled at each time point.
d = np.zeros(len(s)+1)  # miles

d[0] = 0 # start measuring from Denver (could be from anywhere though)

# Calc 2: integrate
for i in range(1,len(d)):
    d[i] = d[i-1] + s[i-1] * delta_x

# Now let's reverse engineer the distances back into the speeds.
# Calc 1: differentiate
computed_s = np.zeros(len(s))  # mph
for i in range(0,len(computed_s)):
    computed_s[i] = (d[i+1] - d[i]) / delta_x  
    
#Differentiate the speed
accel = np.zeros(len(s)) #mph^2
for i in range(0,len(accel) - 1):
	accel[i] = (s[i+1] - s[i]) / delta_x

# Plot these suckers.
plt.plot(delta_x * np.arange(0,len(d)), d, color="blue",
    label="distance")
plt.plot(delta_x * np.arange(0,len(s)), s, color="green", label="speed")
plt.plot(delta_x * np.arange(0,len(computed_s)), computed_s,
    color="red", linestyle="dashed", label="computed speed")
plt.plot(delta_x * np.arange(0,len(accel)), accel,
    color="orange", linewidth=2, linestyle="dashed", label="acceleration")
plt.xlabel("hours")
plt.ylabel("miles")
plt.title("Item #3")
plt.legend()
plt.show()
