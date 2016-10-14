
class ScoreMatrix():
    """
    Functions for manipulation of the Score Matrix for the iterated prisoner's dilemma:
    ( P1 score is on the left, P2 on the right )
            P1
            C        D
    P2  C [ 3, 3 ] [ 5, 0 ]
        D [ 0, 5 ] [ 1, 1 ]
    """

    SCORE_CC = (3, 3) # P1 = c, P2 = d
    SCORE_CD = (0, 5) # P1 = c, P2 = d
    SCORE_DD = (1, 1) # P1 = d, P2 = d
    SCORE_DC = (5, 0) # P1 = d, P2 = c

    _matrix = [[]]

    def __init__(self):
        self._matrix[0][0] = self.SCORE_CC
        self._matrix[0][1] = self.SCORE_CD
        self._matrix[1][0] = self.SCORE_DC
        self._matrix[1][1] = self.SCORE_DD

    def getScore(self, choice1, choice2):
        """
        return the corresponding scores for the 2 choices.
        Consider using a named tuple or dictionary for this method?
        :param choice1:
        :param choice2:
        :return: A tuple where (p1score, p2score)
        """
        if 'c' == choice1 and 'c' == choice2:
            return self._matrix[0][0]
        if 'c' == choice1 and 'd' == choice2:
            return self._matrix[0][1]
        if 'd' == choice1 and 'c' == choice2:
            return self._matrix[1][0]
        else:
            return self._matrix[1][1]

