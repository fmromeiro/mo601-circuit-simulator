from collections.abc import Iterable
from dataclasses import dataclass
from functools import reduce
import typing


Operations = typing.Literal['OR', 'NOR', 'AND', 'NAND', 'XOR', 'XNOR', 'NOT']
SignalValue = bool
SignalName = typing.Literal['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                            'U', 'V', 'W', 'X', 'Y', 'Z']


@dataclass
class Signal:
    name: SignalName
    gate: Operations
    inputs: Iterable[SignalName]
    outputs: Iterable[SignalName]


TCircuit = typing.TypeVar('TCircuit', bound='Circuit')


class Circuit:
    signals: {SignalName, Signal}
    order: [SignalName]

    @staticmethod
    def read_spec(lines: [str]) -> TCircuit:
        signals: {str, Signal} = {}
        for i, line in enumerate(lines):
            if not line:
                continue
            parameters = line.split()
            name = parameters[0]

            gate = parameters[2]
            if gate not in ['OR', 'NOR', 'AND', 'NAND', 'XOR', 'XNOR', 'NOT']:
                raise Exception(
                    f'Unrecognized gate {gate} in line {i} of input')

            inputs = parameters[3:]
            row = Signal(name, gate, inputs, set())
            signals[name] = row
            for inp in inputs:
                if inp not in signals:
                    signals[inp] = Signal(inp, '', set(), set())

        for name, signal in signals.items():
            for in_sig in signal.inputs:
                signals[in_sig].outputs.add(name)

        return Circuit(signals)

    def __init__(self: TCircuit, signals: {SignalName, Signal}):
        self.signals = signals
