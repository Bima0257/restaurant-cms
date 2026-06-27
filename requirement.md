# Requirement: CMS Restaurant — Secure Web Application
## 1. Pemetaan Role & Hak Akses

| **Role Aplikasi**              | **Hak Akses**                                                                                                                                                                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Super Admin**                | Full access ke seluruh sistem, termasuk pengelolaan user, role & permission, verifikasi akun, menu, kategori, recipe, bahan makanan, stok, audit penggunaan bahan, pesanan, laporan, pengaturan sistem, backup & restore database, serta audit log aktivitas pengguna.                           |
| **Admin / Restaurant Manager** | Mengelola operasional restoran, meliputi user, verifikasi akun, menu, kategori, recipe, bahan makanan, stok, pesanan, laporan, serta memonitor audit penggunaan bahan makanan. Tidak memiliki akses ke role & permission, pengaturan sistem, backup & restore database, maupun audit log sistem. |
| **Operator / Staff**           | Mengelola menu, kategori, meja, recipe, bahan makanan, memperbarui stok, memproses pesanan, dan memperbarui status pesanan. Dapat melihat riwayat penggunaan bahan berdasarkan transaksi, namun tidak dapat mengelola user, laporan, maupun pengaturan sistem.                                   |
| **Customer**                   | Registrasi dan login, melihat menu, melakukan pemesanan, melihat status serta riwayat pesanan miliknya, mengelola profil, dan memberikan ulasan.                                                                                                                                                 |

## 2. Fitur Wajib & Implementasi Teknis

### 2.1 Registrasi & Verifikasi Akun

- **Endpoint**: `POST /api/auth/register`
- Field: `nama_lengkap`, `username`, `email`, `password`, `confirm_password` — divalidasi dengan Kirim Kode OTP
- Password di-hash dengan `passlib` (`bcrypt`/`argon2`) — **jangan pernah simpan plain text**.
- Status akun: `belum_diverifikasi` | `aktif` | `nonaktif` (gunakan `Enum` di SQLAlchemy).
- Mekanisme verifikasi: token unik (UUID) dikirim via email **atau** diverifikasi manual oleh Admin lewat endpoint `PATCH /api/admin/users/{id}/verify`.
- Tabel pendukung: `verification_tokens` (token, user_id, expired_at, used).

### 2.2 Login dengan Google reCAPTCHA v2

Sistem autentikasi menggunakan **Google reCAPTCHA v2 (Checkbox)** sebagai mekanisme verifikasi untuk mencegah bot, brute force attack, dan penyalahgunaan proses login.

#### Frontend (Svelte)

- Menampilkan widget **Google reCAPTCHA v2 (Checkbox)** pada halaman login.
- Setelah pengguna berhasil melakukan verifikasi (termasuk image challenge apabila diperlukan oleh Google), frontend memperoleh token **`g-recaptcha-response`**.
- Token tersebut dikirim bersama data login ke backend melalui endpoint autentikasi.

#### Backend (FastAPI)

- **Endpoint:** `POST /api/auth/login`

  **Request Body**
  - `username/email`
  - `password`
  - `g-recaptcha-response`

- Backend melakukan validasi token reCAPTCHA menggunakan **Google reCAPTCHA Siteverify API** sebelum proses autentikasi pengguna.

- Login hanya diizinkan apabila:
  1. Token reCAPTCHA valid.
  2. Username/email dan password benar.
  3. Status akun **aktif**.

#### Rate Limiting

Untuk mengurangi risiko brute force attack, sistem menerapkan pembatasan percobaan login menggunakan middleware **SlowAPI** atau pencatatan kegagalan login pada tabel `login_attempts`.

Aturan yang diterapkan:

- Maksimal **5 kali percobaan login gagal**.
- Jika batas tercapai, akun dikunci selama **5 menit**.
- Durasi penguncian dihitung berdasarkan timestamp pada sisi backend.

#### Session Management

Setelah autentikasi berhasil, backend menghasilkan **JWT Access Token** dan **Refresh Token** yang digunakan sebagai kredensial autentikasi pada setiap permintaan API berikutnya.

#### Logout

- **Endpoint:** `POST /api/auth/logout`
- Backend melakukan invalidasi Refresh Token sehingga sesi pengguna tidak dapat digunakan kembali.

### 2.3 Verifikasi Email Menggunakan One-Time Password (OTP)

