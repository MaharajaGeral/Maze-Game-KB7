from collections import deque

def bfs(maze):
    queue = deque([maze.start])
    parent = {maze.start: None}
    dikunjungi = []

    while queue:
        sekarang = queue.popleft()

        if sekarang in dikunjungi:
            continue

        dikunjungi.append(sekarang)

        if sekarang == maze.finish:
            break

        for t in maze.tetangga(sekarang):
            if t not in parent:
                parent[t] = sekarang
                queue.append(t)

    jalur = []
    if maze.finish in dikunjungi:
        sel = maze.finish

        while sel is not None:
            jalur.append(sel)
            sel = parent[sel]

        jalur.reverse()
    return {
        "jalur": jalur,
        "dikunjungi": dikunjungi
    }