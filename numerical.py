import numpy as np


class DieGame:

    def __init__(self, threshold, W, sides=(2, 4, 8, 16, 32, 64)):
        self.threshold = threshold
        self.W = W
        self.crit_point = threshold - W + 1

        sides, sides_low, sides_high, sides_all = [list(sides) for i in range(4)]
        self.sides_null = tuple(sides)
        sides_low.insert(0, 1)
        self.sides_low = tuple(sides_low)
        sides_high.insert(0, W)
        self.sides_high = tuple(sides_high)
        sides_all.insert(0, 1); sides_all.insert(0, W)
        self.sides_all = tuple(sides_all)
        del sides, sides_low, sides_high, sides_all

        self.score_paths = self._calculate_path_data()

    def _calculate_path_data(self):

        def main():

            known = {}
            sub_thresh = [count_paths(i, known) for i in range(0, self.threshold + 1)]

            end_points = range(
                self.threshold + 1,
                self.threshold + 1 + max(self.sides_high)
            )

            # return paths vs steps data for n > threshold
            return [count_paths_end(i, sub_thresh) for i in end_points]


        def add_paths(acc, prec):
            """
            add paths count  vs steps distribution for preceding node to
            accumulator for current node
            """
            for num_steps, num_paths in prec.items():
                try:
                    acc[num_steps + 1] += num_paths
                except KeyError:
                    acc[num_steps + 1] = num_paths


        def count_paths(n, known):
            """
            Calculate paths count vs steps distribution for n < threshold.
            """
            if n in known:
                return known[n]

            paths_vs_steps = {}

            if 0 <= n <= self.crit_point:
                sides = self.sides_high   # (11, 2, ..., 64)
            elif n <= self.threshold:
                sides = self.sides_all    # (1, 11, 2, ..., 64)
            else:
                raise ValueError('invalid n')

            for s in sides:
                prec = n - s
                if prec > 0:
                    # insert path data from preceding
                    add_paths(paths_vs_steps, count_paths(prec, known))
                elif prec == 0:
                    paths_vs_steps[1] = 1

            known[n] = paths_vs_steps

            return paths_vs_steps




        def count_paths_end(n, sub_thresh_data):
            """
            Calculate paths count vs steps distribution for n > threshold. See readme.
            """

            paths_vs_steps = {}
            for s in self.sides_low:
                prec = n - s
                if 0 < prec <= self.threshold:
                   add_paths(paths_vs_steps, sub_thresh_data[prec])
                elif prec == 0:
                    paths_vs_steps[1] = 1

            return paths_vs_steps

        return main()

    @staticmethod
    def dict_to_arr(distr):
        x = np.array([num_steps for num_steps in distr])
        y = np.array([num_paths for num_steps, num_paths in distr.items()])

        return np.array((x, y))
    
    @staticmethod
    def apply_prob(distr, num_choices):
        """
        Accepts num paths (existing) vs num steps, returns num paths (taken)
        vs num steps. Shorter paths are more likely to be traversed. See readme.
        """
        x, y = distr

        # y = y / np.power(num_choices, x)
        y = y * np.power(float(num_choices), np.negative(x))

        return np.array((x, y))

    @staticmethod
    def sum_paths(distr):
        """
        Accepts num paths (taken) vs num steps, returns total number of paths (taken).
        """
        x, y = distr

        return np.sum(y)

    
    def get_scores(self):
        """ return number of paths (taken) vs scores """
        score_data = self.score_paths
        score_data = [self.dict_to_arr(distr) for distr in score_data]
        n = len(self.sides_null) + 1
        score_data = [self.apply_prob(distr, n) for distr in score_data]
        score_data = [self.sum_paths(distr) for distr in score_data]
        scores = np.arange(max(self.sides_high)) + 1
        paths = np.array(score_data)

        return (scores, paths)


    def get_steps(self):
        """ return number of paths (taken) vs steps """
        step_data = self.score_paths
        step_data = [self.dict_to_arr(distr) for distr in step_data]
        n = len(self.sides_null) + 1
        step_data = [self.apply_prob(distr, n) for distr in step_data]

        distr_global = {}

        for distr in step_data:
            num_steps, num_paths = distr

            for s, p in zip(num_steps, num_paths):
                try:
                    distr_global[s] += p
                except KeyError:
                    distr_global[s] = p

        return self.dict_to_arr(distr_global)
