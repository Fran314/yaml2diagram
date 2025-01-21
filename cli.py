import argparse

parser = argparse.ArgumentParser(prog='yaml2diagram', description='Convert a YAML file describing a diagram into an html file with the render of the diagram')
parser.add_argument('input', help='yaml input file')
parser.add_argument('output', help='html output file')

args = parser.parse_args()