Sistem menerapkan verifikasi email menggunakan **One-Time Password (OTP)** untuk memastikan bahwa alamat email yang didaftarkan oleh pengguna valid dan dapat menerima email.

#### Alur Verifikasi

1. Pengguna melakukan registrasi dengan mengisi data yang diperlukan.
2. Backend menghasilkan **OTP acak sebanyak 6 digit**.
3. OTP disimpan pada database atau cache dengan waktu kedaluwarsa (**Time-To-Live/TTL**) selama **2 menit**.
4. Backend mengirimkan kode OTP ke alamat email pengguna menggunakan layanan **Resend Email API**.
5. Pengguna memasukkan kode OTP pada halaman verifikasi.
6. Backend memvalidasi kode OTP dan masa berlakunya.
7. Jika OTP valid, status akun diubah menjadi **Verified** sehingga pengguna dapat melakukan login.

#### Endpoint

**POST** `/api/auth/register`

Digunakan untuk melakukan registrasi akun baru dan mengirimkan OTP ke email pengguna.

**POST** `/api/auth/verify-email`

Digunakan untuk memverifikasi kode OTP.

**Request Body**

- `email`
- `otp_code`

**POST** `/api/auth/resend-otp`

Digunakan untuk mengirim ulang kode OTP apabila kode sebelumnya telah kedaluwarsa atau belum diterima.

**Request Body**

- `email`

#### Aturan Keamanan

- OTP terdiri dari **6 digit angka acak**.
- Masa berlaku OTP adalah **2 menit**.
- OTP hanya dapat digunakan **satu kali**.
- Pengguna dapat meminta pengiriman ulang OTP setelah **60 detik**.
- Maksimal **5 kali percobaan** memasukkan OTP yang salah.
- Jika batas percobaan tercapai, OTP dinyatakan tidak berlaku dan pengguna harus meminta OTP baru.

#### Implementasi

- **Frontend:** Svelte
- **Backend:** FastAPI
- **Email Service:** Resend
- **Format Email:** HTML Email Template
- **Status Akun:** `Pending Verification` → `Verified`

### 2.4 CRUD dengan Validasi dan Sanitasi Data

Seluruh fitur **Create, Read, Update, dan Delete (CRUD)** pada sistem menerapkan mekanisme validasi dan sanitasi data untuk menjaga integritas data serta mencegah serangan seperti SQL Injection, Cross-Site Scripting (XSS), dan pengiriman data yang tidak valid.

#### Validasi Data

Validasi dilakukan pada dua sisi, yaitu frontend dan backend.

**Frontend (Svelte)**

- Validasi form sebelum data dikirim ke server.
- Menampilkan pesan kesalahan (error message) secara langsung kepada pengguna.
- Melakukan validasi format email, panjang password, panjang karakter, serta field wajib (required).

**Backend (FastAPI)**

- Seluruh request divalidasi menggunakan **Pydantic Schema**.
- Memastikan tipe data, panjang karakter, format email, serta aturan bisnis (business rules) sesuai dengan ketentuan sistem.
- Data yang tidak memenuhi validasi akan ditolak dan mengembalikan respons **HTTP 422 (Unprocessable Entity)** atau **HTTP 400 (Bad Request)**.

#### Sanitasi Data

Sebelum data disimpan ke database, backend melakukan sanitasi terhadap data masukan untuk mengurangi risiko serangan keamanan.

Proses sanitasi meliputi:

- Menghapus spasi berlebih (trim whitespace).
- Validasi tipe data.
- Escape karakter khusus pada output yang ditampilkan kembali ke pengguna.
- Penggunaan parameterized query melalui ORM sehingga mencegah SQL Injection.
- Validasi tipe file, ukuran file, dan ekstensi pada proses upload gambar.

#### Hak Akses CRUD

Setiap operasi Create, Read, Update, dan Delete dibatasi menggunakan **Role-Based Access Control (RBAC)** sehingga pengguna hanya dapat mengakses data sesuai dengan hak akses yang dimiliki.

#### Audit Perubahan Data

Setiap perubahan data penting, seperti penambahan, perubahan, maupun penghapusan data master dan transaksi, dicatat pada **Audit Log** yang memuat informasi:

- Pengguna yang melakukan aksi.
- Jenis aktivitas (Create, Update, Delete).
- Waktu aktivitas.
- Modul yang diakses.
- Alamat IP pengguna (opsional).

#### Respon API

