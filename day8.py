entries = []
output = []
with open("day8.in") as f:
    while True:
        try:
            # output_segs = []
            # line = next(f).strip().split(" | ")
            # print(line)
            # if len(line) == 2:
            #     output_segs = line[1].split(" ")
            # sig_pattern_segs = line[0]
            # output_segs.extend(next(f).strip().split(" "))
            line = next(f).strip().split(" | ")
            output_segs = line[1].split(" ")
            output.append(output_segs)
            everything = []
            everything.extend(output_segs)
            sig_pattern_segs = line[0].split(" ")
            everything.extend(sig_pattern_segs)
            entries.append(everything)
        except StopIteration:
            break

counter = 0
for val in output:
    for segs in val:
        if len(segs) in (2, 4, 3, 7):
            counter += 1
print(counter)

# pt2

total = 0
for index, entry in enumerate(entries):
    segmap = {}
    # segmap keys should look like:
    # aaa
    # b c
    # b c
    # ddd
    # e f
    # e f
    # ggg

    charset_map = {}
    charset_map[1] = None
    charset_map[4] = None
    charset_map[7] = None
    charset_map[8] = None
    two_three_five_chars_options = set()
    six_nine_zero_chars_options = set()

    for segs in entry:
        if len(segs) == 2: # character is 1
            charset_map[1] = frozenset(segs)
        if len(segs) == 4: # character is 4
            charset_map[4] = frozenset(segs)
        if len(segs) == 3: # character is 7
            charset_map[7] = frozenset(segs)
        if len(segs) == 7: # character is 8
            charset_map[8] = frozenset(segs)
        if len(segs) == 5: # character is 2, 3 or 5
            two_three_five_chars_options.add(frozenset(segs))
        if len(segs) == 6: # character is 6 or 9 (or 0 almost forgot abt this)
            six_nine_zero_chars_options.add(frozenset(segs))

    # 7 - 1 is segment a
    segmap["a"] = next(iter(charset_map[7] - charset_map[1]))

    # nums with a: 2, 3, 5, 6, 7, 8, 9
    # 1 : 2
    # 2 : 5
    # 3 : 5
    # 4 : 4
    # 5 : 5
    # 6 : 6
    # 7 : 3
    # 8 : 7
    # 9 : 6

    # can tell 6 from 9 by comparing with the segments from 1
    charset_map[6] = None
    charset_map[9] = None
    for option in six_nine_zero_chars_options:
        if len(option - charset_map[1]) != 6 - 2:
            charset_map[6] = option
            six_nine_zero_chars_options.remove(option)
            break

    # can tell 5 by comparing with 6 (or 9)
    charset_map[5] = None
    for option in two_three_five_chars_options:
        if len(charset_map[6] - option) == 6 - 5:
            charset_map[5] = option
            two_three_five_chars_options.remove(option)
            break

    # can tell 2 from 3 by comparing with 1
    charset_map[2] = None
    charset_map[3] = None
    for option in two_three_five_chars_options:
        if len(option - charset_map[1]) == 3:
            charset_map[3] = option
        else:
            assert len(option - charset_map[1]) == 4
            charset_map[2] = option

    # can tell 0 from 9 by comparing with 5
    charset_map[0] = None
    for option in six_nine_zero_chars_options:
        if len(option - charset_map[5]) == 1:
            charset_map[9] = option
        else:
            charset_map[0] = option

    # pretty sure i don't even need to decode the segments now
    output_num = ""
    for num_seg in output[index]:
        for num, segs in charset_map.items():
            if frozenset(num_seg) == segs:
                output_num += str(num)
                break
    total += int(output_num)
print(total)
