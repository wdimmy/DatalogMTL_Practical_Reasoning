import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--index", type=str, default="E")
args = parser.parse_args()
#os.rename("rules.meteor", "itemporal_program_{}".format(args.index))



template = "{}({})@[{},{}]\n"
results = []
for data in os.listdir("./"):
    if data.endswith("csv"):
        predicate = data.split("_")[1]
        with open(data) as file:
            for i, line in enumerate(file):
                if i == 0:
                    continue
                atoms = line.split(",")[:-2]
                atoms = [str(int(float(item))) for item in atoms]
                timepoints = [i for i in range(100)]
                for _ in range(20):
                    times = random.sample(timepoints, 2)
                    if times[0] > times[1]:
                        a, b = times[1], times[0]
                    else:
                        a, b = times[0], times[1]
                    fact = template.format(predicate, ",".join(atoms), a, b)
                    results.append(fact)
                # timepoints = [i for i in range(100, 200)]
                # for _ in range(80):
                #     times = random.sample(timepoints, 2)
                #     if times[0] > times[1]:
                #         a, b = times[1], times[0]
                #     else:
                #         a, b = times[0], times[1]
                #     fact = template.format(predicate, ",".join(atoms), a, b)
                #     results.append(fact)
                # timepoints = [i for i in range(200, 300)]
                # for _ in range(40):
                #     times = random.sample(timepoints, 2)
                #     if times[0] > times[1]:
                #         a, b = times[1], times[0]
                #     else:
                #         a, b = times[0], times[1]
                #     fact = template.format(predicate, ",".join(atoms), a, b)
                #     results.append(fact)

random.shuffle(results)
print(len(results))
for number in [1000000]:
    with open("../datasets/fig3/itemporal_{}_data_{}".format(args.index, number), "w") as file:
        file.writelines(results[:number])

# clear the files
for data in os.listdir("./"):
    if data.endswith("csv"):
        os.remove(data)
os.remove("rules.vada")






