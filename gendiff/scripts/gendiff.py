#!/usr/bin/env python3
import argparse


parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')

parser.parse_args()

