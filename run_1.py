from meteor_reasoner.graphutil.graph import *
from meteor_reasoner.materialization.index_build import *
from meteor_reasoner.materialization.materialize import materialize
import argparse
from meteor_reasoner.materialization.coalesce import coalescing_d

parser = argparse.ArgumentParser()
parser.add_argument("--datapath", required=True, type=str, help="Input the dataset path")
parser.add_argument("--rulepath", required=True, type=str, help="Input the program path")
parser.add_argument("--steps", default=100, type=int, help="Input the number of rule applications")
args = parser.parse_args()


if __name__ == "__main__":
    print("================ Begin to load the dataset and the program ============\n")
    with open(args.rulepath) as file:
        raw_program = file.readlines()
        program = load_program(raw_program)
        predicates = set()
        for rule in program:
            predicates.add(rule.head.get_predicate())
            for literal in rule.body:
                if isinstance(literal, BinaryLiteral):
                    predicates.add(literal.left_literal.get_predicate())
                    predicates.add(literal.right_literal.get_predicate())
                else:
                    predicates.add(literal.get_predicate())

    with open(args.datapath) as file:
        lines = file.readlines()
        raw_data = []
        for line in lines:
            for predicate in predicates:
                if line.startswith(predicate):
                     raw_data.append(line)
                     break

        D = load_dataset(raw_data)
        coalescing_d(D)
        D_index = build_index(D)
    print("================ End of the loading ============\n")
    print("================ Begin to do materialization ============")

    materialize(D, program, D_index, K=args.steps)

    print("================ End ============\n")