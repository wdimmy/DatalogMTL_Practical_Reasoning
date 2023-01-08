import random
import os

for filename in os.listdir("../datasets/fig2"):
    with open("../datasets/fig2/"+filename) as file:
        results = file.readlines()
        facts = random.sample(results, 10)

        targets = []
        template = "{}@[{},{}]\n"
        for fact in facts:
            if random.choice([0,  1]) == 1:
                atom = fact.split("@")[0]
                left, right = fact.split("@")[1][1:-2].split(",")
                a, b = random.sample([item for item in range(int(left), int(right)+1)], 2)
                if a > b:
                    a, b = b, a
                targets.append(template.format(atom, a, b))
            else:
                atom = fact.split("@")[0]
                a, b = random.sample([-1, -2, -3, -4], 2)
                if a > b:
                    a, b = b, a
                targets.append(template.format(atom, a, b))
    with open("fig2/"+filename+".txt", "w") as file:
        file.writelines(targets)






