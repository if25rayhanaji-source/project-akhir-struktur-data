import csv
import os

FILE_CSV = "pasien.csv"

# =========================
# LINKED LIST
# =========================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        node = Node(data)

        if not self.head:
            self.head = node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = node

    def tampilkan(self):
        current = self.head

        if not current:
            print("Data kosong")
            return

        while current:
            print(current.data)
            current = current.next

    def cari(self, id_pasien):
        current = self.head

        while current:
            if current.data["id"] == id_pasien:
                return current
            current = current.next

        return None

    def hapus(self, id_pasien):
        current = self.head
        prev = None

        while current:
            if current.data["id"] == id_pasien:

                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                return True

            prev = current
            current = current.next

        return False


# =========================
# QUEUE
# =========================

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.is_empty():
            return None

        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0


# =========================
# CSV
# =========================

def load_data():
    pasien_list = LinkedList()
    queue = Queue()

    if os.path.exists(FILE_CSV):
        with open(FILE_CSV, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                pasien_list.tambah(row)
                queue.enqueue(row)

    return pasien_list, queue


def save_data(linkedlist):
    data = []

    current = linkedlist.head

    while current:
        data.append(current.data)
        current = current.next

    with open(FILE_CSV, mode="w", newline='', encoding="utf-8") as file:
        fieldnames = ["id", "nama", "umur", "keluhan", "antrian"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            writer.writerow(item)


# =========================
# CRUD
# =========================

def tambah_pasien(linkedlist, queue):
    id_pasien = input("ID Pasien : ")
    nama = input("Nama : ")
    umur = input("Umur : ")
    keluhan = input("Keluhan : ")

    nomor_antrian = len(queue.items) + 1

    data = {
        "id": id_pasien,
        "nama": nama,
        "umur": umur,
        "keluhan": keluhan,
        "antrian": str(nomor_antrian)
    }

    linkedlist.tambah(data)
    queue.enqueue(data)

    save_data(linkedlist)

    print("Pasien berhasil ditambahkan")


def tampil_data(linkedlist):
    current = linkedlist.head

    print("\n=== DATA PASIEN ===")

    while current:
        d = current.data

        print(
            f"ID:{d['id']} | "
            f"Nama:{d['nama']} | "
            f"Umur:{d['umur']} | "
            f"Keluhan:{d['keluhan']} | "
            f"Antrian:{d['antrian']}"
        )

        current = current.next


def cari_pasien(linkedlist):
    id_pasien = input("Masukkan ID: ")

    hasil = linkedlist.cari(id_pasien)

    if hasil:
        print("Data ditemukan")
        print(hasil.data)
    else:
        print("Data tidak ditemukan")


def update_pasien(linkedlist):
    id_pasien = input("ID pasien yang diupdate: ")

    pasien = linkedlist.cari(id_pasien)

    if pasien:
        pasien.data["nama"] = input("Nama baru: ")
        pasien.data["umur"] = input("Umur baru: ")
        pasien.data["keluhan"] = input("Keluhan baru: ")

        save_data(linkedlist)

        print("Data berhasil diupdate")

    else:
        print("Data tidak ditemukan")


def hapus_pasien(linkedlist):
    id_pasien = input("ID pasien yang dihapus: ")

    if linkedlist.hapus(id_pasien):
        save_data(linkedlist)
        print("Data berhasil dihapus")
    else:
        print("Data tidak ditemukan")


# =========================
# SORTING
# Bubble Sort
# =========================

def sorting_nama(linkedlist):

    data = []

    current = linkedlist.head

    while current:
        data.append(current.data)
        current = current.next

    n = len(data)

    for i in range(n):
        for j in range(n - i - 1):
            if data[j]["nama"].lower() > data[j + 1]["nama"].lower():
                data[j], data[j + 1] = data[j + 1], data[j]

    print("\n=== DATA TERURUT ===")

    for d in data:
        print(d)


# =========================
# PANGGIL ANTRIAN
# =========================

def panggil_antrian(queue):

    pasien = queue.dequeue()

    if pasien:
        print("\nPasien Dipanggil:")
        print(
            pasien["antrian"],
            pasien["nama"]
        )
    else:
        print("Tidak ada antrian")


# =========================
# MENU
# =========================

def menu():

    linkedlist, queue = load_data()

    while True:

        print("\n===== SISTEM ANTRIAN RUMAH SAKIT =====")
        print("1. Tambah Pasien")
        print("2. Tampilkan Pasien")
        print("3. Cari Pasien")
        print("4. Update Pasien")
        print("5. Hapus Pasien")
        print("6. Panggil Antrian")
        print("7. Sorting Nama")
        print("8. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_pasien(linkedlist, queue)

        elif pilih == "2":
            tampil_data(linkedlist)

        elif pilih == "3":
            cari_pasien(linkedlist)

        elif pilih == "4":
            update_pasien(linkedlist)

        elif pilih == "5":
            hapus_pasien(linkedlist)

        elif pilih == "6":
            panggil_antrian(queue)

        elif pilih == "7":
            sorting_nama(linkedlist)

        elif pilih == "8":
            print("Terima kasih")
            break

        else:
            print("Pilihan tidak valid")


menu()