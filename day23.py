def getval(thing):
    if thing == "A": return 1
    if thing == "B": return 10
    if thing == "C": return 100
    if thing == "D": return 1000

class MovementError(Exception):
    pass

class Burrow:
    def __init__(self, rooms, roomlen = 2):
        self.rooms = rooms
        self.roomlen = roomlen
        self.hallway = [None for _ in range(11)]
        self.moves = {"A": 0, "B": 0, "C": 0, "D": 0}

    # def move_from_hallway_to_hallway(self, startpos, endpos):
    #     for space in self.hallway[startpos+1:endpos]:
    #         if space is not None:
    #             raise MovementError(f"{space} in the way in hallway: {self.hallway}")
    #     if endpos in (2, 4, 6, 8):
    #         raise MovementError("cannot stop at room entrance")

    #     self.hallway[endpos] = self.hallway[startpos]
    #     self.hallway[startpos] = None
    #     amphipod = self.hallway[endpos]
    #     self.moves[amphipod] += abs(endpos - startpos)
    #     print(amphipod, abs(endpos - startpos))
    #     return (abs(endpos - startpos)) * getval(self.hallway[endpos])

    def move_from_room_to_hallway(self, room, pos, continuing=False):
        roomlen = len(self.rooms[room])
        if room == 0:
            roomexit = 2
        elif room == 1:
            roomexit = 4
        elif room == 2:
            roomexit = 6
        elif room == 3:
            roomexit = 8

        for space in self.hallway[roomexit+1:pos]:
            if space is not None:
                raise MovementError(f"{space} in the way in hallway: {self.hallway}")
        if not continuing and pos in (2, 4, 6, 8):
            raise MovementError("cannot stop at room entrance")

        amphipod = self.rooms[room].pop(0)
        self.hallway[pos] = amphipod
        self.moves[amphipod] += (self.roomlen + 1 - roomlen) + abs(roomexit - pos)
        print(amphipod, (self.roomlen + 1 - roomlen) + abs(roomexit - pos))
        return ((self.roomlen + 1 - roomlen) + abs(roomexit - pos)) * getval(amphipod)

    def move_from_hallway_to_room(self, pos, room):
        roomlen = len(self.rooms[room])
        amphipod = self.hallway[pos]
        if room == 0:
            roomentrance = 2
        elif room == 1:
            roomentrance = 4
        elif room == 2:
            roomentrance = 6
        elif room == 3:
            roomentrance = 8

        for space in self.hallway[pos+1:roomentrance]:
            if space is not None:
                raise MovementError(f"{space} in the way in hallway: {self.hallway}")
        if roomlen == self.roomlen:
            raise MovementError("Room is full")
        if "ABCD"[room] != amphipod:
            raise MovementError("Cannot stop at this room")
        for thing in self.rooms[room]:
            if thing != amphipod:
                raise MovementError("Invalid items in room to stop in")

        self.rooms[room].insert(0, amphipod)
        self.hallway[pos] = None
        self.moves[amphipod] += (self.roomlen - roomlen) + abs(roomentrance - pos)
        print(amphipod, (self.roomlen - roomlen) + abs(roomentrance - pos))
        return ((self.roomlen - roomlen) + abs(roomentrance - pos)) * getval(amphipod)

    def move_from_room_to_room(self, room1, room2):
        if room2 == 0:
            room2entrance = 2
        elif room2 == 1:
            room2entrance = 4
        elif room2 == 2:
            room2entrance = 6
        elif room2 == 3:
            room2entrance = 8
        return (
            self.move_from_room_to_hallway(room1, room2entrance, continuing=True)
            + self.move_from_hallway_to_room(room2entrance, room2)
        )



with open("day23.in") as f:
    f.readline()
    f.readline()
    line1 = f.readline().strip().strip("#").split("#")
    line2 = f.readline().strip().strip("#").split("#")


other_lines = [
    ["D", "C", "B", "A"],
    ["D", "B", "A", "C"],
]
rooms = [list(i) for i in zip(line1, line2)]
rooms2 = [list(i) for i in zip(line1, *other_lines, line2)]
print(rooms)


b = Burrow(rooms)
energy = 0
# energy += b.move_from_room_to_hallway(3, 9)
# print(energy)
# energy += b.move_from_room_to_room(1, 3)
# print(energy)
# energy += b.move_from_room_to_hallway(0, 1)
# print(energy)
# energy += b.move_from_room_to_room(0, 1)
# print(energy)

