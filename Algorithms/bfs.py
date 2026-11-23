from collections import deque

def bfs(maze, rekam=False):
    queue = deque([maze.start])

    parent = {maze.start: None}
    dikunjungi = []
    sudah = set()

    riwayat_frontier = []
    frontier_maks = len(queue)

    while queue:
        sekarang = queue.popleft()

        if sekarang in sudah:
            continue

        sudah.add(sekarang)
        dikunjungi.append(sekarang)

        if sekarang == maze.finish:
            if rekam:
                riwayat_frontier.append(list(queue))
            break

        for t in maze.tetangga(sekarang):
            if t not in parent:
                parent[t] = sekarang
                queue.append(t)

        frontier_maks = max(frontier_maks, len(queue))

        if rekam:
            riwayat_frontier.append(list(queue))

    jalur = []

    if maze.finish in sudah:
        sel = maze.finish

        while sel is not None:
            jalur.append(sel)
            sel = parent[sel]

        jalur.reverse()

    return {
        "jalur": jalur,
        "dikunjungi": dikunjungi,
        "riwayat_frontier": riwayat_frontier,
        "biaya": maze.hitung_biaya_jalur(jalur) if jalur else 0,
        "frontier_maks": frontier_maks
    }