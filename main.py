import streamlit as st
import json
import os
from datetime import date, datetime

# ==========================================
# 1. KONFIGURASI & VARIABEL GLOBAL
# ==========================================
st.set_page_config(layout="wide", page_title="My Life Tracker")
FILE_JSON = 'data.json'
today = date.today()
now = datetime.now()
format_waktu = now.strftime('%H:%M')
today_str = today.strftime('%Y-%m-%d')

# ==========================================
# 2. OTAK APLIKASI (BACKEND LOGIC)
# ==========================================

def load_data():
    """Memuat data JSON. Pastikan semua kategori ada."""
    default_data = {
        "last_opened": str(today),
        "daily": {}, 
        "exercise": {"type": "Rest", "done": False},
        "quran": {"surat": "", "ayat": "", "last_updated": "-"},
        "buku":  {"judul": "", "halaman": "", "last_updated": "-"},
        "money":  {"masuk": "", "keluar": "", "last_updated": "-"}, # Input Harian Cash
        "bank":   {"income": "", "tarik": "", "last_updated": "-"},  # Input Harian Bank
        "savings": {"cash": 0, "bank": 0},      # Saldo Total (Akumulasi)
        "finance_history": [],                  # <--- TABEL RIWAYAT TRANSAKSI
        "daftar_matkul": [], 
        "kuliah": {}, 
        "others": [],
        "hafalan": {},
        "memos": []   
    }

    if not os.path.exists(FILE_JSON):
        return default_data
    
    with open(FILE_JSON, 'r') as f:
        try:
            data = json.load(f)
        except:
            return default_data 
        
        # --- LOGIKA RESET HARIAN ---
        if data.get("last_opened") != str(today):
            data["daily"] = {k: False for k in data.get("daily", {})} 
            data["exercise"] = {"type": "Rest", "done": False}
            data["last_opened"] = str(today)
            
            with open(FILE_JSON, 'w') as f_write:
                json.dump(data, f_write, indent=4)
            st.toast("🔄 Hari baru! Daily routine di-reset.")

        # --- RECOVERY ---
        for key in default_data:
            if key not in data:
                data[key] = default_data[key]
            
        return data

def save_data():
    with open(FILE_JSON, 'w') as f:
        json.dump(st.session_state.db, f, indent=4)

# --- FUNGSI UPDATE UMUM ---
def update_text(kategori, jenis_input, specific_key):
    nilai_baru = st.session_state[specific_key]
    st.session_state.db[kategori][jenis_input] = nilai_baru
    st.session_state.db[kategori]['last_updated'] = today.strftime('%d %B %Y')
    save_data()

def toggle_check(category, item_name):
    widget_key = f"chk_{category}_{item_name}"
    if category not in st.session_state.db: st.session_state.db[category] = {}
    st.session_state.db[category][item_name] = st.session_state[widget_key]
    save_data()

# --- FUNGSI MANAJEMEN MATKUL ---
def add_new_matkul():
    nama_baru = st.session_state.input_new_matkul
    if nama_baru:
        if nama_baru not in st.session_state.db["daftar_matkul"]:
            st.session_state.db["daftar_matkul"].append(nama_baru)
            st.session_state.db["kuliah"][nama_baru] = {} 
            st.session_state.input_new_matkul = "" 
            save_data()
            st.toast(f"✅ Matkul {nama_baru} berhasil ditambah!")
        else:
            st.toast("⚠️ Nama Matkul sudah ada!")

def delete_matkul(nama_matkul):
    if nama_matkul in st.session_state.db["daftar_matkul"]:
        st.session_state.db["daftar_matkul"].remove(nama_matkul)
        if nama_matkul in st.session_state.db["kuliah"]:
            del st.session_state.db["kuliah"][nama_matkul]
        save_data()
        st.rerun()

# --- FUNGSI TUGAS KULIAH ---
def add_kuliah_task(matkul):
    input_key = f"new_task_kuliah_{matkul}"
    task_text = st.session_state[input_key]
    if task_text:
        if matkul not in st.session_state.db["kuliah"]:
            st.session_state.db["kuliah"][matkul] = {}
        st.session_state.db["kuliah"][matkul][task_text] = False
        st.session_state[input_key] = ""
        save_data()

def delete_kuliah_task(matkul, task_name):
    if task_name in st.session_state.db["kuliah"][matkul]:
        del st.session_state.db["kuliah"][matkul][task_name]
        save_data()
        st.rerun()

