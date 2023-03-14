class Collection:
    def __init__(self, n: int):
        self.convergence = [0] * n
        self.execution_time = [0] * n
        self.best_solution = [0] * n
        self.gap_solution = [0] * n
