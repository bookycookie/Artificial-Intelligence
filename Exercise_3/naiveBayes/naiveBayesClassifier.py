import util
import math

#@Komentiranje problematike labosa s kolegom Mihael Matijascic
class NaiveBayesClassifier(object):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels, smoothing=0, logTransform=False, featureValues=util.Counter()):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = int(smoothing) # this is the smoothing parameter, ** use it in your train method ** #brojnik +1, nazivnih .totalCount*feature (?)
        self.logTransform = logTransform
        self.featureValues = featureValues # empty if there is no smoothing

    def fit(self, trainingData, trainingLabels):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the smoothed estimates so that they can be used to classify.
        
        trainingData is a list of feature dictionaries.  The corresponding
        label lists contain the correct label for each instance.

        To get the list of all possible features or labels, use self.features and self.legalLabels.
        """

        self.features = trainingData[0].keys() # the names of the features in the dataset

        self.prior = util.Counter() # probability over labels
        self.conditionalProb = util.Counter() # Conditional probability of feature feat for a given class having value v
                                      # HINT: could be indexed by (feat, label, value)

        # TODO:
        # construct (and store) the normalized smoothed priors and conditional probabilities

        # hmap = argmax[ P(hi) * P(all Features | hi) ]

        "*** YOUR CODE HERE ***"


        counter_apriori = util.Counter()

        for label in trainingLabels:
            counter_apriori[label] += 1
            continue

        #legalLabels = self.legalLabels

        for label in self.legalLabels:
            self.prior[label] = float(counter_apriori[label]) / len(trainingLabels) #racunanje a priori vjerojatnosti

        #self.prior.normalize()

        counter_likelihood = util.Counter()

        counter = 0
        for dict_td in trainingData:
            for feature in self.features:
                feature_label_value = (feature, trainingLabels[counter], dict_td[feature])
                counter_likelihood[feature_label_value] += 1
            counter += 1


        for feature, label, value in counter_likelihood.keys():
            num = 0
            if self.featureValues.get(feature) != 0: #neke vrijednosti u featureValue su tipa True, False, neke samo True/False, ALI neke su int 0, tako da imam pomocnu varijablu koji ce taj slucaj rjesavati
                num = len(self.featureValues.get(feature))
            self.conditionalProb[(feature, label, value)] = (float(counter_likelihood[(feature, label, value)] + self.k) / (counter_apriori[label] + self.k * num))

            #P(hi|e) = (P(e|hi) + K)/(P(hi) + K*brojVrijednostiZnacajki
        #self.conditionalProb.normalize()



    def predict(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """

        guesses = []
        self.posteriors = [] # posterior probabilities are stored for later data analysis.

        for instance in testData:
            if self.logTransform:
                posterior = self.calculateLogJointProbabilities(instance)
            else:
                posterior = self.calculateJointProbabilities(instance)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses


    def calculateJointProbabilities(self, instance):
        """
        Returns the joint distribution over legal labels and the instance.
        Each probability should be stored in the joint counter, e.g.
        Joint[3] = <Estimate of ( P(Label = 3, instance) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        joint = util.Counter()
        legalLabels = self.legalLabels
        features = self.features

        for label in legalLabels:
            # calculate the joint probabilities for each class
            "* YOUR CODE HERE *"
            product = self.prior[label]
            for feature in features:
                product *= self.conditionalProb[feature, label, instance[feature]]

            joint[label] = product

        return joint


    def calculateLogJointProbabilities(self, instance):
        """
        Returns the log-joint distribution over legal labels and the instance.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, instance) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()
        legalLabels = self.legalLabels
        features = self.features

        for label in legalLabels:
            # calculate the log joint probabilities for each class
            "* YOUR CODE HERE *"
            sum = math.log(self.prior[label])
            for feature in features:
                sum += math.log(self.conditionalProb[feature, label, instance[feature]])

            logJoint[label] = sum

        return logJoint