def toggle_kuliah(matkul, task_name):
    widget_key = f"chk_kuliah_{matkul}_{task_name}"
    st.session_state.db["kuliah"][matkul][task_name] = st.session_state[widget_key]
    save_data()

# --- FUNGSI KHUSUS OTHERS ---
def add_other_task():
    task = st.session_state.new_task_input
    if task:
        st.session_state.db['others'].append({"task": task, "done": False})
        st.session_state.new_task_input = "" 
        save_data()

def toggle_other(index):
    widget_key = f"chk_others_{index}"
    st.session_state.db['others'][index]['done'] = st.session_state[widget_key]
    save_data()

def delete_other_task(index):
    st.session_state.db['others'].pop(index)
    save_data()
    st.rerun()

# --- FUNGSI MEMO / NOTES ---
def add_new_memo():
    judul = st.session_state.in_memo_judul
    isi = st.session_state.in_memo_isi
    
    if judul or isi:
        item_baru = {
            "title": judul,
            "content": isi,
            "date": today.strftime('%d/%m/%Y')
        }
        # Insert di index 0 biar paling atas
        st.session_state.db['memos'].insert(0, item_baru)
        
        # Reset Input
        st.session_state.in_memo_judul = ""
        st.session_state.in_memo_isi = ""
        save_data()
        st.toast("✅ Catatan tersimpan!")

def delete_memo(index):
    st.session_state.db['memos'].pop(index)
    save_data()
    st.rerun()

# --- FUNGSI FINANCE (TUTUP BUKU & HISTORY) ---
def tutup_buku():
    """Memindahkan transaksi hari ini ke History & update saldo."""
    
    # 1. Ambil Angka Hari Ini
    cash_in = int(st.session_state.db['money']['masuk'] or 0)
    cash_out = int(st.session_state.db['money']['keluar'] or 0)
    bank_in = int(st.session_state.db['bank']['income'] or 0)
    bank_out = int(st.session_state.db['bank']['tarik'] or 0)
    
    # Cek: Kalau semua 0, jangan disimpan (ngotorin history)
    if (cash_in + cash_out + bank_in + bank_out) == 0:
        st.toast("⚠️ Data masih kosong, tidak ada yang perlu ditutup.")
        return

    # 2. Update Saldo Utama (Savings)
    net_cash = cash_in - cash_out
    net_bank = bank_in - bank_out
    
    st.session_state.db['savings']['cash'] += net_cash
    st.session_state.db['savings']['bank'] += net_bank
    
    # 3. BUAT CATATAN HISTORI BARU (Ini yang kamu minta!)
    new_record = {
        "date": today.strftime('%d/%m/%Y'),
        "timestamp": datetime.now().strftime('%H:%M'),
        "cash_in": cash_in,
        "cash_out": cash_out,
        "bank_in": bank_in,
        "bank_out": bank_out,
        "balance_after": st.session_state.db['savings']['cash'] + st.session_state.db['savings']['bank']
    }
    
    # Masukkan ke list history (Paling atas = paling baru)
    st.session_state.db['finance_history'].insert(0, new_record)

    # 4. Reset Inputan Hari Ini
    st.session_state.db['money']['masuk'] = ""
    st.session_state.db['money']['keluar'] = ""
    st.session_state.db['bank']['income'] = ""
    st.session_state.db['bank']['tarik'] = ""
    
    st.session_state.db['money']['last_updated'] = today.strftime('%d %B %Y')
    save_data()
    st.toast("✅ Tutup buku berhasil! Data masuk history.")
    st.rerun()

def delete_history_finance(index):
    # Hapus history tapi TIDAK mengembalikan saldo (hanya hapus catatan)
    # Atau mau mengembalikan saldo? Untuk simpelnya, hapus catatan saja dulu.
    st.session_state.db['finance_history'].pop(index)
    save_data()
    st.rerun()

# ==========================================
# 3. INISIALISASI STATE
# ==========================================
if 'db' not in st.session_state:
    st.session_state.db = load_data()

if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

def set_page(nama_halaman):
    st.session_state.page = nama_halaman

# ==========================================
# 4. SIDEBAR (NAVIGASI)
# ==========================================
st.sidebar.title("My To Do App")
st.sidebar.image("cat_bg.jpg",caption="powered by Cips<3", width=160) 
st.sidebar.markdown("### 💈 **Check Berkala:**")

