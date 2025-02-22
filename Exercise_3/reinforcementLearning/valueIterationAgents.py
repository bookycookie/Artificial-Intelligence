# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()

        for i in range(0, self.iterations):

            valueState = util.Counter()

            candidate_state = mdp.getStates()
            for state in candidate_state:
                if mdp.isTerminal(state):
                    pass

                else:
                    valueAction = util.Counter()
                    candidate_action = mdp.getPossibleActions(state)

                    for action in candidate_action:
                        valueAction[action] = self.computeQValueFromValues(state, action)
                   #najbolja vrijednost za state
                    valueState[state] = max(valueAction.values())
            i += 1

            self.values = valueState

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]
##################################################33FIXME MOZDA NIJE PRAVI QVALUE
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #u listu parova smjestam nextState, prob od mdp-a
        listPairs = self.mdp.getTransitionStatesAndProbs(state, action)

        qValue = 0

        gamma = self.discount #faktor raspadanja, oznaka gamma

        for nextState, prob in listPairs:

            reward = self.mdp.getReward(state, action, nextState) #R(s, a, s')
            nextStateValue = self.values[nextState] #(Vk(s'))

            qValue = qValue + prob * (reward + gamma * nextStateValue)
            #Vk+1(s) = maxAction(sumBys' T(s, a, s') * [R(s, a, s') + gamma * Vk(s')]
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions = self.mdp.getPossibleActions(state)

        # Note that if
        #           there are no legal actions, which is the case at the
        #           terminal state, you should return None.
        if not actions:
            return None

        value = util.Counter()

        for action in actions:
            value[action] = self.computeQValueFromValues(state, action)
            #prolazim kroz sve moguce akcije i nalazim maksimalnu akciju
            maxAction = value.argMax()

        return maxAction


    def getPolicy(self, state):

        policy = self.computeActionFromValues(state)

        return policy

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."

        action = self.computeActionFromValues(state)

        return action

    def getQValue(self, state, action):

        qValue = self.computeQValueFromValues(state, action)

        return qValue