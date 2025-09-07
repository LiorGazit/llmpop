from llmpop.monitor_resources import start_resource_monitoring


def test_monitor_thread_starts(tmp_path, monkeypatch):
    logfile = tmp_path / "res.csv"

    # Make psutil.cpu_percent fast by not sleeping 1s in test (optional)
    import psutil

    monkeypatch.setattr(psutil, "cpu_percent", lambda interval=1: 0.1)

    thread = start_resource_monitoring(duration=1, interval=1, logfile=str(logfile))
    thread.join(timeout=3)
    assert logfile.exists()
    assert "CPU_%" in logfile.read_text()
