# maze/maze.py
# Membaca maze dari file txt dan menyediakan fungsi dasar untuk algoritma.

# Urutan arah SELALU sama: atas, kanan, bawah, kiri (sesuai proposal)
ARAH = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # (delta_baris, delta_kolom)


class Maze:
    def __init__(self, grid, start, finish, biaya):
        self.grid = grid          # list 2D berisi karakter
        self.start = start        # (baris, kolom)
        self.finish = finish      # (baris, kolom)
        self.biaya = biaya        # list 2D biaya masuk tiap sel (0 = dinding/start)
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

    def biaya_sel(self, posisi):
        """Biaya untuk MASUK ke sel ini."""
        baris, kolom = posisi
        return self.biaya[baris][kolom]

    def hitung_biaya_jalur(self, jalur):
        """Total biaya = jumlah biaya sel yang dimasuki.
        Start tidak dihitung, finish dihitung."""
        return sum(self.biaya_sel(p) for p in jalur[1:])


def baca_maze(nama_file):
    """Baca file txt lalu kembalikan objek Maze.

    '#' dinding | '1','2','3' sel jalan berbiaya 1/2/3
    '.' jalan biasa (biaya 1, untuk file lama) | 'S' start | 'F' finish (biaya 1)
    """
    grid = []
    biaya = []
    start = None
    finish = None

    with open(nama_file, 'r') as f:
        for baris_teks in f:
            baris_teks = baris_teks.rstrip('\n')
            if baris_teks == '':
                continue
            baris = list(baris_teks)
            baris_biaya = []
            for j, sel in enumerate(baris):
                if sel == 'S':
                    start = (len(grid), j)
                    baris_biaya.append(0)
                elif sel == 'F':
                    finish = (len(grid), j)
                    baris_biaya.append(1)
                elif sel in '123':
                    baris_biaya.append(int(sel))
                elif sel == '.':
                    baris_biaya.append(1)
                else:                       # '#'
                    baris_biaya.append(0)
            grid.append(baris)
            biaya.append(baris_biaya)

    if start is None or finish is None:
        raise ValueError("Maze harus punya satu 'S' dan satu 'F'")

    return Maze(grid, start, finish, biaya)