# 📡 Wivaro

**A real-time internet connectivity tracker and logger**

Wivaro continuously monitors your Wi-Fi (or general internet) connection and records any downtimes and reconnections in a clean, timestamped CSV file.

---

## 🚀 Features

- 🌐 **Real-time monitoring**  
  Sends a ping to the target IP every five seconds.

- 📝 **CSV-based logging**  
  Appends all connection status changes to `logs/internet_log.csv`.

- ⚠️ **Instant downtime alerts**  
  Prints notifications in the terminal whenever your connection is lost or restored.

- 💻 **No external dependencies**  
  Relies solely on Python’s standard library.

- 🧠 **Cross-platform compatibility**  
  Works on Windows, Linux, and macOS.

---

## ⚠️ Disclaimer

This software is provided _as-is_, without any express or implied warranties. Continuous logging may, over time, consume significant disk space. The developer shall not be held liable for any damage, data loss, or other side effects arising from its use.