# Tombol Navigasi
st.sidebar.button("📝 To Do List", on_click=set_page, args=("dashboard",), type="primary" if st.session_state.page == "dashboard" else "secondary")
st.sidebar.button("⏰ History Bacaan", on_click=set_page, args=("history",), type="primary" if st.session_state.page == "history" else "secondary")
st.sidebar.button("📖 Juz Amma", on_click=set_page, args=("hafalan",), type="primary" if st.session_state.page == "hafalan" else "secondary")
st.sidebar.button("💵 Financial", on_click=set_page, args=("finance",), type="primary" if st.session_state.page == "finance" else "secondary")
st.sidebar.button("📒 My Notes", on_click=set_page, args=("note",), type="primary" if st.session_state.page == "note" else "secondary")

st.sidebar.markdown("---")
st.sidebar.title("Pengaturan")
if st.sidebar.button("🗑️ RESET SEMESTER"):
    st.session_state.db["daftar_matkul"] = [] 
    st.session_state.db["kuliah"] = {}       
    st.session_state.db["others"] = []
    st.session_state.db["memos"] = [] 
    st.session_state.db["finance_history"] = [] # Reset history keuangan juga
    st.session_state.db["savings"] = {"cash": 0, "bank": 0} # Reset saldo nol
    st.session_state.db["daily"] = {k: False for k in st.session_state.db["daily"]}
    st.session_state.db["exercise"]["done"] = False
    st.session_state.db["hafalan"] = {} 
    save_data()
    st.rerun()

# ==========================================
# 5. LOGIKA TAMPILAN HALAMAN
# ==========================================

