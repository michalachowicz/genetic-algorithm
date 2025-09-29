from functions import genetic, calc_points
import json
import matplotlib.pyplot as plt
import time

with open("cities", "r") as file:
    a = json.load(file)

p, score = genetic(200, 1000, a, 50, 0.3, 0.5, 0.3, 0.2)
print(score[-1])
plt.clf()
plt.plot(range(len(score)),score)
plt.show()

