"""Entry point for Caliban's experiment config expansion."""

from __future__ import absolute_import, division, print_function

import json
import logging as ll
from typing import List

from absl import app, logging
from absl.flags import argparse_flags

import caliban.config as c
from caliban import __version__

ll.getLogger('caliban.expansion').setLevel(logging.ERROR)


def expansion_parser():
  """Creates and returns the argparse instance for the experiment config
  expansion app.

  """

  parser = argparse_flags.ArgumentParser(
      description=
      "Experiment config expander. For documentation, visit http://go/caliban",
      prog="expansion")
  parser.add_argument('--version',
                      action='version',
                      version="%(prog)s {}".format(__version__))
  parser.add_argument("--pprint",
                      action="store_true",
                      help="Pretty-print the config to stdout.")
  parser.add_argument(
      "--print_flags",
      action="store_true",
      help=
      "Print the actual flags generated by each experiment in the expansion, \
one per line.")
  parser.add_argument(
      "experiment_config",
      type=c.load_experiment_config,
      help="Path to an experiment config, or 'stdin' to read from stdin.")

  return parser


def parse_flags(argv):
  """Function required by absl.app.run. Internally generates a parser and returns
  the results of parsing caliban arguments.

  """
  args = argv[1:]
  return expansion_parser().parse_args(args)


def _print_flags(expanded: List[c.Experiment]) -> None:
  """Print the flags associated with each experiment in the supplied expansion
  list.

  """
  for m in expanded:
    flags = c.experiment_to_args(m)
    print(' '.join(flags))


def _print_json(expanded: List[c.Experiment], pprint: bool = False) -> None:
  """Print the list of expanded experiments to stdout; if pprint is true,
  pretty-prints each JSON dict using an indent of 2, else prints the list with
  no newlines.

  """
  indent = 2 if pprint else None
  print(json.dumps(expanded, indent=indent))


def run_app(args):
  """Main function to run the Caliban app. Accepts a Namespace-type output of an
  argparse argument parser.

  """
  conf = args.experiment_config
  expanded = c.expand_experiment_config(conf)

  if args.print_flags:
    _print_flags(expanded)
  else:
    _print_json(expanded, pprint=args.pprint)


def main():
  app.run(run_app, flags_parser=parse_flags)


if __name__ == '__main__':
  main()
