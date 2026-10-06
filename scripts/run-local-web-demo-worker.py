"""Run Picoclaw as a separate LiveKit worker for website character demos.

Uses the admin dashboard's local LiveKit settings and the Manager API service
key. The worker keeps each anonymous room in its own temporary workspace.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def env_values(path):
    values = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if separator:
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


home = Path.home()
backend = home / "cheeko-backend/main"
picoclaw = home / "picoclaw"
source = home / ".picoclaw-livekit-run"
admin = env_values(backend / "admin-dashboard/.env")
manager = env_values(backend / "manager-api-node/.env")
picoclaw_env = env_values(picoclaw / ".env")
service_key = picoclaw_env.get("MANAGER_API_SECRET") or manager.get("SERVICE_SECRET_KEY")
binary = picoclaw / "build/picoclaw-livekit-darwin-arm64"

required = ("LIVEKIT_API_KEY", "LIVEKIT_API_SECRET")
if not binary.is_file() or not service_key or any(not admin.get(key) for key in required):
    raise SystemExit("Local Picoclaw binary, LiveKit credentials, or Manager API service key is missing.")
if manager.get("WEB_DEMO_AGENT_NAME") != "cheeko-web-demo":
    raise SystemExit("Set WEB_DEMO_AGENT_NAME=cheeko-web-demo in manager-api-node/.env and restart the API.")

with tempfile.TemporaryDirectory(prefix="cheeko-web-picoclaw-") as directory:
    work = Path(directory)
    config = json.loads((source / "config.json").read_text())
    config.setdefault("agents", {}).setdefault("defaults", {})["workspace"] = str(work / "workspace")
    livekit = config.setdefault("livekit_service", {})
    livekit["server_url"] = "ws://127.0.0.1:7880"
    livekit["manager_api"] = {"base_url": "http://127.0.0.1:8002/toy"}
    config_path = work / "config.json"
    config_path.write_text(json.dumps(config, indent=2))
    config_path.chmod(0o600)
    security_path = work / ".security.yml"
    shutil.copyfile(source / ".security.yml", security_path)
    security_path.chmod(0o600)

    environment = os.environ.copy()
    environment.update({
        "PICOCLAW_HOME": str(work),
        "PICOCLAW_LIVEKIT_SERVER_URL": "ws://127.0.0.1:7880",
        "PICOCLAW_LIVEKIT_API_KEY": admin["LIVEKIT_API_KEY"],
        "PICOCLAW_LIVEKIT_API_SECRET": admin["LIVEKIT_API_SECRET"],
        "MANAGER_API_URL": "http://127.0.0.1:8002/toy",
        "MANAGER_API_SECRET": service_key,
    })
    print("Starting isolated Picoclaw worker: cheeko-web-demo", flush=True)
    subprocess.run(
        [str(binary), "--agent-name", "cheeko-web-demo", "--config", str(config_path)],
        cwd=picoclaw,
        env=environment,
        check=True,
    )
