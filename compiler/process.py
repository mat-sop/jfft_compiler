from config import CONST_PREFIX, ITERATOR_PREFIX
from generator.const import gen_const


def process(commands, memory_manager):
    commands = resolve_constances(commands, memory_manager)
    commands = determine_jumps(commands)
    commands = resolve_iterators(commands, memory_manager)
    return commands


def validate(commands):
    iterators = []
    for c in commands:
        if '###' not in c:
            continue
        elif 'iterator_start' in c:
            iterators.append(c.split('___'[-1]))
        elif 'iterator_end' in c:
            iterators.remove(c.split('___'[-1]))
            

def determine_jumps(commands):
    for i in range(len(commands)):
        if 'k_' in commands[i]:
            k_diff = int(commands[i].split('_')[-1])
            jmp = commands[i].split(' ')[0]
            commands[i] = f'{jmp} {i+k_diff}'
    return commands


def resolve_constances(commands, memory_manager):
    generated = []
    constants = {}
    for n in memory_manager.constants:
        i = memory_manager.get_free_index()
        generated += gen_const(n, i)
        constants[n] = i

    for i in range(len(commands)):
        if CONST_PREFIX in commands[i]:
            n = int(commands[i].split('_')[-1])
            c = commands[i].split(' ')[0]
            commands[i] = f'{c} {constants[n]}'
    return generated + commands


def resolve_iterators(commands, memory_manager):
    indexes = {}
    for i in range(len(commands)):
        if ITERATOR_PREFIX in commands[i]:
            iterator = commands[i].split('_')[-1]
            if iterator not in indexes:
                indexes[iterator] = memory_manager.get_free_index()
            index = indexes[iterator]
            c = commands[i].split(' ')[0]
            commands[i] = f'{c} {index}'
    return commands
