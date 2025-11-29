from backend.rng import RNG  # RNG wrapper for reproducible sampling


class SpinEngine:
    def __init__(self, rng, config):
        self.rng = rng  # RNG instance (seeded upstream)
        self.config = config  # parameters such as means/stddevs and slot count

    def simulate(self):
        # Draw angular velocity and spin duration from the configured distributions.
        omega = self.rng.normal(self.config.OMEGA_MEAN, 
                                self.config.OMEGA_STD)
        tspin = self.rng.expo(self.config.TSPIN_LAMBDA)
        # Convert to landing angle, then map into a numbered slot.
        angle = (omega * tspin) % 360 # angulo q a bola cai
        slot_width = 360 / self.config.NUM_SLOTS
        slot = int(angle/slot_width)
        return {
            "omega": omega,
            "tspin": tspin,
            "angle": angle,
            "slot": slot
        }
