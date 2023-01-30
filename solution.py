class Solution:
    def __init__(self):
        self.best = 0
        self.best_individual = []
        self.convergence = []
        self.optimizer = ""
        self.objfname = ""
        self.start_time = 0
        self.end_time = 0
        self.execution_time = 0
        self.lb = 0
        self.ub = 0
        self.dim = 0
        self.pop_num = 0
        self.maxiers = 0
        self.instance = ""
        self.routes = []
