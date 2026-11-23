def dfs(maze):
    stack = [maze.start]
    parent = {maze.start: None}
    dikunjungi = []          # urutan kunjungan (dipakai animasi)
    sudah = set()            # untuk cek cepat
    frontier_maks = len(stack)

    while stack:
        sekarang = stack.pop()

        if sekarang in sudah:
            continue
        sudah.add(sekarang)
        dikunjungi.append(sekarang)

        if sekarang == maze.finish:
            break

        for t in reversed(maze.tetangga(sekarang)):
            if t not in sudah:
                if t not in parent:
                    parent[t] = sekarang
                stack.append(t)

        frontier_maks = max(frontier_maks, len(stack))

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
        "biaya": maze.hitung_biaya_jalur(jalur) if jalur else 0,
        "frontier_maks": frontier_maks,
    }