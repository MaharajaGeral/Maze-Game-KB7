def dfs(maze):
    stack = [maze.start]
    parent = {maze.start: None}
    dikunjungi = []

    while stack:
        sekarang = stack.pop()

        if sekarang in dikunjungi:
            continue
        dikunjungi.append(sekarang)

        if sekarang == maze.finish:
            break

        for t in reversed(maze.tetangga(sekarang)):
            if t not in dikunjungi:
                if t not in parent:
                    parent[t] = sekarang
                stack.append(t)

    jalur = []
    if maze.finish in dikunjungi:
        sel = maze.finish
        while sel is not None:
            jalur.append(sel)
            sel = parent[sel]
        jalur.reverse()

    return {"jalur": jalur, "dikunjungi": dikunjungi}