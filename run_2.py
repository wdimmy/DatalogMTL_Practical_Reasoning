from meteor_reasoner.automata.buichi_automata import *
from meteor_reasoner.materialization.materialize import materialize
from meteor_reasoner.automata.automaton import consistency
from meteor_reasoner.utils.entail_check import entail
from meteor_reasoner.materialization.index_build import *
import argparse

D, program, F, fixpoint = None, None, None, False


def call_mat(D, program, F):
    CF = CycleFinder(program=program)
    program = CF.get_revevant_rules(F.get_predicate())
    CF = CycleFinder(program=program)
    if len(CF.loop) == 0:  # it is a non-recursive program
        while True:
            flag = materialize(D, rules=program)
            if entail(F, D):
                return True, "Materialisation"
            else:
                if flag:
                    return False, "Materialisation"
    else:
        while True:
            fixpoint = materialize(D, rules=program, K=1)
            if fixpoint:
                if entail(F, D):
                    return True, "Materialisation"
                else:
                    return False, "Materialisation"
            else:
                if entail(F, D):
                    return True, "Materialisation"


def call_automata(D, program, F):
    flag = consistency(D, program, F)
    if flag:
        return True, "Automata"
    else:
        return False, "Automata"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datapath", default="./datasets/fig1_left/itemporal_data_1", type=str, help="Input the dataset path")
    parser.add_argument("--rulepath", default="./programs/fig1_left/itemporal_program_1",  type=str, help="Input the program path")
    parser.add_argument("--factpath",
                        default="",
                        type=str, help="Input the fact path you wanna check the entailment")
    parser.add_argument("--fact",
                        default="g528(710,822,404)@[44,47]",
                        type=str, help="Input the fact you wanna check the entailment")
    parser.add_argument("--automata_only", default=False, action="store_true")

    args = parser.parse_args()
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

    try:
        fact = parse_str_fact(args.fact)
        F = Atom(fact[0], fact[1], fact[2])
        flag, name = call_automata(D, program, F)
        if flag:
            print("[Automata: True] The input dataset and program do not entail the input fact!")
        else:
            print("[Automata: False] The input dataset and program entail the input fact!")

    except:
        raise ("The input contains formatting errors!")

