def search(root, success, children):
    agenda = [ [ root ] ]
    while agenda:
        path = agenda.pop(0)
        if success(path):
            return path
        seen = set(path)
        for c in children(path):
            if c not in seen:
                agenda.append(path + [c])
    return None
