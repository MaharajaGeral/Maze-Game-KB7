
import sys
import pygame

from Maze.maze import baca_maze
from Algorithms.bfs import bfs
from Algorithms.dfs import dfs
from Visual.visualizer import (hitung_tata_letak, gambar_maze,
                               gambar_panel_samping, WARNA_LATAR)


def animasikan(maze, hasil, nama_algoritma, judul):
    pygame.init()
    tata = hitung_tata_letak(maze)
    layar = pygame.display.set_mode((tata["lebar_jendela"], tata["tinggi_jendela"]))
    pygame.display.set_caption("Animasi " + nama_algoritma)
    jam = pygame.time.Clock()

    dikunjungi = hasil["dikunjungi"]
    jalur = hasil["jalur"]
    riwayat = hasil["riwayat_frontier"]

    jumlah_tampil = 0    # berapa sel dikunjungi yang sudah digambar
    kecepatan = 1        # sel yang ditambah per frame
    selesai = False

    jalan = True
    while jalan:
        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                jalan = False
            elif kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_ESCAPE:
                    jalan = False
                elif kejadian.key == pygame.K_UP:
                    kecepatan += 1
                elif kejadian.key == pygame.K_DOWN and kecepatan > 1:
                    kecepatan -= 1
                elif kejadian.key == pygame.K_r:   # ulangi animasi
                    jumlah_tampil = 0
                    selesai = False

        # tambah sel yang digambar
        if not selesai:
            jumlah_tampil += kecepatan
            if jumlah_tampil >= len(dikunjungi):
                jumlah_tampil = len(dikunjungi)
                selesai = True

        # jalur baru muncul kalau semua sel sudah selesai digambar
        if selesai:
            jalur_tampil = jalur
        else:
            jalur_tampil = []

        info = ["Algoritma: " + nama_algoritma,
                "Dikunjungi: %d" % jumlah_tampil,
                "Kecepatan: %d (atas/bawah)" % kecepatan]
        if selesai:
            info.append("Panjang jalur: %d" % (len(jalur) - 1))
            info.append("Tekan R untuk ulang")

        frontier = riwayat[jumlah_tampil - 1] if jumlah_tampil > 0 else [maze.start]

        layar.fill(WARNA_LATAR)
        gambar_maze(layar, maze, tata["maze_x"], tata["maze_y"], tata["ukuran_sel"],
                    frontier=frontier, dieksplorasi=dikunjungi[:jumlah_tampil],
                    jalur=jalur_tampil)
        gambar_panel_samping(layar, tata["panel_x"], tata["panel_y"],
                             maze, judul, info)
        pygame.display.flip()
        jam.tick(30)

    pygame.quit()


if __name__ == "__main__":
    nama_file = sys.argv[1] if len(sys.argv) > 1 else "Maze/data/small_1.txt"
    algoritma = sys.argv[2].lower() if len(sys.argv) > 2 else "bfs"

    maze = baca_maze(nama_file)

    if algoritma == "dfs":
        hasil = dfs(maze, rekam=True)
    else:
        hasil = bfs(maze, rekam=True)

    animasikan(
        maze,
        hasil,
        algoritma.upper(),
        nama_file.split("/")[-1]
    )