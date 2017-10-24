import random
import numpy as np
import numpy.random as nr
from collections import Counter


class DieGameSim:
    def __init__(
            self,
            threshold,
            W,
            sides=(2, 4, 8, 16, 32, 64),
            samps=int(5e5)
    ):
        self.threshold = threshold
        self.W = W

        sides = list(sides)
        sides.insert(0, -1)          # -1 is stand in for W
        self.sides = tuple(sides)

        data = np.array([self._simulate() for i in range(samps)])
        self.scores = data[:, 0]
        self.steps = data[:, 1]



    def _simulate(self):

        # batch generate gumballs beforehand for efficiency
        dispensed = list(nr.choice(self.sides, self.threshold))

        chewed = 0
        count = 0
        while chewed <= self.threshold:
            gb = dispensed.pop()
            count += 1
            if gb == -1:    # if gb is W
                if chewed + self.W > self.threshold:
                    gb = 1
                else:
                    gb = self.W
            chewed += gb

        score = chewed - self.threshold
        return score, count

    def get_scores(self):
        score_counts = Counter(self.scores)
        scores = [score for score in score_counts]
        hits = [count for score, count in score_counts.items()]
        return (scores, hits)

    def get_steps(self):
        step_counts = Counter(self.steps)
        steps = [steps for steps in step_counts]
        counts = [count for score, count in step_counts.items()]
        return (steps, counts)



