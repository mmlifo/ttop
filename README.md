# ttop 🚀

A sleek, lightweight, and modern Terminal System Monitor built with Python, [Textual](https://github.com/Textualize/textual), and [Rich](https://github.com/Textualize/rich).

`ttop` provides a clean 2x2 grid dashboard to monitor your system metrics in real time with high accuracy and minimal resource overhead.

![License](https://img.shields.io/github/license/mmlifo/ttop)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

---

## ✨ Features

- **💻 CPU Monitoring:** Real-time per-core load tracking and temperature sensors with dynamic thermal alerts.
- **🧠 Memory & Swap:** Clear visual breakdown of RAM and Swap usage.
- **💾 Disk Usage:** Partition-aware storage monitoring (Read/Write I/O & total usage).
- **🌐 Network Metrics:** Live network interface stats with download/upload speed gauges.
- **🎨 Clean Aesthetic:** Modern Cyan/White/Blue color palette designed for high contrast and readability.
- **⚡ Standalone Executable:** Zero external dependencies required when running the pre-built binary.

---

## 🛠️ Installation

### Option 1: Standalone Binary (Recommended)

Download the pre-compiled binary directly from the [Releases](https://github.com/mmlifo/ttop/releases) page:

```bash
# Make it executable
chmod +x ttop

# Move to system path (optional)
sudo mv ttop /usr/local/bin/
