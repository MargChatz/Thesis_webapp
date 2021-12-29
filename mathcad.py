import math
from scipy.stats import lognorm

def graph_values(median, std,iterations):
    ys = []
    xs = []    
    for i in range(1,10):
        i = i/10
        xs.append(i)
        ys.append(1/(std*i*math.sqrt(math.pi*2)) * math.exp(  (-1)*((math.log(i) - math.log(median))**2)/(2*std**2)))
        
    for i in range(1,iterations+1):
        xs.append(i)
        ys.append(1/(std*i*math.sqrt(math.pi*2)) * math.exp(  (-1)*((math.log(i) - math.log(median))**2)/(2*std**2)))

    return (xs, ys)

# def f(std,median,i):
#     return 1/(std*i*math.sqrt(math.pi*2)) * math.exp(  (-1)*((math.log(i) - math.log(median))**2)/(2*std**2))

# std = 0.734901
# median = 40.33986



# mathcad_numbers = []
# with open("C:/Users/30697/Desktop/Thesis/flask/lightning_app/templates/mathcad_data.txt" , 'r') as file:
#     lines = file.readlines()
#     mathcad_numbers = [float(line) for line in lines]

# print(type(mathcad_numbers))
# python_numbers = []
# for i in range (1,201):
#     python_numbers.append(round(f(std,median,i),10))
# print(type(python_numbers))
# print(python_numbers[0],mathcad_numbers[0])
# diffs = []
# for i in range(200):
#     diffs.append(python_numbers[i]-mathcad_numbers[i])

# print(sum(diffs))
