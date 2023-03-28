import difflib
import os
from circuit import Circuit
from simulator import Simulator

def find_tests() -> [str]:
    test_folders = [f.path for f in os.scandir('./test') if f.is_dir()]
    result = []
    for folder in test_folders:
        folder_items = set(f.name for f in os.scandir(folder))
        if {'circuito.hdl', 'estimulos.txt', 'esperado0.csv', 'esperado1.csv'}.issubset(folder_items):
            result.append(folder)
    return result

def build_circuit(test_path: os.PathLike) -> Circuit:
    with open(os.path.join(test_path, 'circuito.hdl')) as f:
        return Circuit.read_spec(f.readlines())

def build_simulator(test_path: os.PathLike, circuit: Circuit) -> Simulator:
    with open(os.path.join(test_path, 'estimulos.txt')) as f:
        inputs = Simulator.read_input(f.readlines())
        return Simulator(circuit, inputs, 1e3, 1e3)

if __name__ == '__main__':
    for test in find_tests():
        print(f'Rodando teste {test}')
        circuit = build_circuit(test)
        simulator = build_simulator(test, circuit)
        for delay in range(2):
            state = simulator.simulate(delay)
            signals = sorted(state[0].keys())
            max_clock = max(state.keys())
            output = os.path.join(test, f'saida{delay}.csv')
            expected = os.path.join(test, f'esperado{delay}.csv')

            with open(output, 'w') as f:
                print('Tempo',*signals, sep=',', file=f)
                for i in range(max_clock + 1):
                    print(i, end=',', file=f)
                    print(*(str(int(state[i][s])) for s in signals), sep=',', file=f)

            if abs(os.path.getsize(output) - os.path.getsize(expected)) > 2:
                print(f'  Teste {test} teve resultado diferente do esperado para delay {delay}')
            else:
                with open(output) as s:
                    with open(expected) as e:
                        diff = list(difflib.ndiff(s.readlines(), e.readlines(), linejunk=difflib.IS_LINE_JUNK))
                        if not all(x.startswith('  ') for x in diff):
                            print(f'  Teste {test} teve resultado diferente do esperado para delay {delay}')