from functools import reduce
import typing
from circuit import Circuit, Operations, SignalName, SignalValue

TSimulator = typing.TypeVar('TSimulator', bound='Simulator')


def map_value(val: str) -> SignalValue:
    if val == '0':
        return False
    return True

class Simulator:
    inputs: {int: {SignalName: SignalValue}}
    circuit: Circuit

    @staticmethod
    def read_input(lines: [str]) -> {int: {SignalName: SignalValue}}:
        clock: int = 0
        result = {clock: {}}
        for line in lines:
            # print(line, clock)
            if '+1' in line:
                clock += 1
                result[clock] = {}
                continue
            params = line.split()
            # print(params)
            signals = params[0]
            values = params[2]
            for i, signal in enumerate(signals):
                value = values[i]
                result[clock][signal] = map_value(value)
        return result

    def __init__(self: TSimulator,
                 circuit: Circuit,
                 inputs: {int: {SignalName: SignalValue}}):
        self.circuit = circuit
        self.inputs = inputs

    @staticmethod
    def compute(gate: Operations, val_a: SignalValue = None, val_b: SignalValue = None):
        match gate:
            case 'OR':
                return val_a or val_b
            case 'NOR':
                return not (val_a or val_b)
            case 'AND':
                return val_a and val_b
            case 'NAND':
                return not (val_a and val_b)
            case 'XOR':
                return val_a != val_b
            case 'XNOR':
                return val_a == val_b
            case 'NOT':
                return not val_a
            case _:
                return val_a

    def simulate_0_1(self: TSimulator) -> None:
        clock = 0
        current_state = {s: False for s in self.circuit.signals.keys()}
        state = {clock: current_state}
        while True:
            state[clock].update(self.inputs.get(clock, {}))
            # print(state[clock], self.inputs.get(clock))
            delta = 0
            d_state = {delta: state[clock].copy()}
            while True:
                delta += 1
                d_state[delta] = d_state[delta - 1].copy()
                for name, signal in self.circuit.signals.items():
                    vals = [d_state[delta - 1][inp] for inp in signal.inputs]
                    if signal.gate:
                        d_state[delta][name] = self.compute(signal.gate, *vals)
                    # print(clock, name, signal.gate, vals, d_state[delta][name])
                if delta > 0 and d_state[delta] == d_state[delta - 1]:
                    break
            state[clock] = d_state[delta]
            # print(clock, state[clock])
            if clock > 0 and clock > max(self.inputs.keys()) and state[clock] == state[clock -1]:
                break
            clock += 1
            state[clock] = state[clock - 1].copy()
        # print(state)
        return state

    def simulate_1(self: TSimulator) -> None:
        clock = 0
        current_state = {s: False for s in self.circuit.signals.keys()}
        state = {clock: current_state}
        state[clock].update(self.inputs.get(clock, {}))
        while True:
            # print(state[clock], self.inputs.get(clock))
            clock += 1
            state[clock] = state[clock - 1].copy()
            state[clock].update(self.inputs.get(clock, {}))
            # delta = 0
            # d_state = {delta: state[clock].copy()}
            for name, signal in self.circuit.signals.items():
                vals = [state[clock - 1][inp] for inp in signal.inputs]
                if signal.gate:
                    state[clock][name] = self.compute(signal.gate, *vals)
                # print(clock, name, signal.gate, vals, d_state[delta][name])
            # if delta > 0 and d_state[delta] == d_state[delta - 1]:
            #     break
            # state[clock] = d_state[delta]
            # # print(clock, state[clock])
            if clock > 0 and clock > max(self.inputs.keys()) and state[clock] == state[clock -1]:
                break
            # clock += 1
            # state[clock] = state[clock - 1].copy()
        # print(state)
        return state



    def simulate_0(self: TSimulator) -> None:
        clock = 0
        current_state = {s: False for s in self.circuit.signals.keys()}
        current_state.update(self.inputs[clock])
        state = {clock: current_state}
        last_input = max(self.inputs.keys())
        all_inputs = set(s for s, sig in self.circuit.signals.items()
                            if len(sig.inputs) == 0)
        print(all_inputs)
        while True: #clock cycle
            delta = 0
            d_state = {delta: state[clock]}
            not_computed = (set(s for s in self.circuit.signals.keys())
                            - all_inputs)
            next_in_line = reduce(
                            lambda agg, cur: agg | self.circuit.signals[cur].outputs,
                            self.inputs[clock],
                            set())

            while True: #delta cycle
                tmp_next = set()
                print(f'{next_in_line=}')
                for out in next_in_line:
                    s = self.circuit.signals[out]
                    gate = s.gate
                    inputs = (d_state[delta][inp] for inp in s.inputs)
                    d_state[delta][out] = self.compute(gate, *inputs)
                    tmp_next.update(s.outputs)
                    if out in not_computed:
                        not_computed.remove(out)

                print(f'{not_computed=}\n{delta=}\n{d_state=}\n')
                input()
                if (len(not_computed) == 0
                    and delta > 0 and d_state[delta] == d_state[delta - 1]):
                    state[clock] = d_state[delta]
                    break
                delta += 1
                d_state[delta] = d_state[delta - 1].copy()
                next_in_line = tmp_next

            if (clock >= last_input
                and clock > 0
                and state[clock] == state[clock-1]):
                break
            clock += 1
            state[clock] = state[clock - 1].copy()
        return state

