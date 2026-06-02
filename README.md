[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Styling](https://img.shields.io/badge/UI-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Environment](https://img.shields.io/badge/Environment-Termux-A4C639?style=for-the-badge&logo=android&logoColor=white)](https://termux.dev)


# 🚀 IG-Intel V2 - Live Web Monitoring OSINT Dashboard

An advanced, stealthy, and lightweight Instagram OSINT (Open Source Intelligence) monitoring engine. Equipped with a high-performance **FastAPI** backend, automated **APScheduler** tracking loops, and a stunning, responsive dark-themed **Tailwind CSS Web Dashboard**. 

Specially optimized to run flawlessly on mobile and localized environments via **Termux** and **Kali NetHunter** without heavy dependencies.

---

## 🎨 Dashboard Preview & UI
The application shifts the legacy terminal-based tracking log into a modern, easy-to-use control panel. You can deploy trackers, monitor background sync statuses, and manage your intelligence target queue directly via any smartphone or PC browser.

---

## 🔥 Key Features
* 📱 **Tailwind Web Frontend:** Modern cyber-style UI with real-time counters and action controls.
* ⚡ **FastAPI Core Architecture:** High-speed asynchronous engine serving both web layouts and REST endpoints.
* ⏱️ **Automated Surveillance Loop:** Background job manager running automatically every 15 minutes to sync target metrics.
* 📦 **Localized SQLite Storage:** Thread-safe local database architecture configured specifically to eliminate setup complexities on Android platforms.
* 📑 **Interactive API Console:** Built-in Swagger UI sandbox for manual query debugging (`/docs`).

---

## 📂 Repository Directory Structure
```text
ig-intel-v2/
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── scheduler.py
│   └── database/
│       ├── __init__.py
│       └── postgres.py
└── templates/
    └── index.html
```
### 🛠️ Installation & Deployment
**Follow these commands inside your local environment (Termux, Linux, or PC) to fire up the system:**

**1. Clone the Workspace**

```bash
git clone https://github.com/naveen-anon/ig-intel-v2.0.git
cd ig-intel-v2.0
```
**2. Install Core Dependencies**
Ensure you have Python 3 installed. Run the following requirement installation pip matrix:

```bash
pip install -r requirements.txt
```
***3. Initialize the Surveillance Engine***
*Boot up your backend worker and frontend service using the master launcher file:*

```bash
python3 run.py
```

---

## 🌐 How to Access the App

Once the console logs state `🚀 IG-Intel V2 System Engine Online & Monitoring Live...`, open up your web browser and navigate to:

* 💻 **Web Dashboard UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* 🛠️ **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Architecture Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Serves the web-based Tailwind control dashboard. |
| **GET** | `/monitor/list` | Pulls all target metrics records from the internal database. |
| **POST**| `/monitor/add/{username}` | Deploys a new background surveillance tracker onto a profile. |
| **POST**| `/monitor/stop/{username}` | Halts active tracking loops for a specified target profile. |

---
