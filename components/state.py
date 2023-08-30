class Timer:
    def __init__(self, obj=None):
        self.can_claim_marry: bool = False
        self.claim_reset: int = 0
        self.rolls_left: int = 0
        self.rolls_reset: int = 0
        self.daily_reset: int = 0

        if obj:
            for key in obj:
                setattr(self, key, obj[key])

    def __str__(self):
        return (
            "{can_claim_marry: %s, claim_reset: %s, rolls_left: %s, rolls_reset: %s, daily_reset: %s}"
            % (
                self.can_claim_marry,
                self.claim_reset,
                self.rolls_left,
                self.rolls_reset,
                self.daily_reset,
            )
        )


class Settings:
    def __init__(self, obj=None):
        self.marry_claim_reset: int = 0
        self.exact_minute_claim_reset: int = 0

        if obj:
            for key in obj:
                setattr(self, key, obj[key])

    def __str__(self):
        return "{marry_claim_reset: %s, exact_minute_claim_reset: %s}" % (
            self.marry_claim_reset,
            self.exact_minute_claim_reset,
        )


class State:
    def __init__(self):
        self.timeout: int = 0
        self.settings = Settings()
        self.timer = Timer()

    def __str__(self):
        return f"State: timeout: {self.timeout}, settings: {self.settings} timer: {self.timer}"
