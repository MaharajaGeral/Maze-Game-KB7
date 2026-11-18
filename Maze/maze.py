# maze/maze.py
# Membaca maze dari file txt dan menyediakan fungsi dasar untuk algoritma.

# Urutan arah SELALU sama: atas, kanan, bawah, kiri (sesuai proposal)
ARAH = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # (delta_baris, delta_kolom)


class Maze:
    def __init__(self, grid, start, finish):
        self.grid = grid          # list 2D berisi karakter
        self.start = start        # (baris, kolom)
        self.finish = finish      # (baris, kolom)
        self.tinggi = len(grid)
        self.lebar = len(grid[0])

    def bisa_dilalui(self, baris, kolom):
        """True jika sel ada di dalam grid dan bukan dinding."""
        if baris < 0 or baris >= self.tinggi:
            return False
        if kolom < 0 or kolom >= self.lebar:
            return False
        return self.grid[baris][kolom] != '#'

    def tetangga(self, posisi):
        """Daftar sel tetangga yang valid, urutan: atas, kanan, bawah, kiri."""
        baris, kolom = posisi
        hasil = []
        for db, dk in ARAH:
            b, k = baris + db, kolom + dk
            if self.bisa_dilalui(b, k):
                hasil.append((b, k))
        return hasil


def baca_maze(nama_file):
    """Baca file txt lalu kembalikan objek Maze."""
    grid = []
    start = None
    finish = None

    with open(nama_file, 'r') as f:
        for i, baris_teks in enumerate(f):
            baris_teks = baris_teks.rstrip('\n')
            if baris_teks == '':
                continue
            baris = list(baris_teks)
            for j, sel in enumerate(baris):
                if sel == 'S':
                    start = (len(grid), j)
                elif sel == 'F':
                    finish = (len(grid), j)
            grid.append(baris)

    if start is None or finish is None:
        raise ValueError("Maze harus punya satu 'S' dan satu 'F'")

    return Maze(grid, start, finish)