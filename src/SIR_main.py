#Population Size
POPULATION = 2490

#Initial Infected Population
INITIAL_INFECTED = 1

#Prob of transmission
PROB = 0.5

#Num of interactions
NUM = 1.5

#Recovery time (days)
RECOVERY = 16

#Length of simulation (days)
DURATION = 100

#####################################################################
# Run simulation (dont change anything below here)                  #   
#####################################################################

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

I0 = INITIAL_INFECTED
R0 = 0
S0 = POPULATION - (I0 + R0)

beta, gamma = PROB*NUM, 1/RECOVERY
duration = np.linspace(start=0, stop=DURATION, num=DURATION)

intial_values = S0, I0, R0

#Get derivatives and integrate
def derivatives(y, t, POPULATION, beta, gamma):
    S, I, R = y
    dotS = -beta*S*(I/POPULATION)
    dotI = beta*S*(I/POPULATION) - gamma*I
    dotR = gamma*I
    return dotS, dotI, dotR

results = odeint(derivatives, intial_values, duration, args=(POPULATION, beta, gamma))
S, I, R = results.T

#Plot graph
plt.grid(b=True, which='major', c='k', lw=2, ls='-', alpha=0.2)
plt.xlabel('Time (days)')
plt.ylabel('Number of people')
plt.plot(duration, S, color='g', label='Susceptible')
plt.plot(duration, I, color='r', label='Infected')
plt.plot(duration, R, color='b', label='Removed')
plt.fill_between(duration, S, color='g', alpha=0.3)
plt.fill_between(duration, I, color='r', alpha=0.3)
plt.fill_between(duration, R, color='b', alpha=0.3)
plt.legend().get_frame().set_alpha(0.8)
plt.show()
