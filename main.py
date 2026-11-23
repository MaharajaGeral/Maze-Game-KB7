import os
import time
import tracemalloc
import pygame

from Maze.maze import baca_maze
from Algorithms.bfs import bfs
from Algorithms.dfs import dfs
from Visual.visualizer import (
    hitung_ukuran_sel,
    hitung_tata_letak,
    gambar_maze,
    gambar_panel_samping,
    WARNA_FRONTIER,
    WARNA_DIEKSPLORASI,
    WARNA_JALUR,
    WARNA_LATAR,
    WARNA_GARIS,
    WARNA_DINDING,
    WARNA_BIAYA,
    WARNA_START,
    WARNA_FINISH,
    WARNA_DIEKSPLORASI,
    WARNA_JALUR,
    WARNA_TEKS,
)

# Lokasi folder data maze (relatif terhadap lokasi main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Maze", "data")

# Warna tambahan untuk antarmuka menu & papan statistik
WARNA_KARTU = (255, 255, 255)
WARNA_BORDER = (200, 206, 218)
WARNA_TEKS_REDUP = (95, 102, 115)
WARNA_BFS = (41, 128, 185)
WARNA_DFS = (142, 68, 173)
WARNA_AKSEN = (52, 73, 94)
WARNA_TOMBOL_HOVER = (238, 242, 248)
WARNA_MULAI = (39, 174, 96)
WARNA_MULAI_HOVER = (33, 150, 83)
WARNA_KELUAR = (231, 76, 60)
WARNA_KELUAR_HOVER = (203, 67, 53)
WARNA_PUTIH = (255, 255, 255)

DAFTAR_MODE = [
    ("bfs", "Animasi BFS"),
    ("dfs", "Animasi DFS"),
    ("bandingkan", "Bandingkan BFS vs DFS"),
]

DAFTAR_UKURAN = [
    ("small", "Kecil (10x10)"),
    ("medium", "Sedang (15x15)"),
    ("big", "Besar (20x20)"),
]

DAFTAR_MAP = [1, 2, 3, 4, 5]


def path_maze(ukuran, nomor):
    """Kembalikan path lengkap dan nama file untuk kombinasi ukuran & nomor map."""
    nama_file = f"{ukuran}_{nomor}.txt"
    return os.path.join(DATA_DIR, nama_file), nama_file


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

def frontier_saat(data, jumlah_tampil, maze):
    """Isi frontier (antre/stack) setelah `jumlah_tampil` sel dikunjungi.
    Sebelum langkah pertama, frontier hanya berisi titik start."""
    if jumlah_tampil <= 0:
        return [maze.start]
    return data["riwayat_frontier"][jumlah_tampil - 1]

def gambar_tombol(
    layar,
    rect,
    teks,
    font,
    aktif=False,
    hover=False,
    warna_aktif=WARNA_AKSEN,
    warna_normal=WARNA_KARTU,
    warna_hover=WARNA_TOMBOL_HOVER,
    warna_teks=WARNA_TEKS,
    warna_teks_aktif=WARNA_PUTIH,
):
    """Gambar tombol sederhana dengan sudut membulat."""
    if aktif:
        bg = warna_aktif
        fg = warna_teks_aktif
        border = warna_aktif
    else:
        bg = warna_hover if hover else warna_normal
        fg = warna_teks
        border = WARNA_BORDER

    pygame.draw.rect(layar, bg, rect, border_radius=8)
    pygame.draw.rect(layar, border, rect, 2 if aktif else 1, border_radius=8)

    surf_teks = font.render(teks, True, fg)
    layar.blit(surf_teks, surf_teks.get_rect(center=rect.center))