Seluruh endpoint CRUD menggunakan format respons JSON yang konsisten sehingga memudahkan integrasi antara frontend (Svelte) dan backend (FastAPI).

### 4.5 Keamanan terhadap SQL Injection

Sistem menerapkan mekanisme keamanan untuk mencegah serangan **SQL Injection**, yaitu teknik penyisipan perintah SQL berbahaya yang bertujuan memperoleh akses tidak sah, mengubah, atau menghapus data pada database.

#### Mekanisme Pencegahan

Pencegahan SQL Injection dilakukan melalui beberapa mekanisme berikut:

- Seluruh proses akses database menggunakan **SQLAlchemy ORM** atau **parameterized query**, sehingga input pengguna tidak digabungkan secara langsung ke dalam perintah SQL.
- Seluruh data masukan divalidasi menggunakan **Pydantic** sebelum diproses oleh backend.
- Data yang diterima disesuaikan dengan tipe data dan aturan bisnis yang telah ditentukan.
- Backend tidak menampilkan pesan kesalahan database secara langsung kepada pengguna untuk menghindari kebocoran informasi sistem.
- Hak akses terhadap endpoint dibatasi menggunakan **JWT Authentication** dan **Role-Based Access Control (RBAC)**.

#### Contoh Proses Aman

1. Pengguna mengirimkan data melalui frontend (Svelte).
2. Backend (FastAPI) melakukan validasi menggunakan Pydantic.
3. Data yang valid diproses menggunakan SQLAlchemy ORM atau parameterized query.
4. Database mengeksekusi query tanpa menggabungkan input pengguna secara langsung ke dalam sintaks SQL.

Dengan mekanisme tersebut, masukan seperti karakter khusus atau pola SQL Injection akan diperlakukan sebagai **nilai (value)**, bukan sebagai bagian dari perintah SQL.

#### Pengujian

Pengujian dilakukan dengan memasukkan pola SQL Injection pada beberapa form, seperti halaman login dan pencarian data, misalnya:

- `' OR '1'='1`
- `' UNION SELECT ...`
- `admin' --`

Hasil pengujian menunjukkan bahwa sistem menolak input yang tidak valid dan tidak menjalankan perintah SQL yang disisipkan, sehingga autentikasi dan proses CRUD tetap berjalan secara aman.

### 4.6 Sanitasi Output (Perlindungan terhadap Cross-Site Scripting/XSS)

Sistem menerapkan mekanisme sanitasi output untuk mencegah serangan **Cross-Site Scripting (XSS)**, yaitu serangan yang menyisipkan skrip berbahaya ke dalam data yang kemudian ditampilkan kepada pengguna.

#### Mekanisme Pencegahan

Perlindungan terhadap XSS diterapkan melalui beberapa mekanisme berikut:

- Seluruh data yang ditampilkan pada antarmuka diperlakukan sebagai **teks biasa (plain text)**, bukan sebagai kode HTML.
- Frontend (Svelte) menggunakan mekanisme rendering bawaan yang melakukan **escaping** terhadap karakter khusus sehingga script yang disisipkan tidak dieksekusi oleh browser.
- Penggunaan HTML mentah (`{@html}`) hanya dilakukan apabila benar-benar diperlukan dan hanya pada data yang telah melalui proses sanitasi.
- Backend (FastAPI) melakukan validasi terhadap data masukan serta membatasi jenis data yang dapat disimpan sesuai kebutuhan sistem.
- Data yang berasal dari pengguna tidak digunakan secara langsung pada atribut HTML, URL, maupun JavaScript tanpa proses validasi terlebih dahulu.

#### Contoh Pengujian

Pengujian dilakukan dengan memasukkan payload XSS pada beberapa field input, seperti nama menu, kategori, dan deskripsi.

Contoh payload:

```text
<script>alert('XSS')</script>
```

```text
<img src="x" onerror="alert('XSS')">
```

```text
<svg onload="alert('XSS')"></svg>
```

Hasil pengujian menunjukkan bahwa payload ditampilkan sebagai teks biasa atau ditolak sesuai aturan validasi, sehingga skrip tidak dieksekusi oleh browser dan aplikasi tetap berjalan dengan aman.

#### Manfaat

Penerapan sanitasi output memberikan beberapa manfaat, antara lain:

