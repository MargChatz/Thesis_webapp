import math

def graph_values(median, std,iterations):
    """
    """
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