def tampilkan_menu(pilihan):
    """Halaman menu utama untuk memilih mode, ukuran maze, dan nomor map."""
    lebar, tinggi = 720, 540
    layar = pygame.display.set_mode((lebar, tinggi))
    pygame.display.set_caption("Maze Game - BFS & DFS (Menu Utama)")
    jam = pygame.time.Clock()

    font_judul = pygame.font.SysFont(None, 38)
    font_sub = pygame.font.SysFont(None, 21)
    font_label = pygame.font.SysFont(None, 24)
    font_tombol = pygame.font.SysFont(None, 22)
    font_kecil = pygame.font.SysFont(None, 20)

    # Susunan tombol pilihan
    tombol_mode = []
    for i, (kode, label) in enumerate(DAFTAR_MODE):
        rect = pygame.Rect(60 + i * 204, 136, 192, 42)
        tombol_mode.append((rect, kode, label))

    tombol_ukuran = []
    for i, (kode, label) in enumerate(DAFTAR_UKURAN):
        rect = pygame.Rect(60 + i * 204, 224, 192, 42)
        tombol_ukuran.append((rect, kode, label))

    tombol_map = []
    for i, nomor in enumerate(DAFTAR_MAP):
        rect = pygame.Rect(60 + i * 122, 312, 112, 42)
        tombol_map.append((rect, nomor, f"Map {nomor}"))

    rect_mulai = pygame.Rect(185, 452, 200, 46)
    rect_keluar = pygame.Rect(401, 452, 134, 46)

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                return "keluar"
            elif kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_ESCAPE:
                    return "keluar"
                elif kejadian.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "mulai"
            elif kejadian.type == pygame.MOUSEBUTTONDOWN and kejadian.button == 1:
                for rect, kode, _ in tombol_mode:
                    if rect.collidepoint(pos_mouse):
                        pilihan["mode"] = kode
                for rect, kode, _ in tombol_ukuran:
                    if rect.collidepoint(pos_mouse):
                        pilihan["ukuran"] = kode
                for rect, nomor, _ in tombol_map:
                    if rect.collidepoint(pos_mouse):
                        pilihan["nomor"] = nomor
                if rect_mulai.collidepoint(pos_mouse):
                    return "mulai"
                if rect_keluar.collidepoint(pos_mouse):
                    return "keluar"

        layar.fill(WARNA_LATAR)

        # Header
        judul_surf = font_judul.render("MAZE GAME - BFS & DFS", True, WARNA_TEKS)
        layar.blit(judul_surf, judul_surf.get_rect(centerx=lebar // 2, top=22))
        sub_surf = font_sub.render(
            "Visualisasi & Perbandingan Algoritma Pencarian (Kelompok KB7)",
            True,
            WARNA_TEKS_REDUP,
        )
        layar.blit(sub_surf, sub_surf.get_rect(centerx=lebar // 2, top=58))

        # Kartu utama pilihan
        kartu = pygame.Rect(36, 92, 648, 342)
        pygame.draw.rect(layar, WARNA_KARTU, kartu, border_radius=12)
        pygame.draw.rect(layar, WARNA_BORDER, kartu, 1, border_radius=12)

        # 1. Mode
        layar.blit(font_label.render("1. Pilih Mode", True, WARNA_TEKS), (60, 108))
        for rect, kode, label in tombol_mode:
            warna_aktif = WARNA_BFS if kode == "bfs" else (WARNA_DFS if kode == "dfs" else WARNA_AKSEN)
            gambar_tombol(
                layar,
                rect,
                label,
                font_tombol,
                aktif=(pilihan["mode"] == kode),
                hover=rect.collidepoint(pos_mouse),
                warna_aktif=warna_aktif,
            )

        # 2. Ukuran Maze
        layar.blit(font_label.render("2. Pilih Ukuran Maze", True, WARNA_TEKS), (60, 196))
        for rect, kode, label in tombol_ukuran:
            gambar_tombol(
                layar,
                rect,
                label,
                font_tombol,
                aktif=(pilihan["ukuran"] == kode),
                hover=rect.collidepoint(pos_mouse),
                warna_aktif=WARNA_AKSEN,
            )

        # 3. Map
        layar.blit(font_label.render("3. Pilih Peta Labirin", True, WARNA_TEKS), (60, 284))
        for rect, nomor, label in tombol_map:
            gambar_tombol(
                layar,
                rect,
                label,
                font_tombol,
                aktif=(pilihan["nomor"] == nomor),
                hover=rect.collidepoint(pos_mouse),
                warna_aktif=WARNA_AKSEN,
            )

        # Ringkasan pilihan aktif
        _, nama_file = path_maze(pilihan["ukuran"], pilihan["nomor"])
        label_mode = dict(DAFTAR_MODE)[pilihan["mode"]]
        kotak_info = pygame.Rect(60, 374, 600, 42)
        pygame.draw.rect(layar, (242, 245, 250), kotak_info, border_radius=8)
        pygame.draw.rect(layar, WARNA_BORDER, kotak_info, 1, border_radius=8)
        teks_info = f"File: Maze/data/{nama_file}   |   Mode: {label_mode}"
        surf_info = font_kecil.render(teks_info, True, WARNA_TEKS)
        layar.blit(surf_info, surf_info.get_rect(center=kotak_info.center))

        # Tombol Mulai & Keluar
        gambar_tombol(
            layar,
            rect_mulai,
            "Mulai (ENTER)",
            font_label,
            aktif=True,
            warna_aktif=WARNA_MULAI_HOVER if rect_mulai.collidepoint(pos_mouse) else WARNA_MULAI,
        )
        gambar_tombol(
            layar,
            rect_keluar,
            "Keluar (ESC)",
            font_label,
            aktif=True,
            warna_aktif=WARNA_KELUAR_HOVER if rect_keluar.collidepoint(pos_mouse) else WARNA_KELUAR,
        )

        # Petunjuk bawah
        hint = font_kecil.render(
            "Klik pilihan di atas lalu tekan Mulai atau ENTER", True, WARNA_TEKS_REDUP
        )
        layar.blit(hint, hint.get_rect(centerx=lebar // 2, top=510))

        pygame.display.flip()
        jam.tick(30)


def jalankan_animasi_tunggal(maze, mode, judul):
    """Animasikan satu algoritma (BFS atau DFS) lengkap dengan waktu eksekusi."""
    nama_algoritma = "BFS" if mode == "bfs" else "DFS"
    fungsi = bfs if mode == "bfs" else dfs
    hasil = ukur_algoritma(fungsi, maze)

    tata = hitung_tata_letak(maze)
    layar = pygame.display.set_mode((tata["lebar_jendela"], tata["tinggi_jendela"]))
    pygame.display.set_caption(f"Maze Game - Animasi {nama_algoritma} ({judul})")
    jam = pygame.time.Clock()

    font_tombol = pygame.font.SysFont(None, 21)
    font_hint = pygame.font.SysFont(None, 19)

    dikunjungi = hasil["dikunjungi"]
    riwayat_frontier = fungsi(maze, rekam=True)["riwayat_frontier"]
    jalur = hasil["jalur"]
    total_dikunjungi = hasil["jumlah_dikunjungi"]

    jumlah_tampil = 0
    kecepatan = 1
    jeda = False
    selesai = False

    panel_x = tata["panel_x"]
    rect_jeda = pygame.Rect(panel_x, 518, 106, 34)
    rect_ulang = pygame.Rect(panel_x + 114, 518, 106, 34)
    rect_menu = pygame.Rect(panel_x, 562, 220, 38)

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                return "keluar"
            elif kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_ESCAPE:
                    return "menu"
                elif kejadian.key == pygame.K_SPACE:
                    if not selesai:
                        jeda = not jeda
                elif kejadian.key == pygame.K_UP and kecepatan < 3:
                    kecepatan += 1
                elif kejadian.key == pygame.K_DOWN and kecepatan > 1:
                    kecepatan -= 1
                elif kejadian.key == pygame.K_r:
                    jumlah_tampil = 0
                    selesai = False
                    jeda = False
            elif kejadian.type == pygame.MOUSEBUTTONDOWN and kejadian.button == 1:
                if rect_jeda.collidepoint(pos_mouse) and not selesai:
                    jeda = not jeda
                elif rect_ulang.collidepoint(pos_mouse):
                    jumlah_tampil = 0
                    selesai = False
                    jeda = False
                elif rect_menu.collidepoint(pos_mouse):
                    return "menu"

        if not selesai and not jeda:
            jumlah_tampil += kecepatan
            if jumlah_tampil >= total_dikunjungi:
                jumlah_tampil = total_dikunjungi
                selesai = True

        jalur_tampil = jalur if selesai else []

        if selesai:
            teks_jalur = (
                f"{hasil['panjang_jalur']} langkah" if jalur else "Tidak ditemukan"
            )
            teks_waktu = f"{hasil['waktu_ms']:.4f} ms"
            teks_biaya = str(hasil["biaya_jalur"]) if jalur else "-"
            teks_frontier = str(hasil["frontier_maks"])
            teks_memori = f"{hasil['memori_kb']:.1f} KB"
        else:
            teks_jalur = teks_waktu = "..."
            teks_biaya = teks_frontier = teks_memori = "..."

        info = [
            f"Algoritma: {nama_algoritma}",
            f"Dikunjungi: {jumlah_tampil}",
            f"Langkah: {teks_jalur}",
            f"Total biaya: {teks_biaya}",
            f"Frontier maks: {teks_frontier}",
            f"Memori puncak: {teks_memori}",
            f"Waktu: {teks_waktu}",
        ]

        layar.fill(WARNA_LATAR)
        gambar_maze(
            layar,
            maze,
            tata["maze_x"],
            tata["maze_y"],
            tata["ukuran_sel"],
            frontier=frontier_saat(hasil, jumlah_tampil, maze),
            dieksplorasi=dikunjungi[:jumlah_tampil],
            jalur=jalur_tampil,
        )
        gambar_panel_samping(
            layar, tata["panel_x"], tata["panel_y"], maze, judul, info
        )

        # Kontrol di bawah legenda panel samping
        hint_surf = font_hint.render(
            f"SPASI: Jeda | R: Ulang | Kecepatan: {kecepatan}", True, WARNA_TEKS_REDUP
        )
        layar.blit(hint_surf, (panel_x, 492))

        gambar_tombol(
            layar,
            rect_jeda,
            "Lanjut" if jeda else "Jeda",
            font_tombol,
            hover=(not selesai and rect_jeda.collidepoint(pos_mouse)),
            warna_normal=(240, 242, 246) if selesai else WARNA_KARTU,
            warna_teks=WARNA_TEKS_REDUP if selesai else WARNA_TEKS,
        )
        gambar_tombol(
            layar,
            rect_ulang,
            "Ulangi (R)",
            font_tombol,
            hover=rect_ulang.collidepoint(pos_mouse),
        )
        gambar_tombol(
            layar,
            rect_menu,
            "Kembali ke Menu (ESC)",
            font_tombol,
            aktif=True,
            warna_aktif=(70, 92, 114) if rect_menu.collidepoint(pos_mouse) else WARNA_AKSEN,
        )

        pygame.display.flip()
        jam.tick(30)


def _gambar_legenda_ringkas(layar, x, y, font):
    """Gambar legenda warna secara horizontal di bagian bawah layar perbandingan."""
    item = [
        (WARNA_FRONTIER, "Frontier"),
        (WARNA_DIEKSPLORASI, "Dieksplorasi"),
        (WARNA_JALUR, "Jalur akhir"),
        (WARNA_DINDING, "Dinding"),
        (WARNA_BIAYA[1], "Biaya 1"),
        (WARNA_BIAYA[2], "2"),
        (WARNA_BIAYA[3], "3"),
    ]
    posisi_x = x
    ukuran = 14
    for warna, label in item:
        pygame.draw.rect(layar, warna, (posisi_x, y + 2, ukuran, ukuran))
        pygame.draw.rect(layar, WARNA_GARIS, (posisi_x, y + 2, ukuran, ukuran), 1)
        surf = font.render(label, True, WARNA_TEKS)
        layar.blit(surf, (posisi_x + ukuran + 6, y))
        posisi_x += ukuran + 6 + surf.get_width() + 18


def _buat_ringkasan_perbandingan(hasil_bfs, hasil_dfs):
    """Susun dua baris kesimpulan perbandingan BFS vs DFS."""
    p_bfs, p_dfs = hasil_bfs["panjang_jalur"], hasil_dfs["panjang_jalur"]
    if p_bfs < p_dfs:
        info_jalur = f"Langkah lebih sedikit: BFS ({p_bfs} vs {p_dfs})"
    elif p_dfs < p_bfs:
        info_jalur = f"Langkah lebih sedikit: DFS ({p_dfs} vs {p_bfs})"
    else:
        info_jalur = f"Langkah sama ({p_bfs})"

    b_bfs, b_dfs = hasil_bfs["biaya_jalur"], hasil_dfs["biaya_jalur"]
    if b_bfs < b_dfs:
        info_biaya = f"Biaya lebih murah: BFS ({b_bfs} vs {b_dfs})"
    elif b_dfs < b_bfs:
        info_biaya = f"Biaya lebih murah: DFS ({b_dfs} vs {b_bfs})"
    else:
        info_biaya = f"Biaya total sama ({b_bfs})"

    v_bfs, v_dfs = hasil_bfs["jumlah_dikunjungi"], hasil_dfs["jumlah_dikunjungi"]
    if v_bfs < v_dfs:
        info_node = f"Node lebih hemat: BFS ({v_bfs} vs {v_dfs})"
    elif v_dfs < v_bfs:
        info_node = f"Node lebih hemat: DFS ({v_dfs} vs {v_bfs})"
    else:
        info_node = f"Node dikunjungi sama ({v_bfs})"

    w_bfs, w_dfs = hasil_bfs["waktu_ms"], hasil_dfs["waktu_ms"]
    lebih_cepat = "BFS" if w_bfs < w_dfs else "DFS"
    return [
        f"{info_jalur}  |  {info_biaya}",
        f"{info_node}  |  Lebih cepat: {lebih_cepat}",
    ]


def jalankan_perbandingan(maze, judul):
    """Mode Side-by-Side: jalankan BFS (kiri) dan DFS (kanan) secara bersamaan."""
    hasil_bfs = ukur_algoritma(bfs, maze)
    hasil_dfs = ukur_algoritma(dfs, maze)

    lebar, tinggi = 840, 640
    layar = pygame.display.set_mode((lebar, tinggi))
    pygame.display.set_caption(f"Maze Game - Perbandingan BFS vs DFS ({judul})")
    jam = pygame.time.Clock()

    font_header = pygame.font.SysFont(None, 27)
    font_kolom = pygame.font.SysFont(None, 24)
    font_stat = pygame.font.SysFont(None, 21)
    font_tombol = pygame.font.SysFont(None, 20)
    font_kecil = pygame.font.SysFont(None, 19)

    area_maze = 300
    ukuran_sel = hitung_ukuran_sel(maze, area_maze, area_maze)
    offset_x = (area_maze - maze.lebar * ukuran_sel) // 2
    offset_y = (area_maze - maze.tinggi * ukuran_sel) // 2

    # Tombol kontrol di header kanan atas
    rect_jeda = pygame.Rect(520, 10, 96, 32)
    rect_ulang = pygame.Rect(624, 10, 92, 32)
    rect_menu = pygame.Rect(724, 10, 96, 32)

    tampil_bfs = 0
    tampil_dfs = 0
    kecepatan = 1
    jeda = False
    selesai_bfs = False
    selesai_dfs = False

    ringkasan = _buat_ringkasan_perbandingan(hasil_bfs, hasil_dfs)

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                return "keluar"
            elif kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_ESCAPE:
                    return "menu"
                elif kejadian.key == pygame.K_SPACE:
                    if not (selesai_bfs and selesai_dfs):
                        jeda = not jeda
                elif kejadian.key == pygame.K_UP and kecepatan < 3:
                    kecepatan += 1
                elif kejadian.key == pygame.K_DOWN and kecepatan > 1:
                    kecepatan -= 1
                elif kejadian.key == pygame.K_r:
                    tampil_bfs = 0
                    tampil_dfs = 0
                    selesai_bfs = False
                    selesai_dfs = False
                    jeda = False
            elif kejadian.type == pygame.MOUSEBUTTONDOWN and kejadian.button == 1:
                if rect_jeda.collidepoint(pos_mouse) and not (selesai_bfs and selesai_dfs):
                    jeda = not jeda
                elif rect_ulang.collidepoint(pos_mouse):
                    tampil_bfs = 0
                    tampil_dfs = 0
                    selesai_bfs = False
                    selesai_dfs = False
                    jeda = False
                elif rect_menu.collidepoint(pos_mouse):
                    return "menu"

        if not jeda:
            if not selesai_bfs:
                tampil_bfs += kecepatan
                if tampil_bfs >= hasil_bfs["jumlah_dikunjungi"]:
                    tampil_bfs = hasil_bfs["jumlah_dikunjungi"]
                    selesai_bfs = True
            if not selesai_dfs:
                tampil_dfs += kecepatan
                if tampil_dfs >= hasil_dfs["jumlah_dikunjungi"]:
                    tampil_dfs = hasil_dfs["jumlah_dikunjungi"]
                    selesai_dfs = True

        layar.fill(WARNA_LATAR)

        # Header atas
        teks_header = f"Perbandingan BFS vs DFS - {judul} ({maze.tinggi}x{maze.lebar})"
        layar.blit(font_header.render(teks_header, True, WARNA_TEKS), (20, 16))

        semua_selesai = selesai_bfs and selesai_dfs
        gambar_tombol(
            layar,
            rect_jeda,
            "Lanjut" if jeda else "Jeda",
            font_tombol,
            hover=(not semua_selesai and rect_jeda.collidepoint(pos_mouse)),
            warna_normal=(240, 242, 246) if semua_selesai else WARNA_KARTU,
            warna_teks=WARNA_TEKS_REDUP if semua_selesai else WARNA_TEKS,
        )
        gambar_tombol(
            layar,
            rect_ulang,
            "Ulangi (R)",
            font_tombol,
            hover=rect_ulang.collidepoint(pos_mouse),
        )
        gambar_tombol(
            layar,
            rect_menu,
            "Menu (ESC)",
            font_tombol,
            aktif=True,
            warna_aktif=(70, 92, 114) if rect_menu.collidepoint(pos_mouse) else WARNA_AKSEN,
        )

        # Dua kolom berdampingan: BFS (kiri) dan DFS (kanan)
        kolom_data = [
            (20, "BFS (Breadth-First Search)", WARNA_BFS, hasil_bfs, tampil_bfs, selesai_bfs),
            (430, "DFS (Depth-First Search)", WARNA_DFS, hasil_dfs, tampil_dfs, selesai_dfs),
        ]

        for kartu_x, nama_judul, warna_judul, data, tampil, sudah_selesai in kolom_data:
            kartu = pygame.Rect(kartu_x, 54, 390, 488)
            pygame.draw.rect(layar, WARNA_KARTU, kartu, border_radius=10)
            pygame.draw.rect(layar, WARNA_BORDER, kartu, 1, border_radius=10)

            # Judul kolom & status
            layar.blit(font_kolom.render(nama_judul, True, warna_judul), (kartu_x + 15, 64))
            teks_status = "Selesai" if sudah_selesai else ("Dijeda" if jeda else "Berjalan")
            warna_status = WARNA_MULAI if sudah_selesai else WARNA_TEKS_REDUP
            surf_status = font_kecil.render(teks_status, True, warna_status)
            layar.blit(surf_status, (kartu_x + 375 - surf_status.get_width(), 67))

            # Maze di tengah kolom
            maze_x = kartu_x + 15 + offset_x
            maze_y = 90 + offset_y
            gambar_maze(
                layar,
                maze,
                maze_x,
                maze_y,
                ukuran_sel,
                frontier=frontier_saat(data, tampil, maze), 
                dieksplorasi=data["dikunjungi"][:tampil],
                jalur=data["jalur"] if sudah_selesai else [],
            )

            # Statistik di bawah maze (hasil akhir baru tampil setelah finish tercapai)
            teks_jalur = (
                f"{data['panjang_jalur']} langkah"
                if (sudah_selesai and data["jalur"])
                else ("Tidak ditemukan" if sudah_selesai else "...")
            )
            teks_waktu = (
                f"{data['waktu_ms']:.4f} ms" if sudah_selesai else "..."
            )
            teks_biaya = (
                str(data["biaya_jalur"]) if (sudah_selesai and data["jalur"])
                else ("-" if sudah_selesai else "...")
            )
            teks_frontier = str(data["frontier_maks"]) if sudah_selesai else "..."
            teks_memori = f"{data['memori_kb']:.1f} KB" if sudah_selesai else "..."
            baris_stat = [
                ("Total biaya", f": {teks_biaya}"),
                ("Langkah", f": {teks_jalur}"),
                ("Node dikunjungi", f": {tampil}"),
                ("Frontier maksimum", f": {teks_frontier}"),
                ("Memori puncak", f": {teks_memori}"),
                ("Waktu eksekusi", f": {teks_waktu}"),
            ]
            for idx, (label_stat, nilai_stat) in enumerate(baris_stat):
                y_stat = 400 + idx * 22
                layar.blit(font_stat.render(label_stat, True, WARNA_TEKS), (kartu_x + 15, y_stat))
                layar.blit(font_stat.render(nilai_stat, True, WARNA_TEKS), (kartu_x + 156, y_stat))

        # Bar bawah: legenda + ringkasan / petunjuk
        bar_bawah = pygame.Rect(20, 552, 800, 72)
        pygame.draw.rect(layar, WARNA_KARTU, bar_bawah, border_radius=10)
        pygame.draw.rect(layar, WARNA_BORDER, bar_bawah, 1, border_radius=10)

        _gambar_legenda_ringkas(layar, 34, 563, font_kecil)
        surf_kecepatan = font_kecil.render(
            f"Kecepatan: {kecepatan} (Atas/Bawah)", True, WARNA_TEKS_REDUP
        )
        layar.blit(surf_kecepatan, (806 - surf_kecepatan.get_width(), 563))

        if selesai_bfs and selesai_dfs:
            surf_bawah = font_kecil.render(ringkasan[0], True, WARNA_AKSEN)
            surf_bawah2 = font_kecil.render(ringkasan[1], True, WARNA_AKSEN)
            layar.blit(surf_bawah2, (34, 607))
        else:
            surf_bawah = font_kecil.render(
                "SPASI: Jeda/Lanjut  |  Atas/Bawah: Kecepatan  |  R: Ulangi  |  ESC: Kembali ke Menu",
                True,
                WARNA_TEKS_REDUP,
            )
        layar.blit(surf_bawah, (34, 590))

        pygame.display.flip()
        jam.tick(30)


def main():
    pygame.init()
    pilihan = {
        "mode": "bandingkan",
        "ukuran": "small",
        "nomor": 1,
    }

    while True:
        aksi = tampilkan_menu(pilihan)
        if aksi == "keluar":
            break

        jalur_file, nama_file = path_maze(pilihan["ukuran"], pilihan["nomor"])
        maze = baca_maze(jalur_file)

        if pilihan["mode"] == "bandingkan":
            hasil_layar = jalankan_perbandingan(maze, nama_file)
        else:
            hasil_layar = jalankan_animasi_tunggal(maze, pilihan["mode"], nama_file)

        if hasil_layar == "keluar":
            break

    pygame.quit()


if __name__ == "__main__":
    main()