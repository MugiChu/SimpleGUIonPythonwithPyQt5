import subprocess
import multiprocessing
import sys
import psutil
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton



class MonitorThread(QThread):
    cpu_usage_changed = pyqtSignal(float)
    memory_usage_changed = pyqtSignal(float)
    temp_changed = pyqtSignal(str)
    ssdandhdd_changed = pyqtSignal(str)
    battery_changed = pyqtSignal(str)
    fan_changed = pyqtSignal(str)
    ping_changed = pyqtSignal(str)
    cores_changed = pyqtSignal(int)
    t_changed = pyqtSignal(str)
    mhz_changed = pyqtSignal(str)

    def run(self):
        while True:
            try:
                temp_info = psutil.sensors_temperatures()
            except:
                temp_info = "Не удалось получить информацию о температуре попробуйте на Linux/FreeBSD"
            try:
                ssdandhdd_info = psutil.disk_usage('/')
                ssdandhdd_info = str(ssdandhdd_info)
            except:
                ssdandhdd_info = "Не удалось получить информацию о SSD/HDD на попробуйте Linux/FreeBSD"
            try:
                battery_info = psutil.sensors_battery()
                battery_info = str(battery_info)
            except:
                battery_info = "Аккумулятор отсутствует"
            try:
                fan_speeds = psutil.sensors_fans()
                fan_speeds = str(fan_speeds)
            except:
                fan_speeds = "Куллер отсутствует"

            mhz = psutil.cpu_freq()
            mhz = str(mhz)
            t = psutil.net_io_counters()
            t = str(t)
            result0 = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True)
            ping_output = result0.stdout.strip()
            cores = multiprocessing.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            self.temp_changed.emit(temp_info)
            self.cpu_usage_changed.emit(cpu_percent)
            self.memory_usage_changed.emit(memory_usage)
            self.ssdandhdd_changed.emit(ssdandhdd_info)
            self.battery_changed.emit(battery_info)
            self.fan_changed.emit(fan_speeds)
            self.ping_changed.emit(ping_output)
            self.cores_changed.emit(cores)
            self.t_changed.emit(t)
            self.mhz_changed.emit(mhz)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мониторинг")
        self.setGeometry(200, 200, 1400, 1400)
        self.text_edit_temp = QTextEdit()
        self.text_edit_temp.setGeometry(10, 10, 180, 30)
        self.text_edit_battery = QTextEdit()
        self.text_edit_battery.setGeometry(10, 10, 180, 30)
        self.text_edit_ssdandhdd = QTextEdit()
        self.text_edit_ssdandhdd.setGeometry(10, 10, 180, 30)
        self.text_edit_cpu = QTextEdit()
        self.text_edit_cpu.setGeometry(10, 10, 180, 30)
        self.text_edit_memory = QTextEdit()
        self.text_edit_memory.setGeometry(10, 10, 180, 30)
        self.text_edit_fan = QTextEdit()
        self.text_edit_fan.setGeometry(10, 10, 180, 30)
        self.text_edit_ping = QTextEdit()
        self.text_edit_ping.setGeometry(10, 10, 480, 30)
        self.text_edit_cores = QTextEdit()
        self.text_edit_cores.setGeometry(10, 10, 180, 30)
        self.text_edit_t = QTextEdit()
        self.text_edit_t.setGeometry(10, 10, 180, 30)
        self.text_edit_mhz = QTextEdit()
        self.text_edit_mhz.setGeometry(10, 10, 180, 30)
        self.button_start_stop = QPushButton("Старт")
        self.monitor_thread = MonitorThread()
        self.is_monitoring = False

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit_t)
        layout.addWidget(self.text_edit_mhz)
        layout.addWidget(self.text_edit_temp)
        layout.addWidget(self.text_edit_battery)
        layout.addWidget(self.text_edit_ssdandhdd)
        layout.addWidget(self.text_edit_cpu)
        layout.addWidget(self.text_edit_memory)
        layout.addWidget(self.text_edit_fan)
        layout.addWidget(self.text_edit_ping)
        layout.addWidget(self.text_edit_cores)
        layout.addWidget(self.button_start_stop)
        self.setLayout(layout)

        self.button_start_stop.clicked.connect(self.start_stop_monitoring)
        self.monitor_thread.cpu_usage_changed.connect(self.update_cpu_usage_text)
        self.monitor_thread.memory_usage_changed.connect(self.update_memory_usage_text)
        self.monitor_thread.temp_changed.connect(self.update_temp_usage_text)
        self.monitor_thread.battery_changed.connect(self.update_battery_usage_text)
        self.monitor_thread.ssdandhdd_changed.connect(self.update_ssdandhdd_usage_text)
        self.monitor_thread.fan_changed.connect(self.update_fan_usage_text)
        self.monitor_thread.ping_changed.connect(self.update_ping_usage_text)
        self.monitor_thread.cores_changed.connect(self.update_cores_usage_text)
        self.monitor_thread.t_changed.connect(self.update_t_usage_text)
        self.monitor_thread.mhz_changed.connect(self.update_mhz_usage_text)

    def start_stop_monitoring(self):
        if self.is_monitoring:
            self.monitor_thread.terminate()
            self.is_monitoring = False
            self.button_start_stop.setText("Старт")
        else:
            self.monitor_thread.start()
            self.is_monitoring = True
            self.button_start_stop.setText("Стоп")

    def update_mhz_usage_text(self, mhz_usage):
        self.text_edit_mhz.setPlainText(f"CPU Mhz: {mhz_usage}")

    def update_t_usage_text(self, t_usage):
        self.text_edit_t.setPlainText(f"Network I/O stats: {t_usage}")
    
    def update_cores_usage_text(self, core_usage):
        self.text_edit_cores.setPlainText(f"Cores info: {core_usage}")

    def update_ping_usage_text(self, ping_usage):
        self.text_edit_ping.setPlainText(f"ping info: {ping_usage}")

    def update_fan_usage_text(self, fan_usage):
        self.text_edit_fan.setPlainText(f"Fan info: {fan_usage}")

    def update_battery_usage_text(self, battery_usage):
        self.text_edit_battery.setPlainText(f"battery info: {battery_usage}")

    def update_ssdandhdd_usage_text(self, ssdandhdd_usage):
        self.text_edit_ssdandhdd.setPlainText(f"SSD/HDD usage info in bite: {ssdandhdd_usage}")
    
    def update_temp_usage_text(self, temp_usage):
        self.text_edit_temp.setPlainText(f"CPU temp: {temp_usage}")

    def update_cpu_usage_text(self, cpu_usage):
        self.text_edit_cpu.setPlainText(f"CPU usage: {cpu_usage}%")

    def update_memory_usage_text(self, memory_usage):
        self.text_edit_memory.setPlainText(f"Memory usage: {memory_usage}%")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