# energy += b.move_from_room_to_hallway(0, 0)
# print(energy)
# energy += b.move_from_room_to_hallway(3, 1)
# print(energy)
# energy += b.move_from_room_to_hallway(3, 9)
# print(energy)
# energy += b.move_from_room_to_room(0, 3)
# print(energy)
# energy += b.move_from_hallway_to_room(1, 0)
# print(energy)
# energy += b.move_from_hallway_to_room(0, 0)
# print(energy)
# energy += b.move_from_room_to_hallway(2, 1)
# print(energy)
# energy += b.move_from_room_to_hallway(2, 3)
# print(energy)
# energy += b.move_from_hallway_to_room(9, 2)
# print(energy)
# energy += b.move_from_room_to_room(1, 2)
# print(energy)
# energy += b.move_from_room_to_room(1, 3)
# print(energy)
# energy += b.move_from_hallway_to_room(3, 1)
# print(energy)
# energy += b.move_from_hallway_to_room(1, 1)
# print(energy)
# print(b.hallway)
# print(b.rooms)


energy += b.move_from_room_to_hallway(0, 1)
print(energy)
energy += b.move_from_room_to_hallway(3, 10)
print(energy)
energy += b.move_from_room_to_hallway(2, 3)
print(energy)
energy += b.move_from_room_to_hallway(2, 9)
print(energy)
energy += b.move_from_room_to_room(1, 2)
print(energy)
energy += b.move_from_room_to_room(3, 2)
print(energy)
energy += b.move_from_room_to_room(1, 3)
print(energy)
print(b.rooms)
print(b.hallway)
energy += b.move_from_hallway_to_room(3, 1)
print(energy)
energy += b.move_from_room_to_room(0, 3)
print(energy)
energy += b.move_from_hallway_to_room(9, 1)
print(energy)
energy += b.move_from_hallway_to_room(1, 0)
print(energy)
energy += b.move_from_hallway_to_room(10, 0)

print(energy)
print(b.rooms)
print(b.moves)

# this is wrong. i just stared at it a bit and decided i need to subtract 2


# pt 2

b2 = Burrow(rooms2, 4)
energy = 0

# energy += b2.move_from_room_to_hallway(1, 0)
# energy += b2.move_from_room_to_hallway(1, 1)
# energy += b2.move_from_room_to_hallway(1, 3)
# energy += b2.move_from_room_to_hallway(1, 9)

# energy += b2.move_from_hallway_to_room(3, 1)
# energy += b2.move_from_room_to_room(2, 1)
# energy += b2.move_from_room_to_room(2, 1)

# energy += b2.move_from_room_to_hallway(2, 7)
# energy += b2.move_from_room_to_room(2, 1)

# energy += b2.move_from_hallway_to_room(1, 2)
# energy += b2.move_from_hallway_to_room(0, 2)

# energy += b2.move_from_hallway_to_hallway(7, 0)
# energy += b2.move_from_room_to_hallway(3, 1)
# energy += b2.move_from_room_to_hallway(3, 3)

# energy += b2.move_from_room_to_room(3, 2)
# energy += b2.move_from_room_to_room(3, 2)

# energy += b2.move_from_hallway_to_room(9, 3)

# energy += b2.move_from_hallway_to_hallway(3, 10)
# energy += b2.move_from_room_to_hallway(0, 9)

# energy += b2.move_from_room_to_room(0, 3)
# energy += b2.move_from_room_to_room(0, 3)
# energy += b2.move_from_room_to_room(0, 3)

# energy += b2.move_from_hallway_to_room(0, 0)
# energy += b2.move_from_hallway_to_room(1, 0)
# energy += b2.move_from_hallway_to_room(9, 0)
# energy += b2.move_from_hallway_to_room(10, 0)

# print(energy)
# print(b2.rooms)
# print(b2.moves)

# 51549: wrong


# energy += b2.move_from_room_to_hallway(2, 0)
# energy += b2.move_from_room_to_hallway(2, 1)
# energy += b2.move_from_room_to_hallway(2, 9)
# energy += b2.move_from_room_to_hallway(2, 7)

# energy += b2.move_from_room_to_room(1, 2)
# energy += b2.move_from_room_to_room(1, 2)

# energy += b2.move_from_room_to_hallway(1, 3)
# energy += b2.move_from_room_to_hallway(1, 5)

# energy += b2.move_from_hallway_to_room(3, 1)
# energy += b2.move_from_hallway_to_room(1, 1)
# energy += b2.move_from_hallway_to_room(0, 1)

