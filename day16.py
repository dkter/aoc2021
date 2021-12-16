from dataclasses import dataclass
from enum import Enum
from typing import Union
import operator
from functools import reduce


version_sum = 0


class OpType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    GT = 5
    LT = 6
    EQ = 7


@dataclass
class Operator:
    optype: OpType
    subpackets: list["Packet"]


@dataclass
class Packet:
    last_index: int
    version: int
    content: Union[int, Operator]


def parse_literal(binstr):
    bits = []
    last = False
    for index, bit in enumerate(binstr):
        if index % 5 == 0:
            if last:
                #print(f"LAST index {index} for {binstr}")
                break
            if bit == "0":
                last = True
        else:
            bits.append(bit)
    else:
        index += 1
    return 6 + index, int("".join(bits), 2)


def parse_operator(typeid, binstr):
    #print(binstr)
    length_type_id = binstr[0]
    if length_type_id == "0":
        length = int(binstr[1:16], 2)
        subpacket_substr = binstr[16:16+length]
        subpackets = []
        while True:
            packet = parse_packet(subpacket_substr)
            subpackets.append(packet)
            #print(packet)
            subpacket_substr = subpacket_substr[packet.last_index:]
            if not subpacket_substr.strip("0"):
                break
        return 6 + 16 + length, subpackets
    elif length_type_id == "1":
        num_subpackets = int(binstr[1:12], 2)
        #print(num_subpackets)
        subpacket_substr = binstr[12:]
        subpackets = []
        for i in range(num_subpackets):
            packet = parse_packet(subpacket_substr)
            subpackets.append(packet)
            #print(packet)
            subpacket_substr = subpacket_substr[packet.last_index:]
        return 6 + len(binstr) - len(subpacket_substr), subpackets


def parse_packet(binstr):
    global version_sum  # fuck it
    version = int(binstr[:3], 2)
    version_sum += version
    typeid = int(binstr[3:6], 2)
    #print(binstr, version, typeid)
    if typeid == 4:
        # literal
        last_index, literal = parse_literal(binstr[6:])
        return Packet(last_index, version, literal)
    else:
        last_index, subpackets = parse_operator(typeid, binstr[6:])
        op = Operator(OpType(typeid), subpackets)
        return Packet(last_index, version, op)


with open("day16.in") as f:
    hexstr = f.readline().strip()


num = int(hexstr, 16)
binstr = ''.join([
    format(int(ch, 16), "04b")
    for ch in hexstr
])
#print(binstr)
base_packet = parse_packet(binstr)
print(base_packet)
print(version_sum)



# part 2
# small enough that recursion is ok here i think

def sum_(*nums):
    return sum(nums)

def prod(*nums):
    return reduce(operator.mul, nums, 1)

def min_(*nums):
    return min(nums)

def max_(*nums):
    return max(nums)

funcs = {
    OpType.SUM: sum_,
    OpType.PRODUCT: prod,
    OpType.MINIMUM: min_,
    OpType.MAXIMUM: max_,
    OpType.GT: operator.gt,
    OpType.LT: operator.lt,
    OpType.EQ: operator.eq,
}

def eval_packet(packet):
    if isinstance(packet.content, int):
        return packet.content
    else:
        args = [eval_packet(p) for p in packet.content.subpackets]
        return funcs[packet.content.optype](*args)

print(eval_packet(base_packet))
