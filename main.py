import os
import pygame

from Maze.maze import baca_maze
from Visual.animasi import jalankan_animasi_tunggal, jalankan_perbandingan
from Visual.ui import (
    gambar_tombol, WARNA_AKSEN, WARNA_BFS, WARNA_BORDER, WARNA_DFS,
    WARNA_KARTU, WARNA_KELUAR, WARNA_KELUAR_HOVER, WARNA_MULAI,
    WARNA_MULAI_HOVER, WARNA_TEKS_REDUP,
)
from Visual.visualizer import WARNA_LATAR, WARNA_TEKS

# Lokasi folder data maze (relatif terhadap lokasi main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Maze", "data")

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