# >>> HALAMAN 1: DASHBOARD
if st.session_state.page == "dashboard":
    c_title, c_time = st.columns([0.7, 0.3])
    with c_title:
        st.title(f"📝 My Dashboard")
        st.markdown(f"### <span style='color:blue'>{today.strftime('%d %B %Y')}</span>", unsafe_allow_html=True)
    with c_time:
        st.markdown(f"<h1 style='text-align: right; color: gray;'>{format_waktu}</h1>", unsafe_allow_html=True)
    st.divider()

    daily_col, kuliah_col, other_col = st.columns(3)

    # --- KOLOM 1: DAILY ---
    with daily_col:
        st.markdown(f"## <span style='color:green'>Daily</span>", unsafe_allow_html=True)
        def render_daily_group(title, items):
            c1, c2 = st.columns([0.4, 0.6])
            with c1: st.markdown(f"##### {title}")
            with c2:
                for item in items:
                    val = st.session_state.db['daily'].get(item, False)
                    st.checkbox(item, value=val, key=f"chk_daily_{item}", on_change=toggle_check, args=("daily", item))
            st.divider()

        render_daily_group("Ibadah", ["Subuh", "Dhuhur", "Ashar", "Maghrib", "Isha"])
        render_daily_group("Rumah", ["Sapu Lantai", "Buang Sampah", "Cuci Piring", "Cuci Baju"])
        render_daily_group("Diri", ["Mandi", "Skin Care Pagi", "Skin Care Malam"])
        render_daily_group("Daily Intake", ["Makan Pagi", "Makan Siang", "Makan Malam", "Creatine"])

        # Exercise
        st.markdown("##### Exercise")
        saved_ex = st.session_state.db['exercise']
        c_ex1, c_ex2 = st.columns([0.7, 0.3])
        with c_ex1:
            new_type = st.selectbox("Jenis", ["Rest", "Push", "Pull", "Legs", "Push-Pull", "Full-Body", "Cardio"], 
                                   index=["Rest", "Push", "Pull", "Legs", "Push-Pull", "Full-Body", "Cardio"].index(saved_ex.get('type', 'Rest')),
                                   label_visibility="collapsed")
            if new_type != saved_ex.get('type'):
                st.session_state.db['exercise']['type'] = new_type
                save_data()
                st.rerun()
        with c_ex2:
            val_ex = saved_ex.get('done', False)
            if st.checkbox("Done", value=val_ex, key="chk_ex_done"):
                 st.session_state.db['exercise']['done'] = True
                 save_data()
            else:
                 if val_ex: 
                     st.session_state.db['exercise']['done'] = False
                     save_data()
        st.divider()
        
        def render_tracker(title, cat, fields):
            st.markdown(f"##### {title}")
            for f, label in fields.items():
                widget_id = f"input_{cat}_{f}"
                st.text_input(label, value=st.session_state.db[cat][f], 
                              key=widget_id, 
                              on_change=update_text, 
                              args=(cat, f, widget_id))
        
        render_tracker("📖 Quran", "quran", {"surat": "Surat", "ayat": "Ayat"})
        render_tracker("📚 Buku", "buku", {"judul": "Judul", "halaman": "Halaman"})

    # --- KOLOM 2: KULIAH ---
    with kuliah_col:
        st.markdown(f"## <span style='color:red'>Kuliah</span>", unsafe_allow_html=True)
        c_add_mk, c_btn_mk = st.columns([0.8, 0.2])
        with c_add_mk:
            st.text_input("Buat Matkul Baru:", placeholder="Nama Matkul (Contoh: Alpro)", 
                          key="input_new_matkul", label_visibility="collapsed")
        with c_btn_mk:
            st.button("➕", help="Tambah Matkul", on_click=add_new_matkul)
        st.divider()

        if not st.session_state.db["daftar_matkul"]:
            st.info("Belum ada mata kuliah. Tambahkan di atas! 👆")

        for matkul in st.session_state.db["daftar_matkul"]:
            c_head, c_del_mk = st.columns([0.85, 0.15])
            with c_head: st.markdown(f"### **{matkul}**")
            with c_del_mk:
                if st.button("🗑️", key=f"del_mk_{matkul}", help=f"Hapus Matkul {matkul}"):
                    delete_matkul(matkul)

            if matkul not in st.session_state.db["kuliah"]:
                st.session_state.db["kuliah"][matkul] = {}

            st.text_input("Tambah", label_visibility="collapsed", placeholder=f"+ Tugas {matkul}...",
                key=f"new_task_kuliah_{matkul}", on_change=add_kuliah_task, args=(matkul,)
            )

            tasks = list(st.session_state.db["kuliah"][matkul].items())
            if not tasks: st.caption("Belum ada tugas.")
            
            for task_name, is_done in tasks:
                c_chk, c_del = st.columns([0.85, 0.15])
                with c_chk:
                    st.checkbox(task_name, value=is_done, key=f"chk_kuliah_{matkul}_{task_name}",
                        on_change=toggle_kuliah, args=(matkul, task_name))
                with c_del:
                    if st.button("✖", key=f"del_kul_{matkul}_{task_name}"):
                        delete_kuliah_task(matkul, task_name)
            st.divider()

    # --- KOLOM 3: LAINNYA ---
    with other_col:
        st.markdown(f"## <span style='color:blue'>Lainnya</span>", unsafe_allow_html=True)
        st.text_input("Tambah", label_visibility="collapsed", placeholder="+ Beli galon...", 
                      key="new_task_input", on_change=add_other_task)
        st.subheader("List:")
        if st.session_state.db['others']:
            for i, item in enumerate(st.session_state.db['others']):
                c_chk, c_del = st.columns([0.85, 0.15])
                with c_chk:
                    st.checkbox(item['task'], value=item['done'], key=f"chk_others_{i}",
                        on_change=toggle_other, args=(i,))
                with c_del:
                    if st.button("✖", key=f"del_other_{i}"):
                        delete_other_task(i)
        else:
            st.info("Kosong.")

# >>> HALAMAN 2: HISTORY BACAAN
elif st.session_state.page == "history":
    st.title("⏰ History & Progress Bacaan")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📖 Al-Quran")
        quran_data = st.session_state.db['quran']
        st.info(f"**Terakhir Update:** {quran_data['last_updated']}")
        m1, m2 = st.columns(2)
        m1.metric("Surat", quran_data['surat'] if quran_data['surat'] else "-")
        m2.metric("Ayat", quran_data['ayat'] if quran_data['ayat'] else "-")
        st.markdown("#### Update Cepat:")
        st.text_input("Update Surat:", value=quran_data['surat'], key="hist_q_surat", 
                      on_change=update_text, args=("quran", "surat", "hist_q_surat"))
        st.text_input("Update Ayat:", value=quran_data['ayat'], key="hist_q_ayat", 
                      on_change=update_text, args=("quran", "ayat", "hist_q_ayat"))
    with col2:
        st.markdown("### 📚 Buku")
        buku_data = st.session_state.db['buku']
        st.info(f"**Terakhir Update:** {buku_data['last_updated']}")
        b1, b2 = st.columns(2)
        b1.metric("Judul Buku", buku_data['judul'] if buku_data['judul'] else "-")
        b2.metric("Halaman Terakhir", buku_data['halaman'] if buku_data['halaman'] else "-")
        st.markdown("#### Update Cepat:")
        st.text_input("Update Judul:", value=buku_data['judul'], key="hist_b_judul", 
                      on_change=update_text, args=("buku", "judul", "hist_b_judul"))
        st.text_input("Update Hal:", value=buku_data['halaman'], key="hist_b_halaman", 
                      on_change=update_text, args=("buku", "halaman", "hist_b_halaman"))

