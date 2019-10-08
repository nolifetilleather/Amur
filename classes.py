

class Signal:

    def __init__(
            self,
            name,
            plc,
            signal_type=None,
            position=None,
            location=None,
            ff_out=None,
            device=None,
            address=None,
    ):
        self.name = name
        self.plc = plc
        self.signal_type = signal_type
        self.position = position
        self.location = location
        self.ff_out = ff_out
        self.device = device
        self.address = address

    
