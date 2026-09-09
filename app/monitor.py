import os
import psutil
from prometheus_client import Gauge

cpu_gauge = Gauge("system_cpu_percent", "Current CPU utilization in percent")
memory_gauge = Gauge("system_memory_percent", "Current memory utilization in percent")
disk_gauge = Gauge("system_disk_percent", "Current disk utilization in percent")
process_count = Gauge("system_process_count", "Number of running processes")


def collect_metrics():
    """Collect host/container resource metrics and publish them to Prometheus."""
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage(os.path.abspath(os.sep)).percent
    processes = len(psutil.pids())

    cpu_gauge.set(cpu)
    memory_gauge.set(memory)
    disk_gauge.set(disk)
    process_count.set(processes)

    return {
        "cpu_percent": cpu,
        "memory_percent": memory,
        "disk_percent": disk,
        "process_count": processes,
    }