# >>> HALAMAN 3: HAFALAN JUZ AMMA
elif st.session_state.page == "hafalan":
    st.title("📖 Hafalan Juz 'Amma")
    st.caption("Centang surat yang sudah lancar dihafal.")
    st.divider()

    list_juz_amma = [
        "An-Naba'", "An-Nazi'at", "'Abasa", "At-Takwir", "Al-Infitar", 
        "Al-Mutaffifin", "Al-Insyiqaq", "Al-Buruj", "At-Tariq", "Al-A'la",
        "Al-Ghasyiyah", "Al-Fajr", "Al-Balad", "Asy-Syams", "Al-Lail",
        "Ad-Duha", "Al-Insyirah", "At-Tin", "Al-'Alaq", "Al-Qadr",
        "Al-Bayyinah", "Az-Zalzalah", "Al-'Adiyat", "Al-Qari'ah", "At-Takatsur",
        "Al-'Asr", "Al-Humazah", "Al-Fil", "Quraisy", "Al-Ma'un",
        "Al-Kautsar", "Al-Kafirun", "An-Nasr", "Al-Lahab", "Al-Ikhlas",
        "Al-Falaq", "An-Nas"
    ]

    col1, col2, col3 = st.columns(3)
    def render_surah_checkbox(surah_name):
        is_done = st.session_state.db['hafalan'].get(surah_name, False)
        st.checkbox(surah_name, value=is_done, key=f"chk_hafalan_{surah_name}", on_change=toggle_check, args=("hafalan", surah_name))

    with col1:
        for surah in list_juz_amma[:12]: render_surah_checkbox(surah)
    with col2:
        for surah in list_juz_amma[12:24]: render_surah_checkbox(surah)
    with col3:
        for surah in list_juz_amma[24:]: render_surah_checkbox(surah)
    
    st.divider()
    total_surah = len(list_juz_amma)
    sudah_hafal = sum(1 for v in st.session_state.db['hafalan'].values() if v is True)
    persen = sudah_hafal / total_surah if total_surah > 0 else 0
    st.progress(persen, text=f" Progres: {sudah_hafal} dari {total_surah} Surat")

# >>> HALAMAN 4: MY NOTES (MASONRY LAYOUT)
elif st.session_state.page == "note":
    st.title("📒 My Notes")
    st.caption("Catat ide, rangkuman, atau curhatanmu di sini (Support Markdown!).")
    st.divider()

    # --- INPUT SECTION ---
    with st.expander("➕ Buat Catatan Baru", expanded=True):
        st.text_input("Judul Catatan:", key="in_memo_judul", placeholder="Cth: Ide Skripsi")
        st.text_area("Isi Catatan (Markdown):", key="in_memo_isi", height=150, 
                     placeholder="Bisa pakai **bold**, - list, atau # Header")
        st.button("Simpan Catatan", on_click=add_new_memo)

    st.divider()

    # --- DISPLAY SECTION (3 KOLOM MASONRY) ---
    if not st.session_state.db['memos']:
        st.info("Belum ada catatan. Buat baru di atas! 👆")
    else:
        cols = st.columns(3)
        for i, memo in enumerate(st.session_state.db['memos']):
            col_idx = i % 3 
            with cols[col_idx]:
                with st.container(border=True):
                    c_head, c_del = st.columns([0.85, 0.15])
                    with c_head:
                        if memo['title']: st.markdown(f"#### {memo['title']}")
                        st.caption(f"📅 {memo['date']}")
                    with c_del:
                        if st.button("🗑️", key=f"del_mem_{i}"):
                            delete_memo(i)
                    st.markdown("---")
                    if memo['content']:
                        st.markdown(memo['content'])
                    else:
                        st.caption("*Tidak ada isi konten*")


