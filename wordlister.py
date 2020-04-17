#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Wordlister, a simple wordlist generator and mangler written in python.\n"""

# Written By Ananke: https://github.com/4n4nk3
from itertools import permutations, islice
from multiprocessing import Pool
import argparse


def init_argparse() -> argparse.ArgumentParser:
    """Define and manage arguments passed to Wordlister via terminal.\n"""
    parser = argparse.ArgumentParser(
        description='A simple wordlist generator and mangler written in python.')
    required = parser.add_argument_group('required arguments')
    # Required arguments
    required.add_argument('--input', help='Input file name', required=True)
    required.add_argument('--perm', help='Max number of words to be combined on the same line',
                          required=True, type=int)
    required.add_argument('--min', help='Minimum generated password length', required=True,
                          type=int)
    required.add_argument('--max', help='Maximum generated password length', required=True,
                          type=int)
    # Optional arguments
    parser.add_argument('--test', help='Output first N iterations (single process/core)',
                        required=False, type=int)
    parser.add_argument('--cores',
                        help='Manually specify processes/cores pool that you want to use',
                        required=False, type=int)
    parser.add_argument('--leet', help='Activate l33t mutagen', action='store_true')
    parser.add_argument('--cap', help='Activate capitalize mutagen', action='store_true')
    parser.add_argument('--up', help='Activate uppercase mutagen', action='store_true')
    parser.add_argument('--append', help='Append chosen word (append \'word\' to all passwords)',
                        required=False)
    parser.add_argument('--prepend', help='Append chosen word (prepend \'word\' to all passwords)',
                        required=False)
    return parser


def printer(combo_printer: list):
    """Print generated words to stdout and in case apply chosen mutagens (append, prepend, leet).\n"""
    if len(set(map(str.lower, combo_printer))) == len(combo_printer):
        line_printer = ''.join(combo_printer)
        if args.min <= len(line_printer) <= args.max:
            print(line_printer)
            if args.append is not None:
                print(line_printer + args.append)
            if args.prepend is not None:
                print(args.prepend + line_printer)
            if args.leet is True:
                leet(line_printer)
    return True


def slice_and_run(single_iterator: permutations):
    """Makes slices from iterator and process them via a process pool.\n"""
    step = 10000000
    start = 0
    stop = start + step
    # I use next_it bool to make sure to create one more slice with no end limit when slices are finished
    next_it = False
    while True:
        if next_it is False:
            cake_slice = islice(single_iterator, start, stop)
        else:
            cake_slice = islice(single_iterator, start, None)
        if args.cores is None:
            with Pool() as pool:
                data = pool.map(printer, cake_slice)
        else:
            with Pool(args.cores) as pool:
                data = pool.map(printer, cake_slice)
        start += step
        stop += step
        if next_it is True:
            break
        if not data:
            next_it = True


def my_replace(line_to_mutate):
    leet_replacements = (('o', '0'), ('O', '0'), ('a', '4'), ('A', '4'), ('e', '3'), ('E', '3'),
                         ('i', '1'), ('I', '1'), ('s', '5'), ('S', '5'))
    for old_printer, new_printer in leet_replacements:
        line_to_mutate = line_to_mutate.replace(old_printer, new_printer)
    return line_to_mutate


def leet(line_leet: str):
    """Apply leet mutagen and then if needed apply append and prepend to leeted version of the string.\n"""
    line_leet = my_replace(line_leet)
    print(line_leet)
    if args.append is not None:
        print(line_leet + args.append)
    if args.prepend is not None:
        print(args.prepend + line_leet)


def test_printer(x_test: int, out_counter_test: int):
    """Test printer.\n"""
    input_list = read_input_file(args.input)
    for combo in permutations(input_list, x_test + 1):
        if len(set(map(str.lower, combo))) == len(combo):
            line = ''.join(combo)
            if args.min <= len(line) <= args.max:
                print(line)
                out_counter_test += 1
                if out_counter_test >= args.test:
                    return out_counter_test
                if args.append is not None:
                    print(line + args.append)
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                if args.prepend is not None:
                    print(args.prepend + line)
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                if args.leet is True:
                    line = my_replace(line)
                    print(line)
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                    if args.append is not None:
                        print(line + args.append)
                        out_counter_test += 1
                        if out_counter_test >= args.test:
                            return out_counter_test
                    if args.prepend is not None:
                        print(args.prepend + line)
                        out_counter_test += 1
                        if out_counter_test >= args.test:
                            return out_counter_test
    return out_counter_test


def read_input_file(file_path):
    """Read input file and return a set of words.\n"""
    input_list = set()
    try:
        with open(file_path, 'r') as input_file:
            for row in input_file:
                word = row.rstrip('\n')
                input_list.add(word)
                # Apply capitalize mutagen and upper mutagen if needed
                if args.cap is True:
                    input_list.add(word.capitalize())
                if args.up is True:
                    input_list.add(word.upper())
    except FileNotFoundError:
        print('Input file not found!\nExiting...')
    return input_list


def test_run():
    """Test run to generate only N words.\n"""
    out_counter = 0
    n_perm = args.perm
    n_test = args.test
    for x in range(n_perm):
        out_counter = test_printer(x, out_counter)
        if out_counter >= n_test:
            break


def real_run():
    """Real run.\n"""
    input_list = read_input_file(args.input)
    n_perm = args.perm
    for x in range(n_perm):
        slice_and_run(permutations(input_list, x + 1))


args = init_argparse().parse_args()

# Test run or real run
if args.test is not None:
    test_run()
else:
    real_run()
