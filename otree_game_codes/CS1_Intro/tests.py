from otree.api import Bot

from . import *


class PlayerBot(Bot):
    cases = [
        "norm",
        "pros",
        "cons",
    ]  # norm: normal behavior, pros:prosocial behav, cons:selfish behavior

    def play_round(self):
        yield P02Welcome, {}
        yield Submission(StageDivider, {"foo": 99}, check_html=False)
        yield P03InstructionsN, {}

        yield P04Example, {}

        if self.case == "norm":
            yield P05ComprehensionCheck, {
                "compr1": 1,
                "compr2": 0,
                "compr3": 7,
                "compr4": 1,
                "compr5": 0,
            }
        elif self.case == "pros":
            yield P05ComprehensionCheck, {
                "compr1": 1,
                "compr2": 0,
                "compr3": 7,
                "compr4": 1,
                "compr5": 0,
            }
        else:
            yield P05ComprehensionCheck, {
                "compr1": 1,
                "compr2": 0,
                "compr3": 7,
                "compr4": 1,
                "compr5": 0,
            }

        yield P06ComprehensionSuccess, {"code": 2206}
