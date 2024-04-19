class Statistics:
    """
    This class saves the best in the server since it began to run
    """
    def __init__(self):
        self.best_team = ""
        self.best_score = 0

    def update(self, best_team, best_score):
        """
        Checks if best score should be updated and updates
        :param best_team: New team name
        :param best_score: New team's score
        :return:
        """
        if best_score > self.best_score:
            self.best_score = best_score
            self.best_team = str(best_team)
