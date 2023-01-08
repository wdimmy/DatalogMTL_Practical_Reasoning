import os

for folder in ["fig1", "fig2", "fig3"]:
    for filename in os.listdir(folder):
        results = []
        with open(os.path.join(folder, filename)) as file:
            for line in file:
                fact = line.replace("()", "")
                results.append(fact)
        with open("../datasets/{}/{}".format(folder, filename), "w") as file:
            file.writelines(results)




