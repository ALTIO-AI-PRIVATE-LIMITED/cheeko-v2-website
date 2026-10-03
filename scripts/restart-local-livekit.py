"""Recreate the local LiveKit container with reachable WebRTC media ports.

Keeps the previous container stopped as ``livekit-server-before-network-fix``
until browser verification succeeds. Existing API credentials come from the
running container and are never written into this repository.
"""

import json
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import time


NAME = "livekit-server"
BACKUP = "livekit-server-before-network-fix"
CONFIG = Path(__file__).resolve().parents[1] / ".local" / "livekit.yaml"


def docker(*args):
    return subprocess.run(["docker", *args], check=True, text=True, capture_output=True).stdout.strip()


def lan_ip():
    interfaces = subprocess.run(["ifconfig", "en0"], check=True, text=True, capture_output=True).stdout
    match = re.search(r"\binet (\d+\.\d+\.\d+\.\d+)\b", interfaces)
    if not match:
        raise RuntimeError("No IPv4 address on en0; cannot choose a browser-reachable RTC address")
    return match.group(1)


def is_running():
    try:
        with socket.create_connection(("127.0.0.1", 7880), timeout=1):
            return True
    except OSError:
        return False


def main():
    before = json.loads(docker("inspect", NAME))[0]
    if docker("ps", "-a", "--filter", f"name=^{BACKUP}$", "--format", "{{.Names}}"):
        raise RuntimeError(f"{BACKUP} already exists; review it before replacing LiveKit again")

    keys = next((value for value in before["Config"]["Env"] if value.startswith("LIVEKIT_KEYS=")), None)
    if not keys:
        raise RuntimeError("Current LiveKit container has no LIVEKIT_KEYS environment variable")

    ip = lan_ip()
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        "port: 7880\n"
        "log_level: info\n"
        "rtc:\n"
        "  tcp_port: 7881\n"
        "  port_range_start: 50000\n"
        "  port_range_end: 50100\n"
        f"  node_ip: {ip}\n"
        "  use_external_ip: false\n"
    )
    CONFIG.chmod(0o600)

    networks = list(before["NetworkSettings"]["Networks"])
    if len(networks) != 1:
        raise RuntimeError(f"Expected one existing Docker network, found {len(networks)}")

    with tempfile.NamedTemporaryFile(mode="w", prefix="cheeko-livekit-env-", delete=False) as env_file:
        env_file.write(keys + "\n")
        env_path = Path(env_file.name)
    env_path.chmod(0o600)

    renamed = False
    try:
        docker("rename", NAME, BACKUP)
        renamed = True
        docker("stop", BACKUP)
        docker(
            "run", "-d", "--name", NAME,
            "--restart", before["HostConfig"]["RestartPolicy"]["Name"] or "unless-stopped",
            "--network", networks[0],
            "--env-file", str(env_path),
            "-v", f"{CONFIG}:/etc/livekit.yaml:ro",
            "-p", "7880:7880/tcp",
            "-p", "7881:7881/tcp",
            "-p", "50000-50100:50000-50100/udp",
            before["Config"]["Image"],
            "--config", "/etc/livekit.yaml", "--bind", "0.0.0.0",
        )
        for _ in range(40):
            if is_running():
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("Replacement LiveKit did not open signaling port 7880")
        print(f"LiveKit running with advertised RTC IP {ip}; previous container saved as {BACKUP}.")
        print("Configured ports: TCP 7880, 7881; UDP 50000-50100.")
    except Exception:
        if renamed:
            subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)
            docker("rename", BACKUP, NAME)
            docker("start", NAME)
        raise
    finally:
        env_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
