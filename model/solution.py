import time


class Solution:
    def __init__(self, optimizer="HHOCVRP"):
        self.bks = 0
        self.best = 0
        self.best_individual = []
        self.convergence = []
        self.optimizer = optimizer
        self.objfname = ""
        self.timer_start = 0
        self.timer_end = 0
        self.execution_time = 0
        self.lb = 0
        self.ub = 0
        self.dim = 0
        self.name = ""
        self.routes = []
        self.coordinates = []

    def gap(self):
        """
        Calculate gap of two route in percentage. If the result is positive number,
        that means bks has name better value, and vice versa

        Returns
        -------
        gap : number
            the gap of bks and bs (in percentage)
        """

        return (self.best - self.bks) * 100 / self.bks

    def start_timer(self):
        """Start the timer for testing"""
        self.timer_start = time.time()

    def stop_timer(self):
        """Stop the timer for testing"""
        self.timer_end = time.time()
        self.execution_time = self.timer_end - self.timer_start
