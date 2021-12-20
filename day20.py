def get_surrounding(image, pos, w, h, outer_px):
    # top left
    if pos[0] != 0 and pos[1] != 0:
        yield image[pos[1] - 1][pos[0] - 1]
    else:
        yield outer_px

    # top
    if pos[1] != 0:
        yield image[pos[1] - 1][pos[0]]
    else:
        yield outer_px

    # top right
    if pos[0] != w - 1 and pos[1] != 0:
        yield image[pos[1] - 1][pos[0] + 1]
    else:
        yield outer_px

    # left
    if pos[0] != 0:
        yield image[pos[1]][pos[0] - 1]
    else:
        yield outer_px

    yield image[pos[1]][pos[0]]

    # right
    if pos[0] != w - 1:
        yield image[pos[1]][pos[0] + 1]
    else:
        yield outer_px

    # bottom left
    if pos[0] != 0 and pos[1] != h - 1:
        yield image[pos[1] + 1][pos[0] - 1]
    else:
        yield outer_px

    # bottom
    if pos[1] != h - 1:
        yield image[pos[1] + 1][pos[0]]
    else:
        yield outer_px

    # bottom right
    if pos[0] != w - 1 and pos[1] != h - 1:
        yield image[pos[1] + 1][pos[0] + 1]
    else:
        yield outer_px


def enhance(image, outer_px, algorithm):
    w = len(image[0])
    h = len(image)
    new_image = []
    for y, row in enumerate(image):
        new_row = []
        for x, col in enumerate(row):
            binstr = "".join(get_surrounding(image, (x, y), w, h, outer_px)).replace(".", "0").replace("#", "1")
            idx = int(binstr, 2)
            char = algorithm[idx]
            new_row.append(char)
        new_image.append(new_row)
    if outer_px == ".":
        new_outer_px = algorithm[0]
    else:
        new_outer_px = algorithm[0b111111111]
    return new_image, new_outer_px


def print_img(image):
    for row in image:
        for cell in row:
            print(cell, end='')
        print()


def pad_image(image, margin):
    # quick and dirty fix
    w = len(image[0]) + margin * 2
    new_image = []
    for _ in range(margin):
        new_image.append(["." for i in range(w)])
    for row in image:
        new_image.append(
            ["." for i in range(margin)]
            + list(row)
            + ["." for i in range(margin)]
        )
    for _ in range(margin):
        new_image.append(["." for i in range(w)])
    return new_image


def count_lit(image):
    count = 0
    for row in image:
        for cell in row:
            if cell == "#":
                count += 1
    return count



image = []
with open("day20.in") as f:
    algorithm = f.readline().strip()
    f.readline()
    for line in f:
        image.append(line.strip())


image = pad_image(image, 100)


img2 = image
outer_px = "."
for i in range(2):
    img2, outer_px = enhance(img2, outer_px, algorithm)
    #print_img(img2)
print(count_lit(img2))


# pt2

img2 = image
outer_px = "."
for i in range(50):
    img2, outer_px = enhance(img2, outer_px, algorithm)
print(count_lit(img2))
