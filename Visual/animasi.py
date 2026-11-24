import pygame

from Algorithms.bfs import bfs
from Algorithms.dfs import dfs
from statistik import ukur_algoritma
from Visual.ui import (
    gambar_tombol, WARNA_AKSEN, WARNA_KARTU, WARNA_TEKS_REDUP,
    WARNA_BORDER, WARNA_BFS, WARNA_DFS, WARNA_MULAI,
)
from Visual.visualizer import (
    hitung_ukuran_sel, hitung_tata_letak, gambar_maze, gambar_panel_samping,
    WARNA_FRONTIER, WARNA_DIEKSPLORASI, WARNA_JALUR, WARNA_LATAR,
    WARNA_GARIS, WARNA_DINDING, WARNA_BIAYA, WARNA_TEKS,
)

def frontier_saat(data, jumlah_tampil, maze):
    if jumlah_tampil <= 0:
        return [maze.start]
    sudah = set(data["dikunjungi"][:jumlah_tampil])
    return [s for s in data["riwayat_frontier"][jumlah_tampil - 1] if s not in sudah]

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