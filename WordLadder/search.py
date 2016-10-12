from collections import deque


def search(root, success, children):
    agenda = deque([[root]])
    while agenda:
        path = agenda.popleft()
        if success(path):
            return path
        seen = set(path)
        for c in children(path):
            if c not in seen:
                agenda.append(path + [c])
    return None
