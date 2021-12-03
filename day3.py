with open("day3.in") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

line_length = len(lines[0])

gamma = ""
epsilon = ""
for i in range(line_length):
    bits = [line[i] for line in lines]
    if bits.count("0") > bits.count("1"):
        gamma += "0"
        epsilon += "1"
    else:
        gamma += "1"
        epsilon += "0"

print(int(gamma, 2) * int(epsilon, 2))


# pt2

oxy_rating = ""
lines_elim = lines[:]
for i in range(line_length):
    bits = [line[i] for line in lines_elim]
    next_lines = []
    if bits.count("0") > bits.count("1"):
        for line in lines_elim:
            if line[i] == "0":
                next_lines.append(line)
    else:
        for line in lines_elim:
            if line[i] == "1":
                next_lines.append(line)
    lines_elim = next_lines
    if len(lines_elim) == 1:
        oxy_rating = lines_elim[0]
        break

lines_elim = lines[:]
for i in range(line_length):
    bits = [line[i] for line in lines_elim]
    next_lines = []
    if bits.count("0") <= bits.count("1"):
        for line in lines_elim:
            if line[i] == "0":
                next_lines.append(line)
    else:
        for line in lines_elim:
            if line[i] == "1":
                next_lines.append(line)
    lines_elim = next_lines
    if len(lines_elim) == 1:
        co2_rating = lines_elim[0]
        break

print(int(oxy_rating, 2) * int(co2_rating, 2))
