import time
import psutil
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Header, Footer, Static


def get_cpu_temp_val() -> float:
    """CPU temp"""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        
        for sensor_name in ('coretemp', 'cpu_thermal', 'k10temp', 'zenpower', 'acpitz'):
            if sensor_name in temps and temps[sensor_name]:
                return temps[sensor_name][0].current
        
        first_sensor = next(iter(temps.values()))
        if first_sensor:
            return first_sensor[0].current
    except Exception:
        pass
    return None


def make_bar(percent: float, color: str = "cyan", length: int = 14) -> Text:
    filled = round(length * percent / 100)
    if percent > 0 and filled == 0:
        filled = 1
    
    text = Text()
    text.append("[", style="white")
    text.append("█" * filled, style=color)
    text.append("░" * (length - filled), style="dim white")
    text.append(f"] {percent:5.1f}%", style="white")
    return text


def make_temp_bar(temp_val: float, length: int = 14) -> Text:
    text = Text()
    if temp_val is None:
        text.append("[N/A]", style="dim white")
        return text

    percent = min(max(temp_val, 0), 100)
    filled = round(length * percent / 100)
    if percent > 0 and filled == 0:
        filled = 1

    if temp_val < 60:
        color = "green"
    elif temp_val < 80:
        color = "yellow"
    else:
        color = "red"

    text.append("[", style="white")
    text.append("█" * filled, style=color)
    text.append("░" * (length - filled), style="dim white")
    text.append(f"] {temp_val:4.1f}°C", style="white")
    return text


def make_activity_bar(value_mb: float, max_mb: float = 10.0, color: str = "white", length: int = 15) -> Text:
    percent = min((value_mb / max_mb) * 100, 100)
    filled = round(length * percent / 100)
    if value_mb > 0 and filled == 0:
        filled = 1

    text = Text()
    text.append("[", style="white")
    text.append("█" * filled, style=color)
    text.append("░" * (length - filled), style="dim white")
    text.append("]", style="white")
    return text


class SystemMonitorApp(App):
    CSS = """
    Grid {
        grid-size: 2 2;
        grid-gutter: 1 1;
        padding: 1 2;
        height: 100%;
    }

    Static {
        background: $surface;
        padding: 1;
        height: 100%;
    }

    #cpu_widget {
        border: solid cyan;
    }

    #mem_widget {
        border: solid white;
    }

    #disk_widget {
        border: solid #1e90ff;
    }

    #net_widget {
        border: solid white;
    }
    """

    TITLE = "System Monitor"

    def __init__(self):
        super().__init__()
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Static("Loading CPU Info...", id="cpu_widget"),
            Static("Loading Memory Info...", id="mem_widget"),
            Static("Loading Disk Info...", id="disk_widget"),
            Static("Loading Network Info...", id="net_widget"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        # 1. CPU Usage & Temperature
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_temp = get_cpu_temp_val()
        
        cpu_text = Text()
        cpu_text.append("CPU Usage\n\n", style="bold cyan")
        cpu_text.append("Load : ", style="bold white")
        cpu_text.append_text(make_bar(cpu_percent, color="cyan", length=18))
        cpu_text.append("\nTemp : ", style="bold white")
        cpu_text.append_text(make_temp_bar(cpu_temp, length=18))
        cpu_text.append(f"\n\nCores: {psutil.cpu_count(logical=True)} Threads", style="white")
        self.query_one("#cpu_widget", Static).update(cpu_text)

        # 2. Memory Usage (RAM + Swap)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        mem_text = Text()
        mem_text.append("Memory Usage\n\n", style="bold white")
        
        # RAM Bar
        mem_text.append("RAM  : ", style="bold white")
        mem_text.append_text(make_bar(mem.percent, color="white", length=18))
        
        # Swap Bar
        mem_text.append("\nSwap : ", style="bold white")
        mem_text.append_text(make_bar(swap.percent, color="white", length=18))
        
        mem_text.append(
            f"\n\nRAM Total: {mem.total / (1024**3):.2f} GB | Used: {mem.used / (1024**3):.2f} GB\n"
            f"Swap Total: {swap.total / (1024**3):.2f} GB | Used: {swap.used / (1024**3):.2f} GB",
            style="white"
        )
        self.query_one("#mem_widget", Static).update(mem_text)

        # 3. Disk Usage
        disk_text = Text()
        disk_text.append("Disk Usage\n\n", style="bold #1e90ff")

        partitions = psutil.disk_partitions(all=False)
        seen_mounts = set()

        for partition in partitions:
            if partition.mountpoint in seen_mounts or partition.fstype in ('tmpfs', 'devtmpfs', 'squashfs', 'overlay'):
                continue
            seen_mounts.add(partition.mountpoint)

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                mount_name = partition.mountpoint
                if len(mount_name) > 22:
                    mount_name = mount_name[:19] + "..."
                mount_padded = mount_name.ljust(22)

                disk_text.append(f"{mount_padded} ", style="bold white")
                disk_text.append_text(make_bar(usage.percent, color="#1e90ff", length=12))
                disk_text.append(
                    f" ({usage.used / (1024**3):.1f}/{usage.total / (1024**3):.1f} GB)\n",
                    style="dim white"
                )
            except PermissionError:
                continue

        self.query_one("#disk_widget", Static).update(disk_text)

        # 4. Network Info
        current_net = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - self.last_time

        bytes_sent_sec = (current_net.bytes_sent - self.last_net.bytes_sent) / max(time_delta, 0.001)
        bytes_recv_sec = (current_net.bytes_recv - self.last_net.bytes_recv) / max(time_delta, 0.001)

        sent_mb_s = bytes_sent_sec / (1024**2)
        recv_mb_s = bytes_recv_sec / (1024**2)

        self.last_net = current_net
        self.last_time = current_time

        net_text = Text()
        net_text.append("Network I/O Speed\n\n", style="bold white")
        
        net_text.append("▲ UP  : ", style="bold white")
        net_text.append_text(make_activity_bar(sent_mb_s, max_mb=5.0, color="white", length=15))
        net_text.append(f" {sent_mb_s * 1024:.1f} KB/s\n", style="white")
        
        net_text.append("▼ DOWN: ", style="bold cyan")
        net_text.append_text(make_activity_bar(recv_mb_s, max_mb=10.0, color="cyan", length=15))
        net_text.append(f" {recv_mb_s * 1024:.1f} KB/s\n\n", style="white")
        
        net_text.append(
            f"Total Sent: {current_net.bytes_sent / (1024**2):.1f} MB\n"
            f"Total Recv: {current_net.bytes_recv / (1024**2):.1f} MB",
            style="white"
        )
        self.query_one("#net_widget", Static).update(net_text)


if __name__ == "__main__":
    app = SystemMonitorApp()
    app.run()
