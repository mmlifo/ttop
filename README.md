
# ttop 🚀

A sleek, lightweight, and modern Terminal System Monitor built with Python, [Textual](https://github.com/Textualize/textual), and [Rich](https://github.com/Textualize/rich).

`ttop` provides a clean 2x2 grid dashboard to monitor your system metrics in real time with high accuracy and minimal resource overhead.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ⚡ Dependencies

Running `ttop` from source requires **Python 3.8+** and the following modules:

- **`psutil`** — System metrics and resource utilization
- **`textual`** — Modern TUI application framework
- **`rich`** — Terminal formatting and rendering

---

## 🛠️ Installation & Usage

### Option 1: Standalone Binary (Recommended)

Download the pre-compiled executable directly from the [Releases](https://github.com/mmlifo/ttop/releases) page without installing Python:

```bash
# Make executable
chmod +x ttop

# Run ttop
./ttop

# (Optional) Move to system PATH
sudo mv ttop /usr/local/bin/


Option 2: Running from Source
Clone the repository:

git clone [https://github.com/mmlifo/ttop.git](https://github.com/mmlifo/ttop.git)
cd ttop


pip install psutil textual rich

python ttop.py


📦 Building Standalone Executable

To compile ttop.py into a single standalone binary using PyInstaller:

pip install pyinstaller
pyinstaller --onefile --clean ttop.py -n ttop


The compiled binary will be generated in dist/ttop.
✨ Features

    💻 CPU Monitoring: Real-time per-core load tracking and temperature sensors with dynamic thermal alerts.

    🧠 Memory & Swap: Clear visual breakdown of RAM and Swap usage.

    💾 Disk Usage: Partition-aware storage monitoring (Read/Write I/O & total usage).

    🌐 Network Metrics: Live network interface stats with download/upload speed gauges.

    🎨 Modern TUI: High contrast, clean layout, and minimal system overhead.

📄 License

This project is licensed by me 