import numpy as np
import random
import matplotlib.pyplot as plt

def calc_length(a, b):
    return np.sqrt(abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2)

def cities(n=30):
    p = []
    for i in range(n):
        p.append((np.random.randint(0, 1000), np.random.randint(0, 1000)))
    p.append(p[0])
    return p

def cities_chessboard(n=36):
    p = []
    for i in range(int(np.sqrt(n))):
        for j in range(int(np.sqrt(n))):
            p.append((i*100, j*100))
    p.append(p[0])
    return p

def cities_groups(n=30, g=3):
    p = []
    for i in range(g):
        x = np.random.randint(0, 2000)
        y = np.random.randint(0, 2000)
        for j in range(int(n/g)):
            p.append((np.random.randint(max(0,x-30), min(2000, x+30)), np.random.randint(max(0,y-30), min(2000, y+30))))
    p.append(p[0])
    return p



def population(cities, n=100):
    p = []
    order = list(range(1,len(cities)-1))
    for i in range(n):
        np.random.shuffle(order)
        o = []
        o.append(cities[0])
        for city in order:
            o.append(cities[city])
        o.append(cities[0])
        p.append(o)
    return(p)

def calc_points(route):
    points = 0
    for i in range(len(route)-1):
        points += calc_length(route[i], route[i+1])
    return points

def best_points(population):
    best = 10000000000000
    best_route = []
    for route in population:
        points = calc_points(route)
        if points < best:
            best = points
            best_route = route
    return best, best_route

def compare(route1, route2):
    if calc_points(route1) < calc_points(route2):
        return route1.copy()
    return route2.copy()

def selection(population):
    l = len(population)
    new = []
    for i in range(l):
        a = random.sample(range(l), 2)
        #print(a)
        new.append(compare(population[a[0]], population[a[1]]))
    return new

def mutate_route1(route):
    a = random.sample(range(1, len(route)-1), 2)
    #print(a)
    route[a[0]], route[a[1]] = route[a[1]], route[a[0]]
    return route

def mutate_route2(route):
    a = random.sample(range(1, len(route)-1), 2)
    a_1 = min(a)
    a_2 = max(a)
    b = random.choice(list(range(0, a_1)) + list(range(a_2+1, len(route)-2)))

    if b < a_1:
        new_route = route[:b+1] + route[a_1:a_2] + route[b+1:a_1] + route[a_2:]
    else:
        new_route = route[:a_1] + route[a_2:b] + route[a_1:a_2] + route[b:]
    return new_route

def mutate_route3(route):
    a = random.sample(range(1, len(route)-1), 2)
    a_1 = min(a)
    a_2 = max(a)
    new_route = route[:a_1] + route[a_2:a_1-1:-1] + route[a_2+1:]
    return new_route

def mutate_population(population, p, p1, p2, p3):
    for i, route in enumerate(population):
        if p >random.random():
            r = random.random()
            if r < p1:
                route = mutate_route1(route)
                continue
            if r < p1+p2:
                route = mutate_route2(route)
                continue
            if r < p1+p2+p3:
                route = mutate_route3(route)
                continue
        a = random.choice(range(1, len(route)))
        population[i] = route[a:] + route[1:a] + [route[a]]

    return population

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    if A == C or A == D or B == C or B == D:
        return False
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def del_intesection(route):
    for i in range(len(route)-3):
        for j in range(i+2, len(route)-1):
            if intersect(route[i], route[i+1], route[j], route[j+1]):
                new_route = route[:i+1] + route[j:i:-1] + route[j+1:]
                return new_route
    return route

def sort_population(population):
    return sorted(population, key=lambda x: calc_points(x))

def genetic(p_n, g_n, cities, min_l, pr, pr1, pr2, pr3):
    score = []
    p = population(cities, p_n)
    best = calc_points(p[0])
    best_route = p[0]
    l = 0
    b = 0
    while g_n > 0:
        if l >= min_l:
            #print("deleted")
            p[0] = del_intesection(p[0])
            l = 0
        p = selection(p)
        p = mutate_population(p, pr, pr1, pr2, pr3)
        p = sort_population(p)
        points = calc_points(p[0])
        best_route = p[0]
        if points < best:
            best = points
            l = 0
        else:
            l+=1
        g_n-=1
        #print(best)
        #print(b)
        b+=1
        score.append(best)
        x = []
        y = []
        for i in best_route:
            x.append(i[0])
            y.append(i[1])
        plt.plot(x, y, "ro--")
        plt.draw()
        plt.pause(0.01)
        plt.clf()
    plt.close()
    return p, score