# energy += b2.move_from_hallway_to_room(7, 2)
# energy += b2.move_from_hallway_to_room(9, 2)

# energy += b2.move_from_hallway_to_hallway(5, 9)

# energy += b2.move_from_room_to_hallway(2, 0)
# energy += b2.move_from_room_to_room(2, 1)

# --

# energy += b2.move_from_room_to_hallway(0, 0)
# energy += b2.move_from_room_to_room(2, 0)
# energy += b2.move_from_room_to_hallway(2, 1)
# energy += b2.move_from_room_to_hallway(2, 7)
# energy += b2.move_from_room_to_hallway(2, 3)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_room_to_room(1, 2)
# energy += b2.move_from_room_to_room(1, 2)
# energy += b2.move_from_hallway_to_room(7, 2)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_room_to_room(1, 2)
# energy += b2.move_from_room_to_hallway(1, 9)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_hallway_to_room(3, 1)
# energy += b2.move_from_hallway_to_room(1, 1)
# energy += b2.move_from_room_to_room(0, 1)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_room_to_room(2, 1)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_room_to_hallway(2, 1)

# print(b2.rooms, b2.hallway)

# energy += b2.move_from_room_to_hallway(3, 3)
# energy += b2.move_from_room_to_hallway(3, 5)
# energy += b2.move_from_room_to_room(3, 2)
# energy += b2.move_from_room_to_room(3, 2)

# energy += b2.move_from_hallway_to_room(9, 3)

# energy += b2.move_from_hallway_to_hallway(5, 10)
# energy += b2.move_from_hallway_to_hallway(3, 9)
# #energy += b2.move_from_room_to_hallway(0, 1)

# energy += b2.move_from_room_to_room(0, 3)
# energy += b2.move_from_room_to_room(0, 3)
# energy += b2.move_from_room_to_room(0, 3)

# energy += b2.move_from_hallway_to_room(1, 0)
# energy += b2.move_from_hallway_to_room(0, 0)
# energy += b2.move_from_hallway_to_room(9, 0)
# energy += b2.move_from_hallway_to_room(10, 0)

# print(energy)
# print(b2.rooms)
# print(b2.moves)

# 50355: wrong   // {'A': 75, 'B': 48, 'C': 28, 'D': 47}
# 50353: wrong   // {'A': 73, 'B': 48, 'C': 28, 'D': 47}
# 50349: wrong   // {'A': 69, 'B': 48, 'C': 28, 'D': 47}
# 50347: wrong   // {'A': 67, 'B': 48, 'C': 28, 'D': 47}
# 50327: wrong   // {'A': 67, 'B': 46, 'C': 28, 'D': 47}
# min: {A: 35, B: 28, C: 28, D: 45 (realistically 47)}


energy += b2.move_from_room_to_hallway(1, 0)
energy += b2.move_from_room_to_hallway(1, 1)
energy += b2.move_from_room_to_hallway(1, 3)
energy += b2.move_from_room_to_hallway(1, 9)

energy += b2.move_from_hallway_to_room(3, 1)
energy += b2.move_from_room_to_room(2, 1)
energy += b2.move_from_room_to_room(2, 1)

energy += b2.move_from_room_to_hallway(2, 7)
energy += b2.move_from_room_to_room(2, 1)

energy += b2.move_from_hallway_to_room(1, 2)
energy += b2.move_from_hallway_to_room(0, 2)

energy += b2.move_from_hallway_to_hallway(7, 0)
energy += b2.move_from_room_to_hallway(3, 1)
energy += b2.move_from_room_to_hallway(3, 3)

energy += b2.move_from_room_to_room(3, 2)
energy += b2.move_from_room_to_room(3, 2)

energy += b2.move_from_hallway_to_room(9, 3)

energy += b2.move_from_hallway_to_hallway(3, 10)
energy += b2.move_from_room_to_hallway(0, 9)

energy += b2.move_from_room_to_room(0, 3)
energy += b2.move_from_room_to_room(0, 3)
energy += b2.move_from_room_to_room(0, 3)

energy += b2.move_from_hallway_to_room(0, 0)
energy += b2.move_from_hallway_to_room(1, 0)
energy += b2.move_from_hallway_to_room(9, 0)
energy += b2.move_from_hallway_to_room(10, 0)

# this is all wrong, because I didn't read the last two bullet points in the problem statement
# see day23_auto.py
