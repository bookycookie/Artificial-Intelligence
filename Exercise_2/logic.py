import util
import functools


# Konzultacije s kolegom Mihael Matijascic prije rjesavanja labosa, pseudokod koristen s predavanja

class Labels:
    """
    Labels describing the WumpusWorld
    """
    WUMPUS = 'wumpus'
    TELEPORTER = 'teleporter'
    POISON = 'poison'
    SAFE = 'okay'

    """
    Some sets for simpler checks
    >>> if literal.label in Labels.DEADLY: 
    >>>     # Don't go there!!!
    """
    DEADLY = set([WUMPUS, POISON])
    WTP = set([WUMPUS, POISON, TELEPORTER])

    UNIQUE = set([WUMPUS, POISON, TELEPORTER, SAFE])

    POISON_FUMES = 'fumes'
    TELEPORTER_GLOW = 'glow'
    WUMPUS_STENCH = 'stench'

    INDICATORS = set([POISON_FUMES, TELEPORTER_GLOW, WUMPUS_STENCH])


def stateWeight(state):
    """
    To ensure consistency in exploring states, they will be sorted
    according to a simple linear combination.
    The maps will never be
    larger than 20x20, and therefore this weighting will be consistent.
    """
    x, y = state
    return 20 * x + y


@functools.total_ordering
class Literal:
    """
    A literal is an atom or its negation
    In this case, a literal represents if a certain state (x,y) is or is not
    the location of GhostWumpus, or the poisoned pills.
    """

    def __init__(self, label, state, negative=False):
        """
        Set all values. Notice that the state is remembered twice - you
        can use whichever representation suits you better.
        """
        x, y = state

        self.x = x
        self.y = y
        self.state = state

        self.negative = negative
        self.label = label

    def __key(self):
        """
        Return a unique key representing the literal at a given point
        """
        return (self.x, self.y, self.negative, self.label)

    def __hash__(self):
        """
        Return the hash value - this operator overloads the hash(object) function.
        """
        return hash(self.__key())

    def __eq__(first, second):
        """
        Check for equality - this operator overloads '=='
        """
        return first.__key() == second.__key()

    def __lt__(self, other):
        """
        Less than check
        by using @functools decorator, this is enough to infer ordering
        """
        return stateWeight(self.state) < stateWeight(other.state)

    def __str__(self):
        """
        Overloading the str() operator - convert the object to a string
        """
        if self.negative: return '~' + self.label
        return self.label

    def __repr__(self):
        """
        Object representation, in this case a string
        """
        return self.__str__()

    def copy(self):
        """
        Return a copy of the current literal
        """
        return Literal(self.label, self.state, self.negative)

    def negate(self):
        """
        Return a new Literal containing the negation of the current one
        """
        return Literal(self.label, self.state, not self.negative)

    def isDeadly(self):
        """
        Check if a literal represents a deadly state
        """
        return self.label in Labels.DEADLY

    def isWTP(self):
        """
        Check if a literal represents GhostWumpus, the Teleporter or
        a poisoned pill
        """
        return self.label in Labels.WTP

    def isSafe(self):
        """
        Check if a literal represents a safe spot
        """
        return self.label == Labels.SAFE

    def isTeleporter(self):
        """
        Check if a literal represents the teleporter
        """
        return self.label == Labels.TELEPORTER


class Clause:

    """
    A disjunction of finitely many unique literals.
    The Clauses have to be in the CNF so that resolution can be applied to them. The code
    was written assuming that the clauses are in CNF, and will not work otherwise.

    A sample of instantiating a clause (~B v C):

    >>> premise = Clause(set([Literal('b', (0, 0), True), Literal('c', (0, 0), False)]))

    or; written more clearly
    >>> LiteralNotB = Literal('b', (0, 0), True)
    >>> LiteralC = Literal('c', (0, 0), False)

    >>> premise = Clause(set([[LiteralNotB, LiteralC]]))
    """

    def __init__(self, literals):
        """
        The constructor for a clause. The clause assumes that the data passed
        is an iterable (e.g., list, set), or a single literal in case of a unit clause.
        In case of unit clauses, the Literal is wrapped in a list to be safely passed to
        the set.
        """
        if not type(literals) == set and not type(literals) == list:
            self.literals = set([literals])
        else:
            self.literals = set(literals)

    def isResolveableWith(self, otherClause):
        """
        Check if a literal from the clause is resolveable by another clause -
        if the other clause contains a negation of one of the literals.
        e.g., (~A) and (A v ~B) are examples of two clauses containing opposite literals
        """
        for literal in self.literals:
            if literal.negate() in otherClause.literals:
                return True
        return False

    def isRedundant(self, otherClauses):
        """
        Check if a clause is a subset of another clause.
        """
        for clause in otherClauses:
            if self == clause: continue
            if clause.literals.issubset(self.literals):
                return True
        return False

    def negateAll(self):
        """
        Negate all the literals in the clause to be used
        as the supporting set for resolution.
        """
        negations = set()
        for literal in self.literals:
            clause = Clause(literal.negate())
            negations.add(clause)
        return negations

    def __str__(self):
        """
        Overloading the str() operator - convert the object to a string
        """
        return ' V '.join([str(literal) for literal in self.literals])

    def __repr__(self):
        """
        The representation of the object
        """
        return self.__str__()

    def __key(self):
        """
        Return a unique key representing the literal at a given point
        """
        return tuple(sorted(list(self.literals)))

    def __hash__(self):
        """
        Return the hash value - this operator overloads the hash(object) function.
        """
        return hash(self.__key())

    def __eq__(first, second):
        """
        Check for equality - this operator overloads '=='
        """
        return first.__key() == second.__key()