- Mencegah eksekusi JavaScript berbahaya.
- Melindungi cookie dan token autentikasi dari pencurian melalui XSS.
- Menjaga integritas tampilan antarmuka pengguna.
- Meningkatkan keamanan data pengguna dan sistem secara keseluruhan.

### 4.7 Laporan dengan Watermark

Sistem menyediakan fitur pembuatan laporan dalam format **PDF** yang dilengkapi dengan **watermark perusahaan** sebagai identitas dokumen dan upaya perlindungan terhadap penyalahgunaan atau distribusi dokumen tanpa izin.

#### Jenis Laporan

Sistem dapat menghasilkan beberapa jenis laporan, antara lain:

- Laporan Penjualan
- Laporan Pesanan
- Laporan Stok Bahan Makanan
- Laporan Penggunaan Bahan (Recipe Usage)
- Laporan Menu Terlaris
- Laporan Aktivitas Pengguna (Audit Log)

#### Watermark Dokumen

Setiap laporan PDF yang dihasilkan sistem akan menampilkan watermark berupa:

- Logo perusahaan
- Nama restoran
- Tulisan "Confidential" atau "Internal Use Only" (opsional)

Watermark ditempatkan di bagian tengah halaman dengan tingkat transparansi tertentu sehingga tidak mengganggu keterbacaan isi laporan.

#### Proses Pembuatan Laporan

1. Pengguna memilih jenis laporan dan rentang tanggal.
2. Backend (FastAPI) mengambil data dari database.
3. Sistem menghasilkan dokumen PDF secara otomatis.
4. Watermark perusahaan ditambahkan pada setiap halaman laporan.
5. File PDF dikirim ke pengguna untuk diunduh atau dicetak.

#### Hak Akses

Pembuatan dan pengunduhan laporan dibatasi berdasarkan Role-Based Access Control (RBAC):

- Super Admin : Akses seluruh laporan
- Admin / Restaurant Manager : Akses laporan operasional dan bisnis
- Operator / Staff : Hanya dapat melihat laporan tertentu sesuai kewenangan
- Customer : Tidak memiliki akses laporan internal

#### Manfaat

Penerapan watermark pada laporan memberikan beberapa manfaat:

- Menunjukkan identitas resmi perusahaan.
- Mengurangi risiko penyalahgunaan dokumen.
- Memudahkan identifikasi sumber laporan.
- Meningkatkan profesionalisme dokumen yang dihasilkan sistem.

### 4.8 Backup dan Restore Database

Sistem menyediakan fitur **Backup** dan **Restore Database** untuk menjaga ketersediaan data serta mendukung proses pemulihan apabila terjadi kerusakan sistem, kehilangan data, atau kesalahan operasional.

#### Backup Database

Fitur backup digunakan untuk membuat salinan (backup) seluruh data database ke dalam sebuah file yang dapat disimpan sebagai cadangan.

Proses backup dilakukan sebagai berikut:

1. Super Admin memilih menu **Backup Database**.
2. Backend (FastAPI) menghasilkan file backup database.
3. File backup disimpan pada server dan dapat diunduh oleh Super Admin.
4. Sistem mencatat aktivitas backup pada Audit Log.

#### Restore Database

Fitur restore digunakan untuk mengembalikan database menggunakan file backup yang telah dibuat sebelumnya.

Proses restore dilakukan sebagai berikut:

1. Super Admin mengunggah file backup database.
2. Backend melakukan validasi format file backup.
3. Sistem melakukan proses restore database.
4. Setelah proses berhasil, sistem mencatat aktivitas restore pada Audit Log.

#### Hak Akses

Fitur Backup dan Restore Database hanya dapat diakses oleh **Super Admin**.

#### Keamanan

Untuk menjaga keamanan data, sistem menerapkan beberapa mekanisme berikut:

- Hanya pengguna dengan hak akses **Super Admin** yang dapat melakukan backup maupun restore.
- File backup divalidasi sebelum proses restore dilakukan.
- Seluruh aktivitas backup dan restore dicatat pada Audit Log.
- Sistem menampilkan konfirmasi sebelum proses restore dijalankan karena proses ini berpotensi menimpa data yang ada.

#### Manfaat

Penerapan fitur backup dan restore memberikan beberapa manfaat, antara lain:

- Mengurangi risiko kehilangan data.
- Mempermudah proses pemulihan sistem setelah terjadi kegagalan.
- Mendukung kontinuitas operasional aplikasi.
- Menjamin ketersediaan data apabila terjadi kesalahan konfigurasi atau kerusakan database.

