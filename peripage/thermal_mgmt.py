import time, math
import typing

# pucgenie: We could calculate decay_factor outside of this class because elapsed_time should "stay" almost the same anyway

class ExponentiallyDecayingValueRowWithBleed:
    """
    authors: pucgenie, Google Gemini
    """
    def __init__(self, values: list[float],):
        self.values = values
        self.last_time = time.time()

    def elapse_time(self, now_time: float,) -> float:
        elapsed_time = now_time - self.last_time
        self.last_time = now_time
        return elapsed_time

    def add(self, values: list[float], decay_rate: float, now_time: float,) -> float:
        if len(values) != len(self.values):
            raise ValueError(f"Expected list size differs by {len(self.values) - len(values)}")
        return self.add(values, math.exp(-decay_rate * self.elapse_time(now_time)),)

    def add(self, values: list[float], decay_factor: float,) -> float:
        """
        Applies decay, adds new values, bleeds to neighbors.
        Higher decay_rate means faster decay.

        Returns the maximum after calculating new values.
        """
        forward_bleed: typing.Final[float] = 0
        return_max = 0.0
        for i, add_value in enumerate(values):
            # Standard (core) formula by Gemini: N(t) = N0 * e^(-λt)
            new_val = self.values[i] * decay_factor + add_value + forward_bleed
            self.values[i] = new_val
            if new_val > return_max:
                return_max = new_val
            if add_value > 0:
                forward_bleed = add_value / 4
                if i > 0:
                    new_val = self.values[i-1] + forward_bleed
                    self.values[i-1] = new_val
                    if new_val > return_max:
                        return_max = new_val
            else:
                forward_bleed = 0
        
        return return_max