def resolution(clauses, goal):
    """
    Implement refutation resolution.

    The pseudocode for the algorithm of refutation resolution can be found
    in the slides. The implementation here assumes you will use set of support
    and simplification strategies. We urge you to go through the slides and
    carefully design the code before implementing.
    """
    resolvedPairs = set()
    setOfSupport = goal.negateAll()  # dobili smo negaciju cilja

    # your code here
    while True:
        tmp_set = selectClauses(clauses, setOfSupport, resolvedPairs)
        if tmp_set.__len__() == 0: break

        resolvents = resolvePair(tmp_set[0], tmp_set[1])
        if resolvents.literals.__len__() == 0: return True

        setOfSupport = setOfSupport.union([resolvents])

        if setOfSupport.issubset(clauses): break

        setOfSupport = removeRedundant(setOfSupport)  # TODO PREPRAVI removeRedundant
    return False

def removeRedundant(setOfSupport):
    tmp_sos = set(setOfSupport)

    for clause in setOfSupport:
        if clause.isRedundant(tmp_sos):
            tmp_sos.remove(clause)

    return tmp_sos

def resolvePair(firstClause, secondClause):
    """
    Resolve a pair of clauses.
    """
    tmp_firstClause = Clause(firstClause.literals)
    tmp_secondClause = Clause(secondClause.literals)

    for literal in firstClause.literals:
        if literal.negate() in secondClause.literals:
            tmp_firstClause.literals.remove(literal)
            tmp_secondClause.literals.remove(literal.negate())
            if tmp_secondClause.literals.__len__() == 0:
                if tmp_firstClause.literals.__len__() == 0:
                    return Clause(set()) #vraca prazni set ako su klauzule prazne
    return Clause(tmp_firstClause.literals.union(tmp_secondClause.literals))

def selectClauses(clauses, setOfSupport, resolvedPairs): #uzeti barem 1 iz SoS (1 ili vise) i 0 ili 1 iz clauses
    """
    Select pairs of clauses to resolve.
    """

    for c1 in clauses:       #uzimanje iz clauses, SoS
        for c2 in setOfSupport:
            tmp = (c1, c2)
            if tmp in resolvedPairs:
                continue
            else:
                resolvedPairs.add(tmp)
                return tmp

    for c1 in setOfSupport:      #uzimanje iz SoS 2 puta
        for c2 in setOfSupport:
            tmp = (c1, c2)
            if tmp in resolvedPairs:
                continue
            else:
                resolvedPairs.add(tmp)
                return tmp
    return tuple()


def selectAndReturnTuple(source1, source2, duplicateCheck):
    for a in source1:
        for b in source2:
            tmp = (a, b)
            if tmp in duplicateCheck:
                continue
            else:
                duplicateCheck.add(tmp)
                return tmp
    return tuple()

def testResolution():
    """
    A sample of a resolution problem that should return True.
    You should come up with your own tests in order to validate your code.
    """
    premise1 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0), False)]))
    premise2 = Clause(set([Literal('b', (0, 0), True), Literal('c', (0, 0), False)]))
    premise3 = Clause(Literal('a', (0,0)))

    goal1 = Clause(Literal('c', (0,0)))
    print resolution(set([premise1, premise2, premise3]), goal1) #TRUE

    premise4 = Clause(set([Literal('f', (0, 0), False)]))

    goal2 = Clause(set([Literal('f', (0, 0), False), Literal('g', (0, 0), False)]))
    print resolution(set([premise4]), goal2) #TRUE

    premise5 = Clause(set([Literal('a', (0, 0), True), Literal('b', (0, 0))]))

    goal3 = Clause(set([Literal('c', (0, 0)), ]))
    print resolution(set([premise5]), goal3) #FALSE

    premise6 = Clause(set([Literal('t', (0, 0), True), Literal('u', (0, 0), False)]))
    premise7 = Clause(set([Literal('t', (0, 0), False), Literal('a', (0, 0), False)]))
    premise8 = Clause(set([Literal('u', (0, 0), True), Literal('a', (0, 0), True)]))
    goal4 = Clause(set([Literal('t', (0, 0), True), Literal('a', (0, 0), True)]))

    print resolution(set([premise6, premise7, premise8]), goal4) #FALSE

    premise9 = Clause(set([Literal('t', (0, 0), True), Literal('u', (0, 0), False)]))
    premise10 = Clause(set([Literal('t', (0, 0), False), Literal('a', (0, 0), False)]))
    premise11 = Clause(set([Literal('u', (0, 0), True), Literal('a', (0, 0), True)]))
    goal5 = Clause(set([Literal('t', (0, 0), True), Literal('a', (0, 0), True)]))


if __name__ == '__main__':
    """
    The main function - if you run logic.py from the command line by 
    >>> python logic.py 

    this is the starting point of the code which will run. 
    """
    testResolution() #TRUE, TRUE, FALSE, TRUE