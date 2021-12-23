from copy import deepcopy
from queue import PriorityQueue
from pprint import pprint

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
        self.hallway = tuple(None for _ in range(11))
        self.moves = {"A": 0, "B": 0, "C": 0, "D": 0}
        #self.last_hallway_move = None

    def __hash__(self):
        return hash((hash(self.rooms), hash(self.hallway)))

    def __eq__(self, other):
        return (
            self.rooms == other.rooms
            and self.hallway == other.hallway
        )

    # def move_from_hallway_to_hallway(self, startpos, endpos):
    #     for space in self.hallway[startpos+1:endpos]:
    #         if space is not None:
    #             raise MovementError(f"{space} in the way in hallway: {self.hallway}")
    #     if endpos in (2, 4, 6, 8):
    #         raise MovementError("cannot stop at room entrance")

    #     amphipod = self.hallway[startpos]
    #     list_hallway = list(self.hallway)
    #     list_hallway[endpos] = amphipod
    #     list_hallway[startpos] = None
    #     new_burrow = Burrow(self.rooms, self.roomlen)
    #     new_burrow.hallway = tuple(list_hallway)
    #     new_burrow.moves = self.moves.copy()
    #     new_burrow.moves[amphipod] += abs(endpos - startpos)
    #     new_burrow.last_hallway_move = endpos
    #     #print(amphipod, abs(endpos - startpos))
    #     return new_burrow

    def move_from_room_to_hallway(self, room, pos, continuing=False):
        roomlen = len(self.rooms[room])
        amphipod = self.rooms[room][0]
        if room == 0:
            roomexit = 2
        elif room == 1:
            roomexit = 4
        elif room == 2:
            roomexit = 6
        elif room == 3:
            roomexit = 8

        if pos > roomexit:
            for space in self.hallway[roomexit+1:pos+1]:
                if space is not None:
                    raise MovementError(f"{space} in the way in hallway: {self.hallway}")
        else:
            for space in self.hallway[pos:roomexit]:
                if space is not None:
                    raise MovementError(f"{space} in the way in hallway: {self.hallway}")
        if not continuing and pos in (2, 4, 6, 8):
            raise MovementError("cannot stop at room entrance")

        new_room = self.rooms[room][1:]
        new_rooms = self.rooms[:room] + (new_room,) + self.rooms[room+1:]
        list_hallway = list(self.hallway)
        list_hallway[pos] = amphipod
        new_burrow = Burrow(new_rooms, self.roomlen)
        new_burrow.hallway = tuple(list_hallway)
        new_burrow.moves = self.moves.copy()
        new_burrow.moves[amphipod] += (self.roomlen + 1 - roomlen) + abs(roomexit - pos)
        #new_burrow.last_hallway_move = pos
        #print(amphipod, (self.roomlen + 1 - roomlen) + abs(roomexit - pos))
        return new_burrow

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

        if pos > roomentrance:
            for space in self.hallway[roomentrance+1:pos]:
                if space is not None:
                    raise MovementError(f"{space} in the way in hallway: {self.hallway}")
        else:
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

        new_room = (amphipod,) + self.rooms[room]
        list_hallway = list(self.hallway)
        list_hallway[pos] = None
        new_rooms = self.rooms[:room] + (new_room,) + self.rooms[room+1:]
        new_burrow = Burrow(new_rooms, self.roomlen)
        new_burrow.hallway = tuple(list_hallway)
        new_burrow.moves = self.moves.copy()
        new_burrow.moves[amphipod] += (self.roomlen - roomlen) + abs(roomentrance - pos)
        #new_burrow.last_hallway_move = None
        #print(amphipod, (self.roomlen - roomlen) + abs(roomentrance - pos))
        return new_burrow

    def move_from_room_to_room(self, room1, room2):
        if room2 == 0:
            room2entrance = 2
        elif room2 == 1:
            room2entrance = 4
        elif room2 == 2:
            room2entrance = 6
        elif room2 == 3:
            room2entrance = 8

        new_burrow_1 = self.move_from_room_to_hallway(room1, room2entrance, continuing=True)
        new_burrow_2 = new_burrow_1.move_from_hallway_to_room(room2entrance, room2)
        return new_burrow_2


    def count_correct(self):
        count = 0
        for room, ch in zip(self.rooms, "ABCD"):
            for ch2 in reversed(room):
                if ch2 == ch:
                    count += 1
                else:
                    break
        return count


    def __lt__(self, other):
        return True
        return self.count_correct() < other.count_correct()


    def __repr__(self):
        return str(self)
        return f"Burrow(rooms={self.rooms}, hallway={self.hallway}, hash={hash(self)})"


    def __str__(self):
        s = "#############\n#"
        for ch in self.hallway:
            if ch is None:
                s += "."
            else:
                s += ch
        s += "#\n###"
        for i in range(self.roomlen):
            for room in self.rooms:
                #if len(room) >= self.roomlen - i - 1:
                rm = (".",) * (self.roomlen - len(room)) + room
                # try:
                #     s += room[-len(room) + i]
                #     #s += room[i - (self.roomlen - len(room))]
                # except IndexError:
                #     s += "."
                s += rm[i]
                s += "#"
            if i == 0:
                s += "##\n  #"
            elif i == self.roomlen - 1:
                s += "\n"
            else:
                s += "\n  #"
        s += "  #########"
        return s


