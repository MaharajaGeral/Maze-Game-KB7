import pygame

# KODE WARNA
WARNA_LATAR = (232, 235, 240)      # latar jendela (terang, agar dinding gelap kelihatan)
WARNA_GARIS = (190, 190, 190)      # garis tipis antar sel
WARNA_DINDING = (45, 50, 60)       # sel dinding '#'
WARNA_JALAN = (245, 245, 245)      # sel jalan kosong '.'
WARNA_START = (46, 204, 113)       # hijau   -> titik awal (S)
WARNA_FINISH = (231, 76, 60)       # merah   -> titik tujuan (F)
WARNA_FRONTIER = (241, 196, 15)    # kuning  -> sel di antrean/stack
WARNA_DIEKSPLORASI = (133, 193, 233)  # biru muda -> sudah dieksplorasi
WARNA_JALUR = (155, 89, 182)       # ungu    -> jalur akhir
WARNA_TEKS = (30, 33, 40)          # teks legenda
WARNA_LABEL = (255, 255, 255)      # huruf S/F di dalam sel
WARNA_BIAYA = {                    # Warna biaya sel jalan: makin coklat = makin mahal
    1: (245, 245, 245),   # putih       -> biaya 1 (jalan biasa)
    2: (222, 184, 135),   # coklat muda -> biaya 2 (medan sulit)
    3: (160, 110, 70),    # coklat tua  -> biaya 3 (medan paling sulit)
}

# Daftar legenda: (warna dan keterangan)
LEGENDA = [
    (WARNA_START, "Start (S)"),
    (WARNA_FINISH, "Finish (F)"),
    (WARNA_FRONTIER, "Frontier (antre)"),
    (WARNA_DIEKSPLORASI, "Sudah dieksplorasi"),
    (WARNA_JALUR, "Jalur akhir"),
    (WARNA_DINDING, "Dinding"),
    (WARNA_BIAYA[1], "Biaya 1 (jalan biasa)"),
    (WARNA_BIAYA[2], "Biaya 2 (medan sulit)"),
    (WARNA_BIAYA[3], "Biaya 3 (medan sulit)"),
]

# UKURAN TATA LETAK (piksel)

MARGIN = 20           # jarak tepi jendela ke isi
LEBAR_PANEL = 240     # lebar panel samping (judul, info, legenda)


def hitung_ukuran_sel(maze, lebar_area, tinggi_area):
    """Hitung ukuran 1 sel (piksel) agar seluruh maze muat di area yang tersedia.

    lebar_area, tinggi_area: ruang (piksel) yang boleh dipakai untuk maze.
    Dengan cara ini maze 10x10, 15x15, maupun 20x20 sama-sama pas di layar.
    """
    ukuran_dari_lebar = lebar_area // maze.lebar
    ukuran_dari_tinggi = tinggi_area // maze.tinggi
    return max(2, min(ukuran_dari_lebar, ukuran_dari_tinggi))


def _pilih_warna(maze, baris, kolom, frontier, dieksplorasi, jalur):
    """Tentukan warna sebuah sel. Urutan prioritas dari atas ke bawah:
    start/finish > jalur akhir > frontier > dieksplorasi > jalan/dinding.
    """
    posisi = (baris, kolom)

    if posisi == maze.start:
        return WARNA_START
    if posisi == maze.finish:
        return WARNA_FINISH
    if maze.grid[baris][kolom] == '#':
        return WARNA_DINDING
    dasar = WARNA_BIAYA.get(maze.biaya[baris][kolom], WARNA_JALAN)
    # Eksplorasi/jalur dicampur dengan warna biaya supaya biaya tetap terlihat
    if posisi in jalur:
        return _campur(dasar, WARNA_JALUR, 0.75)
    if posisi in frontier:
        return WARNA_FRONTIER
    if posisi in dieksplorasi:
        return _campur(dasar, WARNA_DIEKSPLORASI, 0.55)
    return dasar


def _campur(warna_a, warna_b, porsi_b):
    """Campur dua warna. porsi_b = seberapa banyak warna_b (0.0 - 1.0)."""
    return tuple(int(a * (1 - porsi_b) + b * porsi_b)
                 for a, b in zip(warna_a, warna_b))


