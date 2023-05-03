import random


class Model:
    best_fit = None  # Highest Scoring set of weights so far

    '''Generator for the genetic algorithm. 
    func            The scoring function that takes inputs as a single list
    ranges          list of dicts, [{"min": num, "max": num},...] Acceptable ranges for each value.
    parent_count    Number of parents per generation
    generations     number of generations
    mutation        percent chance of a mutation (major rerolls, minor slightly adjusts)
    variance        proportional amount to adjust in event of a minor mutation (.1 = up to 10% shift)'''
    def __init__(self, func, ranges, ancestors=5, generations=50,
                 major_mutation_chance=0.01, minor_mutation_chance=0.2, variance=0.2):
        # Save data for later
        self.score_function = func
        self.ranges = ranges
        self.generations = generations
        self.ancestors = ancestors
        self.minor_mutation_chance = minor_mutation_chance
        self.variance = variance
        self.major_mutation_chance = major_mutation_chance

        # Build initial parent set
        weights = len(self.ranges)
        self.parents = []
        for i in range(self.ancestors):
            parent = []
            for gene in range(weights):
                parent.append(self.get_mutation(gene))
            self.parents.append(parent)

    '''Central place to create new genes in case we want to override or change later.
    gene       Number referring to which value to create [w0x0 would be 0, for example. Zero indexed.
    Returns a new gene uniformly placed in the defined range'''
    def get_mutation(self, gene):
        return random.uniform(self.ranges[gene]["min"], self.ranges[gene]["max"])

    '''Steps forward a given number of generations, updating the parents and best fit as it goes.
    generations     Number of generations to step forward (a local override)
    Returns the best fit'''
    def train(self, generations=None):
        # This can be done in multiple stages, so this allows overriding defaults
        if generations is None:
            generations = self.generations
        for i in range(generations):
            children = self.breed(self.parents)
            children.sort(reverse=True, key=self.score_function)
            if self.best_fit is None or self.score_function(children[0]) > self.score_function(self.best_fit):
                self.best_fit = children[0]
            self.parents = children[:self.ancestors]
        return self.best_fit

    '''Takes the current set of parents and builds a generation from them. Each weight has
    a 50/50 chance of being taken from each parent (May override this later, will note here).
    parents         A list of parents (each parent is a list of values)
    Returns a list of children. '''
    def breed(self, parents):
        children = []
        for i in range(len(parents)):
            for j in range(len(parents)):
                if i == j:  # No asexual parents here
                    continue
                mother = parents[i]  # These names are completely arbitrary and will make no sense if I ever
                father = parents[j]  # change it to allow more than two parents. ¯\_(ツ)_/¯
                child = []
                for gene in range(len(mother)):
                    if random.random() < self.major_mutation_chance:
                        child.append(self.get_mutation(gene))
                    elif random.random() > 0.5:
                        child.append(mother[gene])
                    else:
                        child.append(father[gene])
                    # Now we handle minor mutations of the parent genes
                    if random.random() < self.minor_mutation_chance:
                        new_gene = child[gene] * random.uniform(1-self.variance, 1+self.variance)
                        low = self.ranges[gene]["min"]
                        high = self.ranges[gene]["max"]
                        child[gene] = min(max(new_gene, low), high)
                children.append(child)
        return children

