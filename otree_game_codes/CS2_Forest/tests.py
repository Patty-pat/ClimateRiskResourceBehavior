from otree.api import Bot, SubmissionMustFail

from . import *


class PlayerBot(Bot):
    cases = [
        "norm",
        "pros",
        "cons",
    ]  # norm:rational behavior, pros:prosocial behav, cons:selfish behavior

    def play_round(self):
        if self.round_number >= 1:
            if self.case == "norm":
                if self.player.id_in_group == [1]:
                    for invalid_take in [-1, 8]:
                        yield SubmissionMustFail(Forest1, {"take": invalid_take})
                    yield Forest1, {"take": 3}
                elif self.player.id_in_group == [2]:
                    yield Forest1, {"take": 3}
                else:
                    yield Forest1, {"take": 3}
            elif self.case == "pros":
                if self.player.id_in_group == [1, 2]:
                    yield Forest1, {"take": 1}
                else:
                    yield Forest1, {"take": 2}
            else:
                if self.player.id_in_group == [1]:
                    yield Forest1, {"take": 6}
                elif self.player.id_in_group == [1]:
                    yield Forest1, {"take": 5}
                else:
                    yield Forest1, {"take": 7}
        else:
            pass

        if self.round_number >= 1:
            yield Forest2_regrowth

        if self.player.round_number == C.NUM_ROUNDS:
            yield Results

        if self.player.round_number == C.NUM_ROUNDS:
            yield Submission(StageDividerNext, {}, check_html=False)
