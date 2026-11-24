import time
import tracemalloc

def ukur_algoritma(fungsi, maze, jumlah_ulang=5):
    """Mengukur waktu dan memori algoritma."""

    total_detik = 0.0

    # Mengukur waktu eksekusi
    for _ in range(jumlah_ulang):
        mulai = time.perf_counter()
        fungsi(maze)
        selesai = time.perf_counter()

        total_detik += selesai - mulai

    rata_ms = (total_detik / jumlah_ulang) * 1000.0

    # Mengukur penggunaan memori secara terpisah
    tracemalloc.start()
    fungsi(maze)
    _, puncak_byte = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Mengambil hasil algoritma beserta riwayat frontier
    hasil = fungsi(maze, rekam=True)

    jalur = hasil["jalur"]
    dikunjungi = hasil["dikunjungi"]
    riwayat_frontier = hasil["riwayat_frontier"]

    panjang_jalur = len(jalur) - 1 if jalur else 0

    return {
        "jalur": jalur,
        "dikunjungi": dikunjungi,
        "riwayat_frontier": riwayat_frontier,
        "panjang_jalur": panjang_jalur,
        "jumlah_dikunjungi": len(dikunjungi),
        "waktu_ms": rata_ms,
        "biaya_jalur": hasil["biaya"],
        "frontier_maks": hasil["frontier_maks"],
        "memori_kb": puncak_byte / 1024.0,
    }