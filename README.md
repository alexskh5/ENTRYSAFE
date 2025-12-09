# EntrySafe: Facial Recognition Security System for Drop-off and Pick-up

_A Desktop Application using Python & PyQt_

---

## 📌 Overview

EntrySafe is a facial recognition–based security system designed to enhance safety and accountability during student drop-off and pick-up. The system identifies guardians through real-time facial scanning and automatically logs student attendance. In cases where a guardian is not recognized, the system initiates a verification workflow that involves staff and the parent.

This project was developed as a secure and automated replacement for traditional manual attendance and gate-entry monitoring.

---

## 🎯 Key Features

### 👤 Admin/Staff (Primary Actor)

- Login and account creation
- Manage Students (Add, Edit, Delete, View)
- Manage Guardians linked to students
- View and update attendance logs
- View guardian scan logs
- Handle unrecognized guardians (temporary enrollment & external verification)

### 🧑‍🤝‍🧑 Guardian

- Scan face for **Drop-off** or **Pick-up**
- Automatically recorded in the system if matched

### 📱 Parent (External)

- Confirms unrecognized guardians through a call or text from staff

---

## 🏛 Actors and Roles

| Actor                       | Role                                                                |
| --------------------------- | ------------------------------------------------------------------- |
| **Admin/Staff**             | Full control: CRUD operations, verification, attendance, monitoring |
| **Guardian**                | Performs face scan for pick-up/drop-off                             |
| **Parent (External Actor)** | Approves or denies unregistered guardian during verification        |

---

## 🧩 System Use Cases

### Admin/Staff Use Cases

1. **Login / Register Account**
2. **View & Edit Profile**
3. **View Students**
   - Add / Edit / Delete students
   - View Student Guardians  
     ↳ Add / Edit / Delete Guardians
4. **View Student Attendance**
   - Update or correct logs when needed
5. **View Guardian Logs**
6. **Handle Unrecognized Guardian**
   - Temporary record + parent verification

### Guardian Use Case

- **Scan Face (Drop-off / Pick-up)**  
  ↳ Verify Guardian identity  
  ↳ If unrecognized → Extended process to Handle Unrecognized Guardian

### Parent (External) Use Case

- **Respond to Verification Request** (Call/Text)  
  ↳ Confirms if guardian is authorized

---

## 🧠 Core Logic Flow

Guardian Arrives → System Scans Face
│
├─ ✔ Recognized → Log Attendance & Timestamp
│
└─ ✖ Not Recognized → Staff Handles Case
│
└→ Contact Parent → Confirm or Deny Access

---

## 🛠 Technologies Used

| Component            | Technology                |
| -------------------- | ------------------------- |
| Programming Language | Python                    |
| GUI Framework        | PyQt                      |
| Face Recognition     | OpenCV + face_recognition |
| Database             | SQLite / Local Storage    |
| Platform             | Desktop Application       |

---

## 🚀 Installation & Setup

> Ensure Python 3.10+ is installed.

```sh
pip install opencv-python
pip install face_recognition
pip install PyQt6


Run the system:

python main.py

```

---

## Developers

Dela Peña, Sam Alexies  delapenasamalexies@gmail.com
Mangubat, Khezy Gwen    khezmangubat@gmail.com
Lim, Phoebe Gale        phoebegalelim1@gmail.com
Booc, Pearl Shene       boocshene17@gmail.com
Igot, Kimberly Marie    igotkimberlymarie@gmail.com