def gambar_maze(layar, maze, x, y, ukuran_sel,
                frontier=(), dieksplorasi=(), jalur=()):
    """Gambar seluruh grid maze di layar pygame.

    layar        : surface pygame tujuan
    maze         : objek Maze (dari Maze/maze.py)
    x, y         : pojok kiri atas area maze di layar (piksel)
    ukuran_sel   : sisi 1 sel dalam piksel
    frontier     : kumpulan (baris, kolom) yang sedang di antrean/stack
    dieksplorasi : kumpulan (baris, kolom) yang sudah dikunjungi
    jalur        : kumpulan (baris, kolom) jalur akhir start -> finish

    Tiga kumpulan terakhir boleh kosong; maka yang tergambar hanya maze polos.
    Dipanggil ulang tiap frame oleh animasi dengan isi kumpulan yang bertambah.
    """
    # Diubah ke set supaya pengecekan "apakah sel ada di kumpulan" cepat
    frontier = set(frontier)
    dieksplorasi = set(dieksplorasi)
    jalur = set(jalur)

    # Latar abu-abu muda: terlihat sebagai garis tipis di sela-sela sel
    pygame.draw.rect(layar, WARNA_GARIS,
                     (x, y, maze.lebar * ukuran_sel, maze.tinggi * ukuran_sel))

    tampil_angka = ukuran_sel >= 14
    font_angka = pygame.font.SysFont(None, max(13, int(ukuran_sel * 0.6))) if tampil_angka else None

    for baris in range(maze.tinggi):
        for kolom in range(maze.lebar):
            warna = _pilih_warna(maze, baris, kolom,
                                 frontier, dieksplorasi, jalur)
            px = x + kolom * ukuran_sel
            py = y + baris * ukuran_sel
            # ukuran_sel - 1 menyisakan 1 piksel untuk garis antar sel
            pygame.draw.rect(layar, warna,
                             (px, py, ukuran_sel - 1, ukuran_sel - 1))

            # Angka biaya hanya untuk medan sulit (2 dan 3)
            biaya = maze.biaya[baris][kolom]
            if tampil_angka and biaya >= 2 and (baris, kolom) not in (maze.start, maze.finish):
                teks = font_angka.render(str(biaya), True, WARNA_TEKS)
                layar.blit(teks, teks.get_rect(
                    center=(px + (ukuran_sel - 1) // 2, py + (ukuran_sel - 1) // 2)))

    _gambar_label(layar, "S", maze.start, x, y, ukuran_sel)
    _gambar_label(layar, "F", maze.finish, x, y, ukuran_sel)


def _gambar_label(layar, huruf, posisi, x, y, ukuran_sel):
    """Tulis huruf (S/F) di tengah sel, supaya start dan finish jelas terlihat."""
    baris, kolom = posisi
    font = pygame.font.SysFont(None, int(ukuran_sel * 0.8))
    teks = font.render(huruf, True, WARNA_LABEL)
    pusat_x = x + kolom * ukuran_sel + (ukuran_sel - 1) // 2
    pusat_y = y + baris * ukuran_sel + (ukuran_sel - 1) // 2
    layar.blit(teks, teks.get_rect(center=(pusat_x, pusat_y)))


def gambar_legenda(layar, x, y, ukuran_kotak=16):
    """Gambar keterangan kode warna (kotak warna + tulisan) mulai dari (x, y)."""
    font = pygame.font.SysFont(None, 22)
    jarak_baris = ukuran_kotak + 4

    for i, (warna, keterangan) in enumerate(LEGENDA):
        py = y + i * jarak_baris
        pygame.draw.rect(layar, warna, (x, py, ukuran_kotak, ukuran_kotak))
        pygame.draw.rect(layar, WARNA_GARIS,
                         (x, py, ukuran_kotak, ukuran_kotak), 1)  # bingkai
        teks = font.render(keterangan, True, WARNA_TEKS)
        layar.blit(teks, (x + ukuran_kotak + 10, py))


def hitung_tata_letak(maze, lebar_area=600, tinggi_area=600):
    """Tentukan posisi dan ukuran semua elemen supaya konsisten di semua mode.

    Hasilnya dictionary berisi:
      ukuran_sel                  : sisi 1 sel (piksel)
      maze_x, maze_y              : pojok kiri atas area maze
      panel_x, panel_y            : pojok kiri atas panel samping
      lebar_jendela, tinggi_jendela : ukuran jendela yang pas untuk maze ini

    Contoh:
        tata = hitung_tata_letak(maze)
        layar = pygame.display.set_mode((tata["lebar_jendela"], tata["tinggi_jendela"]))
    """
    ukuran = hitung_ukuran_sel(maze, lebar_area, tinggi_area)
    lebar_maze = maze.lebar * ukuran
    tinggi_maze = maze.tinggi * ukuran
    return {
        "ukuran_sel": ukuran,
        "maze_x": MARGIN,
        "maze_y": MARGIN,
        "panel_x": MARGIN * 2 + lebar_maze,
        "panel_y": MARGIN,
        "lebar_jendela": MARGIN * 3 + lebar_maze + LEBAR_PANEL,
        "tinggi_jendela": MARGIN * 2 + tinggi_maze,
    }


def gambar_panel_samping(layar, x, y, maze, judul, baris_info=()):
    """Gambar panel di samping maze: judul, info maze, lalu legenda warna.

    judul      : tulisan besar paling atas, misalnya "Maze Kecil 1"
    baris_info : daftar tulisan tambahan (opsional), misalnya
                 ["Algoritma: BFS"]. Dipakai bagian animasi/menu bila perlu.
    """
    font_judul = pygame.font.SysFont(None, 32)
    font_info = pygame.font.SysFont(None, 22)

    # Judul
    layar.blit(font_judul.render(judul, True, WARNA_TEKS), (x, y))
    posisi_y = y + 40

    # Info dasar maze (diambil dari objek Maze) + info tambahan dari pemanggil
    info = [
        "Ukuran: %d x %d" % (maze.tinggi, maze.lebar),
        "Start: (%d, %d)" % maze.start,
        "Finish: (%d, %d)" % maze.finish,
    ]
    info.extend(baris_info)
    for teks in info:
        layar.blit(font_info.render(teks, True, WARNA_TEKS), (x, posisi_y))
        posisi_y += 20

    # Legenda di bawah info
    posisi_y += 10
    layar.blit(font_info.render("Keterangan warna:", True, WARNA_TEKS),
               (x, posisi_y))
    gambar_legenda(layar, x, posisi_y + 24)


if __name__ == "__main__":
    import sys
    from Maze.maze import baca_maze

    nama_file = sys.argv[1] if len(sys.argv) > 1 else "Maze/data/small_1.txt"
    maze = baca_maze(nama_file)

    pygame.init()
    tata = hitung_tata_letak(maze)
    layar = pygame.display.set_mode((tata["lebar_jendela"], tata["tinggi_jendela"]))
    pygame.display.set_caption("Demo Visual Maze - " + nama_file)
    ukuran = tata["ukuran_sel"]

    # Data contoh (palsu) hanya untuk melihat warna; BUKAN hasil BFS/DFS
    sel_jalan = [(b, k) for b in range(maze.tinggi) for k in range(maze.lebar)
                 if maze.grid[b][k] not in '#SF']
    contoh_dieksplorasi = sel_jalan[:len(sel_jalan) // 2]
    contoh_frontier = sel_jalan[len(sel_jalan) // 2: len(sel_jalan) // 2 + 4]
    contoh_jalur = sel_jalan[:5]
    tampil_contoh = False

    jalan = True
    while jalan:
        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                jalan = False
            elif kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_ESCAPE:
                    jalan = False
                elif kejadian.key == pygame.K_c:
                    tampil_contoh = not tampil_contoh

        layar.fill(WARNA_LATAR)
        if tampil_contoh:
            gambar_maze(layar, maze, tata["maze_x"], tata["maze_y"], ukuran,
                        contoh_frontier, contoh_dieksplorasi, contoh_jalur)
        else:
            gambar_maze(layar, maze, tata["maze_x"], tata["maze_y"], ukuran)
        gambar_panel_samping(layar, tata["panel_x"], tata["panel_y"],
                             maze, nama_file.split("/")[-1])
        pygame.display.flip()

    pygame.quit()