import worder


class WordStatus:
    __slots__ = ["status"]
    values = {
            "not learned": 0,
            "learned": 3,
            "after group": 1,
            "after write": 2
            }
    values.update(
            {v: k for k, v in values.items()}
            )
    def __init__(self, status: str = "not learned"):
        self.status = self.values[status]

    def get_status(self):
        return self.values[self.status]

    def add_value(self, value):
        instance = WordStatus(value)
        self.status |= instance.status
        return instance


    def __or__(self, other):
        instance = WordStatus()
        instance.status |= self.status | other.status
        return instance

    __repr__ = get_status

