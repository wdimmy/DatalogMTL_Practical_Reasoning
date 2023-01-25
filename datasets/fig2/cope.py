import random

writer = open("itemporal_H_data_100000", "w")

lines = []
with open("itemporal_H_data_1000000") as file:
    for line in file:
        lines.append(line)

lines = random.sample(lines, 100000)
for line in lines:
    writer.writelines(line)


