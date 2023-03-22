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
            parameters = line.split()
            # print(parameters)
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
            # print(name, signal)
            for in_sig in signal.inputs:
                signals[in_sig].outputs.add(name)

        return Circuit(signals)

    def find_order(self: TCircuit, signals: {SignalName, Signal}) -> [SignalName]:
        sigs = set(signals.keys())
        inputs = [sig.name for sig in signals.values() if len(sig.inputs) == 0]
        ready = set(inputs)
        sigs = [x for x in sigs if x not in inputs]
        sorting = []
        while sigs:
            last_ready = ready.copy()
            i = 0
            while True:
                if i >= len(sigs):
                    break
                sig = sigs[i]
                signal = signals[sig]
                if set(signal.inputs) <= ready:
                    sigs.remove(sig)
                    ready.add(sig)
                    sorting.append(sig)
                else:
                    i += 1
            if last_ready == ready:
                deps = {1: [], 2: []}
                for s in sigs:
                    deps[len(signal[s].inputs - ready)].append(s)
                sig = None
                if deps[1]:
                    sig = deps[1][0]
                else:
                    sig = deps[2][0]
                sigs.remove(sig)
                ready.add(sig)
                sorting.append(sig)
        return sorting

    def find_order2(self: TCircuit, signals: {SignalName, Signal}) -> [SignalName]:
        permanent = set()
        temporary = set()
        sigs = set(signals.keys())
        sorting = []

        def visit(n):
            if n in permanent:
                return
            if n in temporary:
                return

        while sigs - permanent:
            n = next(iter(sigs - permanent))
            visit(n)


    def __init__(self: TCircuit, signals: {SignalName, Signal}):
        self.signals = signals
        self.order = self.find_order(signals)
