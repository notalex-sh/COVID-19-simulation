#Show statistics of what is occuring each day
show_daily_stats = False

#Number of simulations to run
total_simulations = 10

#Show population stats
show_pop_stats = False

#Number of people in town
total_population = 2490

#Number of initial infected people
initial_infected = 1

#Number of interactions (random between the two numbers)
min_interactions = 5
max_interactions = 10

#Probability of transmitting disease in interaction between infected and susceptible (random between the two numbers/10)
min_trans_prob = 0.1
max_trans_prob = 1

#Recovery time (days, random between the two numbers)
min_recov_time = 11
max_recov_time = 24

#Duration of experiment (days)
duration = 100

#####################################################################
# Run simulation (dont change anything below here)                  #   
#####################################################################

import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

#Create every person

class Person:
  def __init__(self, status, interactions, trans_prob, recov_time):
    self.status = status
    self.interactions = interactions
    self.trans_prob = trans_prob
    self.recov_time = recov_time

def create_person():
  status = "susceptible"
  interactions = random.randint(min_interactions, max_interactions)
  trans_prob = round(random.uniform(min_trans_prob, max_trans_prob), 2)/10
  recov_time = random.randint(min_recov_time, max_recov_time)
  return status, interactions, trans_prob, recov_time

def simulation():
  population = []
  people = 1
  while people <= total_population:
    population.append(Person(*create_person()))
    people += 1

  #Show stats if requested
  if show_pop_stats:
    subject = 1
    for person in population:
      print("Subject " + str(subject) + " | Status: " + person.status + " | Interactions: " + str(person.interactions) + " | Transmission Probability: " + str(person.trans_prob) + " | Recovery Time: " + str(person.recov_time))
      subject += 1

  for person in population[:(initial_infected)]:
    person.status = "infected"
    setattr(person, 'infected_date', 0)

  sus_count = total_population - initial_infected
  inf_count = initial_infected
  rem_count = 0
  sus_list = []
  inf_list = []
  rem_list = []
  day = 1

  while day <= duration:

    #Show stats if requested
    if show_daily_stats:
      print("\nDay: " + str(day) + "--------\n")
      for person in population: print(vars(person))
      print("\nSusceptible: " + str(sus_count) + "\nInfected: " + str(inf_count) + "\nRemoved: " + str(rem_count))

    sus_list.append(sus_count)
    inf_list.append(inf_count)
    rem_list.append(rem_count)

    for person in population:
      if person.status == "removed":
        population.remove(person)
        rem_count += 1
        inf_count -= 1
      if person.status == "infected":
        if (person.recov_time + person.infected_date - 1) <= day:
          person.status = "removed"
        elif person.infected_date != day:
          interactions = 1
          while interactions <= person.interactions:
            if interactions <= sus_count:  
              random_person = random.randint(0, len(population) - 1)
              if population[random_person].status == "susceptible":
                if random.random() <= person.trans_prob:
                  population[random_person].status = "infected"
                  setattr(population[random_person], 'infected_date', day)
                  sus_count -= 1
                  inf_count += 1 
            else:
              break
            interactions += 1 
    day += 1
  return sus_list, inf_list, rem_list

#Run simulations n times

totals_lists = [[], [], []]
current_simulation = 1
while current_simulation <= total_simulations:
  os.system("clear")
  print("Running simulation: " + str(current_simulation))
  print('[' + '='*current_simulation + ' '*(total_simulations - current_simulation) + ']')
  current_simulation_results = simulation()
  totals_lists = [list + [current_simulation_results[index]] for (index, list) in enumerate(totals_lists)]
  print(totals_lists)
  current_simulation += 1

#Create means and equations

def graph_list(input_list):
  output_array = [np.array(person) for person in input_list]
  return [np.mean(person) for person in zip(*output_array)]

totals_lists = [graph_list(list) for list in totals_lists]

max_value = totals_lists[1].index(max(totals_lists[1]))

x_list = np.linspace(0, duration, duration)
y_list = np.array(totals_lists[1])

def exponential(x, a, b):
  return a*np.exp(-b*(x - max_value)**2)

vars, cov = curve_fit(f=exponential, xdata=x_list, ydata=y_list, p0=[0, 0], bounds=(-np.inf, np.inf))

def round_values(i):
  return round(i, 5)

vars = list(map(round_values, vars.tolist()))

equation = str(vars[0]) + 'e^-(' + str(vars[1]) + '(x - ' + str(max_value) + ')^2)'

#Display output

os.system("clear")
print("DONE")
print("----")
print('\nEquation: ' + equation)
print("\nValues up to max point:\n")
print(totals_lists[1][:max_value])

plt.grid(b=True, which='major', c='k', lw=2, ls='-', alpha=0.2)
plt.xlabel('Time (days)')
plt.ylabel('Number of people')
plt.plot(x_list, totals_lists[0], color='g', label='Susceptible')
plt.plot(x_list, totals_lists[1], color='r', label='Infected')
plt.plot(x_list, totals_lists[2], color='b', label='Removed')
plt.fill_between(x_list, totals_lists[0], color='g', alpha=0.3)
plt.fill_between(x_list, totals_lists[1], color='r', alpha=0.3)
plt.fill_between(x_list, totals_lists[2], color='b', alpha=0.3)
plt.legend().get_frame().set_alpha(0.8)
plt.show()