def get_moves_from_room(burrow, room):
    for thing in reversed(burrow.rooms[room]):
        if thing != "ABCD"[room]:
            break
    else:
        # room is full, don't try to move anything out of it
        return

    for hpos in range(11):
        try:
            yield burrow.move_from_room_to_hallway(room, hpos)
        except MovementError:
            pass
    for room2 in range(4):
        if room2 != room:
            try:
                yield burrow.move_from_room_to_room(room, room2)
            except MovementError:
                pass


def get_moves_from_hallway(burrow, hpos):
    # if hpos != burrow.last_hallway_move:
    #     for hpos2 in range(11):
    #         if hpos2 != hpos:
    #             try:
    #                 yield burrow.move_from_hallway_to_hallway(hpos, hpos2)
    #             except MovementError:
    #                 pass
    for room in range(4):
        try:
            yield burrow.move_from_hallway_to_room(hpos, room)
        except MovementError:
            pass


def get_moves(burrow):
    for hpos, h in enumerate(burrow.hallway):
        if h is not None:
            yield from get_moves_from_hallway(burrow, hpos)
    for rpos, r in enumerate(burrow.rooms):
        if len(r) != 0:
            yield from get_moves_from_room(burrow, rpos)


def get_total_energy(burrow):
    return sum(
        [
            getval(char) * burrow.moves[char]
            for char in "ABCD"
        ]
    )


def is_complete(burrow):
    if (
        burrow.rooms[0] == ("A",) * burrow.roomlen
        and burrow.rooms[1] == ("B",) * burrow.roomlen
        and burrow.rooms[2] == ("C",) * burrow.roomlen
        and burrow.rooms[3] == ("D",) * burrow.roomlen
    ):
        if not all(x is None for x in burrow.hallway):
            raise ValueError("this should not happen")
        return True
    return False


def vprint(lst):
    for item in lst:
        print(item)
        print()


def get_shortest_sort(burrow):
    burrow_mincosts = {burrow: 0}
    queue = PriorityQueue()
    queue.put((0, burrow, [burrow]))
    visited = set()
    min_energy = 9999999999

    while not queue.empty():
        energy, b, steps = queue.get()
        visited.add(b)

        if is_complete(b):
            min_energy = min(min_energy, get_total_energy(b))
            #print("min_energy:", min_energy)
            #vprint(steps)
            continue

        for next_burrow in get_moves(b):
            if next_burrow not in visited:
                new_total_energy = get_total_energy(next_burrow)
                if (
                    next_burrow not in burrow_mincosts
                    or burrow_mincosts[next_burrow] > new_total_energy
                ):
                    queue.put((new_total_energy, next_burrow, steps + [next_burrow]))
                    burrow_mincosts[next_burrow] = new_total_energy

    return min_energy






with open("day23.in") as f:
    f.readline()
    f.readline()
    line1 = f.readline().strip().strip("#").split("#")
    line2 = f.readline().strip().strip("#").split("#")


other_lines = [
    ["D", "C", "B", "A"],
    ["D", "B", "A", "C"],
]
rooms = tuple(zip(line1, line2))
rooms2 = tuple(zip(line1, *other_lines, line2))

b1 = Burrow(rooms)
b2 = Burrow(rooms2, 4)
print(get_shortest_sort(b1))
print(get_shortest_sort(b2))
