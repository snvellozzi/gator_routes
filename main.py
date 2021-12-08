import pandas as pd
import numpy as np

# Implementation of the Bellman-Ford algorithm
def BellmanFord(src, end, matrix):
    # number of vertices in one dimension of the matrix
    numVertices = matrix.shape[1]

    # array of distances from src vertex to all other vertices
    dV = [float("inf") for _ in range(len(matrix))]

    # array keeps track of previous vertex connected to each vertex that makes the shortest distance from src
    prev = [None] * 385

    dV[src] = 0

    # Loop through vertices in graph
    for i in range(0, numVertices - 1):
        for j in range(0, numVertices):
            for k in range(0, numVertices):
                if (matrix[j][k] != 0):
                    # if the path from the source vertex to this vertex is shorter than the one stored in the array, save path
                    if (dV[j] + matrix[j][k] < dV[k]):
                        dV[k] = dV[j] + matrix[j][k]

                        prev[k] = j
    for j in range(0, numVertices):
        for k in range(0, numVertices):
            if (matrix[j][k] != 0):
                # checks for neg weight cycles
                if (dV[j] + matrix[j][k] < dV[k]):
                    print("Graph has negative weight cycle.")

    # array will contain all of the cities in the shortest path in order
    inorder = [end]

    index = end

    # iterates through prev to get all the cities in the path from src to end in order
    while index != src and prev[end]!=None:
        inorder.append(index)
        index = prev[index]
    inorder.append(src)

    # returns an array with all of the cities in the path in order
    return inorder[::-1]

# Implementation of Dijkstra's Algorithm
def dijkstra(matrix, src, end, cities_list):
    # array of distances from src vertex to all other vertices (fill w infinity)
    dV = [float("inf") for _ in range(len(matrix))]

    # array of booleans to keep track of if a vertex was visited
    visited = [False for _ in range(len(matrix))]

    dV[src] = 0

    # array keeps track of previous vertex connected to each vertex that makes the shortest distance from src
    prev = [None] * 385

    # array will contain all of the cities in the shortest path in order
    inorder = []

    sum = 0

    # while there are still vertices that have not been visited yet
    while True:

        # find the vertex with the shortest distance from the src vertex
        smallest_distance = float("inf")
        smallest_index = -1
        for i in range(len(matrix)):
            # goes through all vertexes that have not been visited
            if dV[i] < smallest_distance and not visited[i]:
                smallest_distance = dV[i]
                smallest_index = i

        # if all vertices have been visited
        if smallest_index == -1:
            index = end
            while index != src and prev[index] != None:
                inorder.append(index)
                index = prev[index]
            inorder.append(src)

            if prev[end] == None:
                print("There is no connection between the cities.")
                exit()
            else:
                # Print the path with city names
                print("Dijkstra's Shortest Path: ", end=" ")
                for num in reversed(range(len(inorder))):
                    print(cities_list[inorder[num]], end=" ")
                    if num != 0:
                        print(" --> " + str(matrix[inorder[num]][inorder[num - 1]]) + " --> ", end=" ")
            print()

            # returns the array with the shortest path from the src vertex to all other vertices
            return dV

        # iterates through adjacent vertices that have not been visited
        for i in range(len(matrix[smallest_index])):
            # if the path from the source vertex to this vertex is shorter than the one stored in the array, save path
            if matrix[smallest_index][i] != 0 and dV[smallest_index] + matrix[smallest_index][i] < dV[i]:
                dV[i] = dV[smallest_index] + matrix[smallest_index][i]
                prev[i] = smallest_index
        # mark the vertex as visited
        visited[smallest_index] = True

################# THE START OF RUNNING OUR PROGRAM ##########################
# Read in csv file with data
dataset = pd.read_csv("dataset.csv")

# Create adjacency matrix -- unique cities
rows, cols = (385, 385)

# Create 2D list and fill with 0's
matrix = [[0 for i in range(cols)] for j in range(rows)]

# Create list to access index of each city
fromCities = list(dataset.From.values)
toCities = list(dataset.To.values)
fromCities_arr = np.array(fromCities)
fromCities_arr = np.unique(fromCities_arr)

# Unique list of cities
fromCities_list = fromCities_arr.tolist()

# Append any cities in the To col that are not present in the From col (restricted dataset)
for i in toCities:
    if i not in fromCities_list:
        fromCities_list.append(i)

# Populate matrix w data from csv file: Time is based on index of cities in alphabetical order in fromCities_list
for j in range(200):
    matrix[fromCities_list.index(dataset['From'][j])][fromCities_list.index(dataset['To'][j])] = dataset['Time (min)'][j]

# Get user input:
sourceVertex = input("Enter the starting city: ")
endVertex = input("Enter the ending city: ")
# Finds corresponding index of city user entered
startCityIndex = fromCities_list.index(sourceVertex)
endCityIndex = fromCities_list.index(endVertex)

# Call dijkstra's on matrix
results = dijkstra(matrix, startCityIndex, endCityIndex, fromCities_list)

# Prints results from dijkstra's
if results[endCityIndex] != float("inf"):
    print("Dijkstra's: Shortest time between two cities is " + str(results[endCityIndex]) + " min")

print()

# Call Bellman-Ford on matrix
matrix_bellman = np.array(matrix)
src = startCityIndex
end = endCityIndex
results_bellman = BellmanFord(src, end, matrix_bellman)

# Get sum of distances from BF
sum = 0
for i in range(len(results_bellman) - 1):
    sum = sum + matrix_bellman[results_bellman[i]][results_bellman[i + 1]]

# Print entire path with city names
print("Bellman-Ford Shortest Path: ", end=" ")
for i in range(len(results_bellman) - 1):
    #print(fromCities_list[results_bellman[i]] + " --> " + str(matrix_bellman[results_bellman[i]][results_bellman[i + 1]]) + " --> ", end=" ")
    print(fromCities_list[results_bellman[i]], end=" ")
    if i != len(results_bellman) - 2:
        print(" --> " + str(matrix_bellman[results_bellman[i]][results_bellman[i + 1]]) + " --> ", end=" ")

#print(fromCities_list[results_bellman[len(results_bellman) - 1]])
print()
print("Bellman-Ford: Shortest time between " + sourceVertex + " and " + endVertex + " is " + str(sum) + " min")
