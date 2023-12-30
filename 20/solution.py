from __future__ import annotations

import abc
import sys

from collections import deque
from functools import reduce
from itertools import count
from operator import mul


def parse_input(file_handle) -> Network:
    network = Network()
    for line in (l.strip() for l in file_handle.readlines()):
        name,receivers_ = line.split(' -> ')
        receivers = receivers_.split(', ')
        if name == 'broadcaster':
            network.add_module(Broadcaster(name, network, receivers))
            continue
        type_ = {
            '%': FlipFlop,
            '&': Conjunction,
        }[name[0]]
        network.add_module(type_(name[1:], network, receivers))
    return network


class Module(abc.ABC):
    
    def __init__(self, name:str, network:Network, receivers:list[str]) -> None:
        self.name = name
        self.inputs:dict[str,bool] = {}
        self.output:None|bool = None
        self.network = network
        self.receivers = receivers
    
    def send(self, signal) -> None:
        self.network.broadcast(self.name, self.receivers, signal)
    
    @abc.abstractmethod
    def handle_signal(self, address:str, signal:bool) -> list[tuple[str,bool]]:
        ...
    
    def __str__(self) -> str:
        return f'{self.name}: {self.output} -> {", ".join(self.receivers)}'


class Broadcaster(Module):
    
    def __init__(self, name:str, network:Network, receivers:list[str]) -> None:
        super().__init__(name, network, receivers)
        self.output = None
    
    def handle_signal(self, address: str, signal: bool) -> None:
        self.output = signal
        self.send(signal)
    
    def __str__(self) -> str:
        return '-'+super().__str__()


class FlipFlop(Module):
    
    def __init__(self, name:str, network:Network, receivers:list[str]) -> None:
        super().__init__(name, network, receivers)
        self.output = False
    
    def handle_signal(self, address:str, signal:bool) -> tuple[str,bool]:
        if signal is False:
            self.output = not self.output
            self.send(self.output)
    
    def __str__(self) -> str:
        return '%'+super().__str__()


class Conjunction(Module):
    
    def __init__(self, name:str, network:Network, receivers:list[str]) -> None:
        super().__init__(name, network, receivers)
        self.output = False
    
    def handle_signal(self, address:str, signal:bool) -> tuple[str,bool]:
        self.inputs[address] = signal
        self.output = all(self.inputs.values())
        self.send(not self.output)
    
    def __str__(self) -> str:
        return '&'+super().__str__()


class Network:
    
    def __init__(self) -> None:
        self.modules:dict[str,Module] = {}
        self.queue = deque()
        self.pulses:dict[bool,int] = { False:0, True:0 }
        self.add_module(Broadcaster('output', self, []))
        self.add_module(Broadcaster('rx', self, []))
    
    def add_module(self, module:Module) -> None:
        self.modules[module.name] = module
    
    def reset(self):
        self.pulses = { False:0, True:0 }
        for name,module in self.modules.items():
            module.output = False
            for receiver in module.receivers:
                self.modules[receiver].inputs[name] = False
    
    def broadcast(self, sender:str, targets:list[str], signal:bool) -> None:
        for target in targets:
            self.queue.append((sender, target, signal))
        #print(self.queue)
    
    def run(self) -> None:
        global iterations
        global gate_cycle_lengths
        while self.queue:
            sender,target,signal = self.queue.popleft()
            if target=='gh' and signal is True:
                gate_cycle_lengths[sender] = iterations
            self.pulses[signal] += 1
            self.modules[target].handle_signal(sender, signal)
    
    def print(self):
        for name,module in self.modules.items():
            print(module)



def star1(problem_input:Network) -> int:
    problem_input.reset()
    for _ in range(1000):
        problem_input.broadcast('button', ['broadcaster'], False)
        problem_input.run()
    print(problem_input.pulses)
    return problem_input.pulses[False]*problem_input.pulses[True]


iterations = 0
gate_cycle_lengths = {'qx':0, 'rk':0, 'cd':0, 'zf':0}
def star2(problem_input:Network) -> int:
    global iterations
    global gate_cycle_lengths
    problem_input.reset()
    problem_input.broadcast('button', ['broadcaster'], False)
    problem_input.run()
    for iterations in count(1):
        problem_input.broadcast('button', ['broadcaster'], False)
        problem_input.run()
        if all(gcl!=0 for gcl in gate_cycle_lengths.values()):
            break
        
    print(gate_cycle_lengths.values())
    return reduce(mul, (gcl+1 for gcl in gate_cycle_lengths.values()))


if __name__ == '__main__':
    problem_input = parse_input(sys.stdin)
    print(f'*1: {star1(problem_input)}')
    print(f'*2: {star2(problem_input)}')