### 4.10 Proteksi Folder Backup

- Simpan file backup **di luar** folder yang di-serve sebagai static/public (misal `storage/backups/` di luar `app/static/`, **tidak boleh** di folder yang diexpose lewat StaticFiles FastAPI).
- Jika terpaksa di dalam project, tambahkan pengecekan akses lewat endpoint terotentikasi saja (tidak ada direct static route ke folder tersebut).

### 4.9 Audit Log Aktivitas

Sistem menyediakan fitur **Audit Log Aktivitas** untuk mencatat seluruh aktivitas penting yang dilakukan oleh pengguna. Fitur ini bertujuan meningkatkan keamanan, akuntabilitas, serta memudahkan proses monitoring dan investigasi apabila terjadi kesalahan atau penyalahgunaan sistem.

#### Aktivitas yang Dicatat

Audit Log mencatat berbagai aktivitas penting, antara lain:

- Login berhasil.
- Login gagal.
- Logout.
- Registrasi akun.
- Verifikasi email menggunakan OTP.
- Perubahan profil pengguna.
- Penambahan data (Create).
- Perubahan data (Update).
- Penghapusan data (Delete).
- Backup database.
- Restore database.
- Perubahan hak akses pengguna.
- Aktivitas penting lainnya yang memengaruhi data sistem.

#### Informasi yang Disimpan

Setiap log aktivitas menyimpan informasi berikut:

- ID Log
- Nama pengguna
- Role pengguna
- Jenis aktivitas
- Modul yang diakses
- Deskripsi aktivitas
- Waktu aktivitas (timestamp)
- Alamat IP pengguna
- User Agent (browser/perangkat)

#### Hak Akses

Audit Log hanya dapat diakses oleh:

- **Super Admin** : Melihat seluruh aktivitas pengguna.
- **Admin / Restaurant Manager** : Melihat aktivitas operasional sesuai kewenangannya.
- **Operator / Staff** : Tidak memiliki akses.
- **Customer** : Tidak memiliki akses.

#### Proses Pencatatan

Setiap kali pengguna melakukan aktivitas penting, backend (FastAPI) secara otomatis menyimpan informasi aktivitas ke dalam tabel `audit_logs`.

Pencatatan dilakukan tanpa memerlukan interaksi tambahan dari pengguna sehingga seluruh aktivitas dapat ditelusuri kembali apabila diperlukan.

#### Manfaat

Penerapan Audit Log memberikan beberapa manfaat, antara lain:

- Memantau aktivitas seluruh pengguna.
- Mempermudah proses investigasi apabila terjadi penyalahgunaan sistem.
- Mengetahui riwayat perubahan data.
- Meningkatkan keamanan dan transparansi sistem.
- Mendukung proses audit operasional restoran.

#### Contoh Data Audit Log

| Waktu            | Pengguna | Role        | Modul          | Aktivitas                              |
| ---------------- | -------- | ----------- | -------------- | -------------------------------------- |
| 26-06-2026 09:15 | admin    | Super Admin | Authentication | Login berhasil                         |
| 26-06-2026 09:20 | manager  | Admin       | Menu           | Menambahkan menu "Nasi Goreng Spesial" |
| 26-06-2026 09:45 | operator | Operator    | Pesanan        | Memperbarui status pesanan             |
| 26-06-2026 10:30 | admin    | Super Admin | Database       | Backup database                        |
| 26-06-2026 11:00 | admin    | Super Admin | Database       | Restore database                       |

### Session Timeout

Sistem menerapkan **Session Timeout** untuk mengurangi risiko penyalahgunaan akun apabila pengguna meninggalkan aplikasi dalam keadaan masih login.

#### Mekanisme Session

Sistem menggunakan autentikasi berbasis **JSON Web Token (JWT)** yang terdiri dari:

- **Access Token** sebagai token utama untuk mengakses API.
- **Refresh Token** untuk memperoleh Access Token baru setelah masa berlaku Access Token berakhir.

#### Aturan Session Timeout

- Access Token memiliki masa berlaku **15 menit**.
- Refresh Token memiliki masa berlaku **7 hari**.
- Setelah Access Token kedaluwarsa, frontend (Svelte) akan menggunakan Refresh Token untuk meminta Access Token baru kepada backend (FastAPI).
- Apabila Refresh Token telah kedaluwarsa atau tidak valid, pengguna diwajibkan melakukan login kembali.

