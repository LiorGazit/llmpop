import threading
from datetime import datetime
import psutil
import subprocess
from time import sleep

def get_gpu_usage():
    """
    Returns GPU utilization (%) if an NVIDIA GPU is present, else 'N/A'.
    Requires NVIDIA GPUs and nvidia-smi installed.
    """
    try:
        output = subprocess.check_output(
            "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits",
            shell=True, stderr=subprocess.DEVNULL, text=True
        )
        return output.strip().splitlines()[0]
    except Exception:
        return "N/A"

def log_resource_usage(logfile='resource_usage.log', duration=60, interval=5):
    """
    Logs CPU, Memory, and GPU utilization every `interval` seconds for `duration` seconds.
    """
    print(f"Starting resource monitoring for {duration}s (logging every {interval}s to '{logfile}')")
    end_ts = datetime.now().timestamp() + duration
    with open(logfile, 'w') as f:
        f.write("Timestamp,CPU_%,Memory_%,GPU_%\n")
        f.flush()
        while datetime.now().timestamp() < end_ts:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            gpu = get_gpu_usage()
            line = f"{ts},{cpu},{mem},{gpu}\n"
            f.write(line)
            f.flush()
            print(line.strip())
            sleep(max(0, interval - 1))
    print("Resource monitoring completed.")

def start_resource_monitoring(duration=3600, interval=10, logfile='resource_usage.log'):
    """
    Launches log_resource_usage in a daemon thread and returns the Thread object.
    """
    thread = threading.Thread(
        target=log_resource_usage,
        kwargs={'duration': duration, 'interval': interval, 'logfile': logfile},
        daemon=True
    )
    thread.start()
    print(f"→ Resource monitoring started (daemon thread).")
    return thread
