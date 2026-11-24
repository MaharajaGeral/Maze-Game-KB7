import pygame
from Visual.visualizer import WARNA_TEKS

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