#### Idle Session

Untuk meningkatkan keamanan, sistem juga menerapkan **Idle Session Timeout**.

- Jika tidak terdapat aktivitas pengguna selama **30 menit**, frontend secara otomatis mengakhiri sesi pengguna.
- Pengguna akan diarahkan kembali ke halaman login dan diminta melakukan autentikasi ulang.

#### Logout

Saat pengguna melakukan logout:

- Access Token dihapus dari sisi client.
- Refresh Token diinvalidasi oleh backend.
- Seluruh permintaan API menggunakan token tersebut tidak dapat digunakan kembali.

#### Keamanan

Penerapan Session Timeout memberikan beberapa manfaat, antara lain:

- Mengurangi risiko akses tidak sah akibat sesi yang ditinggalkan.
- Melindungi akun pengguna pada perangkat bersama.
- Memastikan setiap akses ke sistem menggunakan token yang masih valid.
- Mendukung mekanisme autentikasi berbasis JWT yang lebih aman.

#### Hak Akses

Session Timeout diterapkan pada seluruh pengguna yang telah berhasil melakukan autentikasi, yaitu:

- Super Admin
- Admin / Restaurant Manager
- Operator / Staff
- Customer

### 4.11 Proteksi Password

Sistem menerapkan mekanisme proteksi password untuk menjaga kerahasiaan kredensial pengguna dan mengurangi risiko penyalahgunaan akun apabila terjadi kebocoran data.

#### Hashing Password

Password pengguna tidak disimpan dalam bentuk teks biasa (_plain text_). Sebelum disimpan ke database, password diproses menggunakan algoritma hashing yang aman, seperti **Argon2** (direkomendasikan) atau **bcrypt**.

Dengan mekanisme ini, password asli tidak dapat diketahui kembali meskipun database berhasil diakses oleh pihak yang tidak berwenang.

#### Kebijakan Password

Untuk meningkatkan keamanan akun, sistem menerapkan ketentuan sebagai berikut:

- Minimal terdiri dari **8 karakter**.
- Mengandung minimal **1 huruf besar (A–Z)**.
- Mengandung minimal **1 huruf kecil (a–z)**.
- Mengandung minimal **1 angka (0–9)**.
- Mengandung minimal **1 karakter khusus** (misalnya `@`, `#`, `!`, `%`, `&`).
- Tidak boleh sama dengan username atau alamat email.

#### Verifikasi Password

Saat proses login, password yang dimasukkan pengguna tidak dibandingkan secara langsung dengan data pada database. Backend melakukan proses verifikasi menggunakan fungsi pemeriksaan hash sehingga password asli tidak pernah ditampilkan maupun dikirim kembali.

#### Perubahan Password

Saat pengguna mengganti password, sistem menerapkan proses berikut:

1. Memverifikasi password lama.
2. Memastikan password baru memenuhi kebijakan keamanan.
3. Menghasilkan hash baru untuk password.
4. Menyimpan hash baru ke database.
5. Mencatat aktivitas perubahan password pada Audit Log.

#### Keamanan

Proteksi password memberikan beberapa manfaat, antara lain:

- Mencegah penyimpanan password dalam bentuk teks biasa.
- Mengurangi risiko pencurian kredensial apabila database mengalami kebocoran.
- Mendukung praktik keamanan autentikasi modern.
- Meningkatkan keamanan akun pengguna.

#### Hak Akses

Fitur proteksi password diterapkan pada seluruh akun pengguna, yaitu:

- Super Admin
- Admin / Restaurant Manager
- Operator / Staff
- Customer

### 4.12 Error Handling Aman

Sistem menerapkan mekanisme **Error Handling Aman** untuk mencegah kebocoran informasi sensitif apabila terjadi kesalahan selama proses eksekusi aplikasi. Informasi teknis hanya dicatat pada server, sedangkan pengguna menerima pesan kesalahan yang bersifat umum.

#### Mekanisme Penanganan Error

Backend (FastAPI) menggunakan mekanisme **Exception Handling** untuk menangani berbagai jenis kesalahan yang terjadi selama proses permintaan (request).

Apabila terjadi kesalahan, sistem akan:

- Mengembalikan kode status HTTP yang sesuai.
- Menampilkan pesan yang mudah dipahami oleh pengguna.
- Tidak menampilkan detail implementasi seperti query SQL, struktur database, path file, maupun stack trace.
- Mencatat informasi teknis ke dalam log server untuk kebutuhan pemeliharaan dan debugging.

