class Signal:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        self.listeners.remove(listener)

    def raise_signal(self, signal_message):
        for listener in self.listeners:
            listener.signal_raised(signal_message)


class SignalListener:
    def signal_raised(self, message):
        pass
