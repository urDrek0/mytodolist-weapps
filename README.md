# 🚀 My Life Tracker: All-in-One Personal Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **A comprehensive, offline-first productivity suite designed to manage daily habits, academic tasks, finances, and spiritual goals in one unified interface.**

---

## 📖 Overview

**My Life Tracker** is not just another to-do list. It is a fully functional **Single Page Application (SPA)** built with Python and Streamlit. It solves the problem of app fragmentation by combining essential life management tools into a single, cohesive dashboard. I Created this Web Application based on my own daily activity and priority.

This project demonstrates complex **State Management**, **Data Persistence (JSON)**, and **Dynamic CRUD Operations** without relying on heavy external database services.

---

## ✨ Key Features

### 1. 📝 Dynamic Dashboard
* **Daily Routine Tracker:** Auto-resetting checklists for prayers, chores, and self-care.
* **Exercise Logger:** Tracks workout types (Push/Pull/Legs) and completion status.
* **Reading Tracker:** Logs progress for Books and Quran reading.

### 2. 🎓 Academic Management (CRUD)
* **Dynamic Course Creation:** Users can add/remove subjects (Mata Kuliah) on the fly.
* **Task Management:** Add specific tasks/assignments per subject with individual progress tracking.

### 3. 💵 Financial Ledger System
* **Dual Wallet Tracking:** Separate tracking for **Cash (Wallet)** and **Bank**.
* **"Closing Book" Logic:** A robust feature that calculates daily net flow, adds it to the permanent savings balance, and resets daily inputs—mimicking real-world accounting.
* **Transaction History:** Logs every "Closing Book" action with timestamps and balance snapshots.
* **Smart Alerts:** Visual warnings if balances drop below critical levels.

### 4. 📒 Masonry Notes
* **Markdown Support:** Write notes with rich text formatting (bold, lists, headers).
* **Masonry Grid Layout:** Aesthetically pleasing 3-column layout for organizing thoughts.

### 5. 🕌 Spiritual Tracker (Hafalan)
* **Juz Amma Progress:** Visual progress bar and checklist for memorization tracking.
* **Persistent Data:** Unlike daily routines, memorization progress is stored permanently.

---

## 🛠️ Tech Stack & Engineering Concepts

This project showcases several software engineering principles:

* **Language:** Python 3.10+
* **Framework:** Streamlit (Web Interface)
* **Database:** Local JSON (NoSQL-like structure)
* **Key Concepts Implemented:**
    * **Session State Management:** Handling data persistence across app reruns.
    * **JSON Serialization/Deserialization:** Storing complex nested data structures locally.
    * **Algorithmic Logic:** Custom logic for "Daily Reset" vs "Permanent Storage" based on date comparison.
    * **Error Handling:** Auto-recovery mechanisms for corrupted or missing data files.

---

## 🚀 How to Run Locally

This app is designed to run offline on your local machine.

### Prerequisites
* Python installed on your computer.

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/life-tracker.git](https://github.com/yourusername/life-tracker.git)
    cd life-tracker
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit
    ```

3.  **Run the App**
    ```bash
    streamlit run main.py
    ```

4.  **Done!** The app will open automatically in your default browser.

---

## 📂 Project Structure


```

life-tracker/
│
├── main.py             # The brain of the application (Frontend + Backend logic)
├── data.json           # Local database (Auto-generated on first run)
├── cat_bg.jpg          # Sidebar asset
├── README.md           # Documentation
└── requirements.txt    # Dependency list

```

---

## 📢 Offline and Private Usage
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/life-tracker.git](https://github.com/yourusername/life-tracker.git)
    cd life-tracker
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit
    ```

3.  **Create `.bat` file**
    ```bash
    @echo off
    title My Life Tracker
    echo Sedang membuka aplikasi...
    cd /d "[Your File Path]"
    python -m streamlit run main.py
    pause
    ```

4.  **Done!** The app will open automatically in your default browser.


## 🤝 Contribution

Feel free to fork this project and submit Pull Requests. Ideas for future updates:
* [ ] Data visualization charts for finance history.
* [ ] Export data to CSV/Excel.
* [ ] Password protection.

---

**Created with ❤️ by Bayu Setyo P**
**Dedicated to my ❤️ Cips<3**