# >>> HALAMAN 5: FINANCE (DENGAN TUTUP BUKU & HISTORY)
elif st.session_state.page == "finance":
    st.title("💵 Keuangan & Tabungan")
    st.caption("Catat arus kas harian, lalu 'Tutup Buku' untuk menyimpannya ke history.")
    st.divider()

    col1, col2, col3 = st.columns(3)

    # Input Harian (Temp)
    money_data = st.session_state.db['money']
    bank_data = st.session_state.db['bank']

    # --- INPUT HARIAN ---
    with col1:
        st.markdown("### 💸 Cash")
        st.text_input("Masuk (Harian):", value=money_data['masuk'], key="hist_m_masuk", 
                      on_change=update_text, args=("money", "masuk", "hist_m_masuk"))
        st.text_input("Keluar (Harian):", value=money_data['keluar'], key="hist_m_keluar", 
                      on_change=update_text, args=("money", "keluar", "hist_m_keluar"))
        
    with col2:
        st.markdown("### 🏦 Bank")
        st.text_input("Masuk (Harian):", value=bank_data['income'], key="hist_b_income", 
                      on_change=update_text, args=("bank", "income", "hist_b_income"))
        st.text_input("Keluar (Harian):", value=bank_data['tarik'], key="hist_b_tarik", 
                      on_change=update_text, args=("bank", "tarik", "hist_b_tarik"))

    # --- REKAP & SALDO ---
    with col3:
        st.markdown("### 📊 Total Aset")
        # Hitung Net Harian
        c_in = int(money_data['masuk'] or 0)
        c_out = int(money_data['keluar'] or 0)
        b_in = int(bank_data['income'] or 0)
        b_out = int(bank_data['tarik'] or 0)

        # Ambil Saldo Disimpan
        saved_cash = st.session_state.db['savings']['cash']
        saved_bank = st.session_state.db['savings']['bank']
        
        # Hitung Real Time
        total_cash = saved_cash + (c_in - c_out)
        total_bank = saved_bank + (b_in - b_out)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Dompet", f"Rp {total_cash:,}", delta=f"{c_in - c_out} Hari ini")
            st.metric("Total Bank", f"Rp {total_bank:,}", delta=f"{b_in - b_out} Hari ini")
        with col2:
            st.markdown("## Informasi:")
            if saved_cash < 50000:
                st.warning("⚠️ Saldo Dompet di bawah Rp 50.000! Segera Ambil Uang.")
            elif saved_cash < 25000:
                st.warning("❗ Saldo Dompet Kritis di bawah Rp 25.000!")
            elif saved_cash >= 1000000:
                st.success("✅ Saldo Dompet Aman.")
        st.markdown("---")
        if st.button("🔒 Tutup Buku & Simpan", type="primary"):
            tutup_buku()

    st.divider()
    
    # --- TABLE HISTORY ---
    st.subheader("📜 Riwayat Transaksi (History)")
    
    if st.session_state.db['finance_history']:
        # Header Table Manual biar rapi
        h1, h2, h3, h4, h5 = st.columns([2, 2, 2, 2, 1])
        h1.markdown("**Tanggal**")
        h2.markdown("**Dompet (+/-)**")
        h3.markdown("**Bank (+/-)**")
        h4.markdown("**Total Aset**")
        h5.markdown("**Aksi**")
        st.markdown("---")
        
        for i, item in enumerate(st.session_state.db['finance_history']):
            c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
            with c1: 
                st.write(f"{item['date']}")
                st.caption(f"{item['timestamp']}")
            with c2: 
                net_c = item['cash_in'] - item['cash_out']
                color = "green" if net_c >= 0 else "red"
                st.markdown(f":{color}[Rp {net_c:,}]")
            with c3: 
                net_b = item['bank_in'] - item['bank_out']
                color = "green" if net_b >= 0 else "red"
                st.markdown(f":{color}[Rp {net_b:,}]")
            with c4: 
                st.write(f"**Rp {item['balance_after']:,}**")
            with c5:
                if st.button("🗑️", key=f"del_hist_{i}"):
                    delete_history_finance(i)
            st.divider()
    else:
        st.info("Belum ada riwayat tutup buku.")