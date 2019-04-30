import random
from collections import Counter

def readFile(fileName):
  lines = open(fileName, "r").readlines()
  inputData = []
  for line in lines:
    temp = line.split(",")
    newTemp = []
    for item in temp:
      newTemp.append(int(item))
    inputData.append(newTemp)
  return inputData


def createRandomPopulation(numberOfCities, populationSize):
  newPopulation = []
  while len(newPopulation) < populationSize:
    valueList = list(range(0, numberOfCities))
    random.shuffle(valueList)
    newPopulation.append(valueList)
  return newPopulation


def costFunction(member, costMatrix):
  costSum = 0
  for i in range(1, len(member)):
    costSum += costMatrix[member[i-1]][member[i]]
  costSum += costMatrix[member[0]][member[len(member)-1]]
  return costSum


def checkConvergence(population, convergenceRate):
  listToString = []
  for member in population:
    listToString.append(''.join(str(member)))
  c = Counter(listToString)
  rate = c.most_common(1)[0][1] / float(len(population))
  return rate >= convergenceRate


def assessPopulationFitness(population, costMatrix):
  return [[costFunction(member, costMatrix), member] for member in population]


def fittestPopulation(population, costMatrix):
  fittestPopulation = []
  populationResults = assessPopulationFitness(population, costMatrix)
  for i in range(len(population)):
    randIndex1 = random.randint(0,len(population)-1)
    randIndex2 = random.randint(0,len(population)-1)
    if populationResults[randIndex1][0] < populationResults[randIndex2][0]:
      fittestPopulation.append(populationResults[randIndex1][1]) 
    else: 
      fittestPopulation.append(populationResults[randIndex2][1]) 
  return fittestPopulation


def mutatePopulation(population, mutationRate):
  mutatedPopulation = []
  for i in range(len(population)):
    if random.random() <= mutationRate:
      member = population[i]
      randMutationIndex1 = random.randint(0, len(member)-1)
      randMutationIndex2 = random.randint(0, len(member)-1)
      temp = member[randMutationIndex1]
      member[randMutationIndex1] = member[randMutationIndex2]
      member[randMutationIndex2] = temp
      mutatedPopulation.append(member)
    else:
      mutatedPopulation.append(population[i])
  return mutatedPopulation


def crossoverPopulation(population, crossoverRate):
  newPopulation = []
  for i in range(len(population)):
    if random.random() <= crossoverRate:
      member = population[i]
      mateIndex = random.randint(0, len(population)-1)
      while mateIndex == i:
        mateIndex = random.randint(0, len(population)-1)
      mate = population[mateIndex]
      cut1 = random.randint(0, len(member)-1)
      cut2 = random.randint(0, len(member)-1)
      while (cut2 - cut1) <= 1:
        cut1 = random.randint(0, len(member)-1)
        cut2 = random.randint(0, len(member)-1)
      newMember = []
      for i in range(len(member)):
        newMember.append(-1)
      lookupDict = {}
      for i in range(cut1+1, cut2):
        newMember[i] = mate[i]
        lookupDict[mate[i]] = member[i]
      for i in range(len(member)):
        if i <= cut1 or i >= cut2:
          candidate = member[i]
          while candidate in newMember:
            candidate = lookupDict[candidate]
          newMember[i] = candidate
      newPopulation.append(newMember)
    else:
      newPopulation.append(population[i])
  return newPopulation




# func: minimize distance traveled

# chromosome representation
# genes on chromosome
# mutation rate
# crossover rate
# one or two point cross over
# tournament selection binary
# full replacement




def setup():
  costMatrix = readFile("data.txt")
  numberOfCities = len(costMatrix)
  convergenceRate = 0.95
  populationSize = 20
  mutationRate = 0.05
  crossoverRate = 0.6
  population = createRandomPopulation(numberOfCities, populationSize)

  iterations = 0
  while checkConvergence(population, convergenceRate) is not True:
    iterations += 1

    bestPopulation = fittestPopulation(population, costMatrix)
    mutatedPopulation = mutatePopulation(bestPopulation, mutationRate)
    bredPopulation = crossoverPopulation(mutatedPopulation, crossoverRate)
    population = bredPopulation
  print(iterations)
  print(costFunction(population[0], costMatrix))
setup()


