import numpy as np
import random
#@rađeno uz razmišljanje prije labosa s  mihaelom matijascicem, kao i prosla 2 labosa

class GeneticAlgorithm(object):
    """
       Implement a simple generationl genetic algorithm as described in the instructions
    """

    def __init__(self, chromosomeShape,
                 errorFunction,
                 elitism=1,
                 populationSize=25,
                 mutationProbability=.1,
                 mutationScale=.5,
                 numIterations=10000,
                 errorTreshold=1e-6
                 ):

        self.populationSize = populationSize  # size of the population of units
        self.p = mutationProbability  # probability of mutation
        self.numIter = numIterations  # maximum number of iterations
        self.e = errorTreshold  # threshold of error while iterating
        self.f = errorFunction  # the error function (reversely proportionl to fitness)
        self.keep = elitism  # number of units to keep for elitism
        self.k = mutationScale  # scale of the gaussian noise

        self.i = 0  # iteration counter

        # initialize the population randomly from a gaussian distribution
        # with noise 0.1 and then sort the values and store them internally

        self.population = []
        for _ in range(populationSize):
            chromosome = np.random.randn(chromosomeShape) * 0.1

            fitness = self.calculateFitness(chromosome)
            self.population.append((chromosome, fitness))

        # sort descending according to fitness (larger is better)
        self.population = sorted(self.population, key=lambda t: -t[1])

    def step(self):
        """
           Run one iteration of the genetic algorithm. In a single iteration,
           you should create a whole new population by first keeping the best
           units as defined by elitism, then iteratively select parents from
           the current population, apply crossover and then mutation.

           The step function should return, as a tuple:

           * boolean value indicating should the iteration stop (True if
              the learning process is finished, False othwerise)
           * an integer representing the current iteration of the
              algorithm
           * the weights of the best unit in the current iteration

        """

        self.i += 1

        new_population = self.bestN(self.keep)

        for nothing in range(0, len(self.population) - self.keep):
            p1, p2 = self.selectParents()

            child_chromosome = self.crossover(p1, p2)

            self.mutate(child_chromosome)

            child_fitness = self.calculateFitness(child_chromosome)

            new_population.append((np.array(child_chromosome), child_fitness))

        self.population = new_population
        self.population = sorted(self.population, key=lambda t: -t[1])

        best_chromosome, best_fitness = self.best()

        error = 1.0 / best_fitness

        done = False

        if self.i >= self.numIter or error < self.e:
            done = True

        return done, self.i, best_chromosome

    def calculateFitness(self, chromosome):
        """
           Implement a fitness metric as a function of the error of
           a unit. Remember - fitness is larger as the unit is better!
        """
        chromosomeError = self.f(chromosome)

        return 1.0 / chromosomeError

    def bestN(self, n):
        """
           Return the best n units from the population
        """

        # reverse_population = self.population
        bestN = []

        for i in range(0, n):
            bestN.append(self.population[i])

        return sorted(bestN, key=lambda t: -t[1])

    def best(self):
        """
           Return the best unit from the population
        """
        return self.population[0]

    def selectParents(self):
        """
           Select two parents from the population with probability of
           selection proportional to the fitness of the units in the
           population
        """
        p1 = None
        p2 = None

        fitness_sum = 0.0

        for i in range(0, len(self.population)):
            fitness_sum += self.population[i][1]

        chosen_one = np.random.uniform(0, fitness_sum)
        pie = 0

        for i in range(0, len(self.population)):
            pie += self.population[i][1]

            if chosen_one <= pie:
                p1 = self.population[i][0]
                break

        chosen_one = np.random.uniform(0, fitness_sum)
        pie = 0

        for i in range(0, len(self.population)):
            pie += self.population[i][1]

            if chosen_one <= pie:
                p2 = self.population[i][0]
                break

        return np.array(p1), np.array(p2)

    def crossover(self, p1, p2):
        """
           Given two parent units p1 and p2, do a simple crossover by
           averaging their values in order to create a new child unit
        """

        child = p1 + p2

        for i in range(0, len(child)):
            child[i] /= 2.0

        return child

    def mutate(self, chromosome):
        """
           Given a unit, mutate its values by applying gaussian noise
           according to the parameter k
        """

        for i in range(0, len(chromosome)):
            if np.random.uniform(0, 1) <= self.p:
                chromosome[i] += random.gauss(0, self.k)
