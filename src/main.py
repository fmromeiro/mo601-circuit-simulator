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
        return Simulator(circuit, inputs)

if __name__ == '__main__':
    for test in find_tests():
        circuit = build_circuit(test)
        simulator = build_simulator(test, circuit)
        state = simulator.simulate_0_1()
        signals = sorted(state[0].keys())
        max_clock = max(state.keys())

        with open(os.path.join(test, 'saida0.csv'), 'w') as f:
            print('Tempo',*signals, sep=',', file=f)
            for i in range(max_clock + 1):
                print(i, end=',', file=f)
                print(*(str(int(state[i][s])) for s in signals), sep=',', file=f)


        state = simulator.simulate_1()
        signals = sorted(state[0].keys())
        max_clock = max(state.keys())
        with open(os.path.join(test, 'saida1.csv'), 'w') as f:
            print('Tempo',*signals, sep=',', file=f)
            for i in range(max_clock + 1):
                print(i, end=',', file=f)
                print(*(str(int(state[i][s])) for s in signals), sep=',', file=f)