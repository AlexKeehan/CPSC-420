
import numpy as np
import matplotlib.pyplot as plt
import random as random

# We'll measure speed, distance, etc, once every (this increment).
delta_x = .01  # hrs

# Make a record of the speeds Stephen drove each hour.
#s = np.array([30,70,75,75,75,70,0,70,30])  # mph


s = np.array([]) #mph
#Tested up to 100000 size array and average was 49.5

#Get initial speed
initial = np.random.randint(0,100)
#Put it into speed array
s = np.append(s, initial)

#Loop through and add speeds to speed array
for i in range(1,9):
	#Get random number between -10 and 10 to add to initial num
	add = np.random.randint(-10,10)
	#Test for edge cases
	test = initial + add
	test_average = np.average(s)
	#If previous speed was below 50, then only add to it
	if test_average < 50:
		add = np.random.randint(0,10)
	#If previous speed was above 50, then only subtract from it
	elif test_average > 50:
		add = np.random.randint(-10,0)
	#Avoid speeds below 0
	elif test < 0:
		add = np.random.randint(0,10)
	#Avoid speeds above 100
	#elif test > 100:
	#	add = np.random.randint(-10,0)
	initial += add
	#Add to speed array
	s = np.append(s, initial)
#s = np.random.uniform(0,100,9)  # mph
#Average it out
average = np.average(s)
print("Average",average)


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

# Plot these suckers.
plt.plot(delta_x * np.arange(0,len(d)), d, color="blue",
    label="distance")
plt.plot(delta_x * np.arange(0,len(s)), s, color="green", label="speed")
plt.plot(delta_x * np.arange(0,len(computed_s)), computed_s,
    color="red", linewidth=5, linestyle="dashed", label="computed speed")
plt.xlabel("hours")
plt.ylabel("miles")
plt.legend()
plt.show()


