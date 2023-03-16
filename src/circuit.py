from collections import namedtuple
from collections.abc import Iterable
from enum import Enum
import typing


class Operations(Enum):
    OR = auto()
    NOR = auto()
    AND = auto()
    NAND = auto()
    XOR = auto()
    XNOR = auto()
    NOT = auto()

SignalName = typing.Literal['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                            'U', 'V', 'W', 'X', 'Y', 'Z']
@dataclass
class Signal:
    name: SignalName
    gate: Operations
    inputs: Iterable[SignalName]
    outputs: Iterable[SignalName]

TCircuit = TypeVar('TCircuit', bound='Circuit')
class Circuit:
    @staticmethod
    def read_spec(lines: [str]) -> TCircuit:
        signals: {str, Signal} = {}
        for i in range(len(lines)):
            i = lines[i]
            parameters = line.split()
            signal = parameters[0]

            gate = parameters[2]
            if gate not in Operations:
                raise Exception(f'Unrecognized gate {gate} in line {i} of input')

            inputs = parameters[3:]
            row = Signal(signal, gate, inputs, set())

        for signal in signals:
            for in_sig in signal.inputs:
                signals[in_sig].out.append(signal)

        return Circuit(signals)

    def __init__(self: TCircuit, signals: Iterable[Signal]):
        self.signals = signals