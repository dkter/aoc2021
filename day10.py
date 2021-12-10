from collections import deque
from statistics import median

with open("day10.in") as f:
    lines = f.readlines()


score = 0

incomplete_lines = []
completion_scores = []
for line in lines:
    stack = deque()
    for ch in line:
        if ch in ("(", "[", "{", "<"):
            stack.append(ch)
        elif ch == ")":
            popped = stack.pop()
            if popped != "(":
                score += 3
                break
        elif ch == "]":
            popped = stack.pop()
            if popped != "[":
                score += 57
                break
        elif ch == "}":
            popped = stack.pop()
            if popped != "{":
                score += 1197
                break
        elif ch == ">":
            popped = stack.pop()
            if popped != "<":
                score += 25137
                break
    else:
        incomplete_lines.append(line)
        completion_score = 0
        stack.reverse()
        for ch in stack:
            completion_score *= 5
            if ch == "(": completion_score += 1
            elif ch == "[": completion_score += 2
            elif ch == "{": completion_score += 3
            elif ch == "<": completion_score += 4
        completion_scores.append(completion_score)

print(score)
print(median(completion_scores))
