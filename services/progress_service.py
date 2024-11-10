class ProgressService:
    def __init__(self):
        self._status = "Idle"

    def update_status(self, status):
        self._status = status
        print(status)  # Logging untuk debugging

    def get_status(self):
        return self._status