#### Kategori Error

Sistem menangani beberapa kategori kesalahan, antara lain:

- **400 Bad Request** – Permintaan tidak valid.
- **401 Unauthorized** – Pengguna belum melakukan autentikasi.
- **403 Forbidden** – Pengguna tidak memiliki hak akses.
- **404 Not Found** – Data atau endpoint tidak ditemukan.
- **422 Unprocessable Entity** – Validasi data gagal.
- **500 Internal Server Error** – Terjadi kesalahan pada server.

#### Respon Error

Seluruh endpoint API mengembalikan format respons JSON yang konsisten sehingga memudahkan integrasi dengan frontend (Svelte).

Contoh struktur respons:

```json
{
  "success": false,
  "message": "Terjadi kesalahan saat memproses permintaan.",
  "errors": null
}
```

Untuk kesalahan validasi, sistem dapat mengembalikan informasi field yang bermasalah tanpa mengungkapkan detail internal server.

#### Logging

Informasi teknis yang dicatat pada server meliputi:

- Waktu kejadian.
- Endpoint yang diakses.
- Metode HTTP.
- ID pengguna (apabila telah login).
- Alamat IP pengguna.
- Jenis exception.
- Detail error untuk kebutuhan debugging.

#### Manfaat

Penerapan Error Handling Aman memberikan beberapa manfaat, antara lain:

- Mencegah kebocoran informasi internal sistem.
- Mengurangi risiko eksploitasi oleh pihak yang tidak berwenang.
- Memudahkan proses monitoring dan debugging.
- Memberikan pengalaman pengguna yang lebih baik melalui pesan kesalahan yang konsisten.

### 4.13 Validasi Upload File

Sistem menerapkan mekanisme **Validasi Upload File** untuk memastikan bahwa file yang diunggah memenuhi persyaratan keamanan dan hanya file yang valid yang dapat disimpan pada server.

#### Jenis File

Sistem hanya mengizinkan jenis file gambar yang digunakan pada beberapa fitur, seperti:

- Foto profil pengguna.
- Gambar menu.
- Gambar kategori.
- Logo restoran.

Format file yang diperbolehkan:

- JPG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

#### Validasi File

Sebelum file disimpan ke server, backend (FastAPI) melakukan beberapa proses validasi, yaitu:

- Memastikan file telah dipilih.
- Memeriksa ekstensi file yang diperbolehkan.
- Memverifikasi MIME Type file.
- Membatasi ukuran file maksimum (misalnya **2 MB**).
- Menghasilkan nama file yang unik untuk menghindari konflik nama.
- Menolak file yang tidak memenuhi ketentuan.

#### Penyimpanan File

Setelah proses validasi berhasil, sistem akan:

1. Menghasilkan nama file yang unik menggunakan UUID atau timestamp.
2. Menyimpan file pada direktori penyimpanan server.
3. Menyimpan informasi lokasi file ke dalam database.
4. Menghapus file lama apabila pengguna melakukan pembaruan gambar.

#### Keamanan

Untuk meningkatkan keamanan proses upload, sistem menerapkan mekanisme berikut:

- Tidak menggunakan nama file asli sebagai nama penyimpanan.
- Tidak mengizinkan upload file executable atau script.
- Memvalidasi MIME Type dan ekstensi file.
- Membatasi ukuran file untuk mencegah penyalahgunaan penyimpanan.
- Menyimpan file di direktori yang telah ditentukan dan tidak mengizinkan eksekusi file yang diunggah.

#### Validasi Frontend

Frontend (Svelte) melakukan validasi awal untuk meningkatkan pengalaman pengguna, meliputi:

- Menampilkan pratinjau (preview) gambar.
- Memeriksa ukuran file sebelum dikirim.
- Memeriksa format file yang dipilih.
- Menampilkan pesan kesalahan apabila file tidak memenuhi ketentuan.

Validasi pada frontend tidak menggantikan validasi pada backend, melainkan berfungsi sebagai pemeriksaan awal.

#### Manfaat

Penerapan validasi upload file memberikan beberapa manfaat, antara lain:

- Mencegah upload file yang tidak sesuai.
- Mengurangi risiko upload file berbahaya.
- Menjaga konsistensi format file pada sistem.
- Meningkatkan keamanan dan efisiensi penyimpanan file.

