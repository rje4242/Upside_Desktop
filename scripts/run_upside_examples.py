#!/usr/bin/env python3
import json
import os
import platform
import shlex
import subprocess
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_ROOT = ROOT / "example_run_logs" / RUN_ID

COMMANDS = [
    ("01.GettingStarted", ["bash", "0.run.sh"]),
    ("01.GettingStarted", ["bash", "1.ana.sh"]),
    ("02.ReplicaExchangeSimulation", ["python", "run.py"]),
    ("03.TrajectoryAnalysis", ["python", "0.run.py"]),
    ("03.TrajectoryAnalysis", ["bash", "1.traj_ana.sh"]),
    ("03.TrajectoryAnalysis", ["python", "2.mbar_meltingCurve_freeEnergy.py"]),
    ("04.HDX", ["python", "0.run.py"]),
    ("04.HDX", ["python", "1.config.py"]),
    ("04.HDX", ["bash", "2.traj_ana.sh"]),
    ("04.HDX", ["bash", "3.get_protaction_states.sh"]),
    ("04.HDX", ["python", "4.calc_HDX.py"]),
    ("05.Advanced_config.py", ["bash", "0.run.sh"]),
    ("05.Advanced_config.py", ["bash", "1.ana.sh"]),
    ("06.PullingSimulation", ["python", "0.run.py"]),
    ("06.PullingSimulation", ["python", "1.get_force.py"]),
    ("07.MoreRestraints", ["python", "0.run.py"]),
    ("08.MembraneSimulation", ["python", "0.normal.run.py"]),
    ("08.MembraneSimulation", ["python", "1.channel.run.py"]),
    ("08.MembraneSimulation", ["python", "2.lateral_pressure.run.py"]),
    ("08.MembraneSimulation", ["python", "3.fixed_curvature.run.py"]),
    ("08.MembraneSimulation", ["python", "4.curvature_dynamics1.run.py"]),
    ("08.MembraneSimulation", ["python", "5.curvature_dynamics2.run.py"]),
    ("09.IsomerizationPRO", ["python", "0.run.py"]),
    ("09.IsomerizationPRO", ["python", "recal_omega.py"]),
    ("09.IsomerizationPRO", ["python", "recal_potential.py"]),
    ("09.IsomerizationPRO", ["python", "plot_two_wall.py"]),
    ("10.SelfAvoidRandomWalk", ["python", "run.py"]),
    ("12.MultistepIntegrator", ["python", "0.run.py"]),
    ("12.MultistepIntegrator", ["bash", "1.ana.sh"]),
    ("13.RestartSimulation", ["python", "0.run.py"]),
    ("13.RestartSimulation", ["python", "0.continue.py"]),
    ("15.SpatialTransformation", ["bash", "0.run.sh"]),
    ("15.SpatialTransformation", ["bash", "1.ana.sh"]),
]


def run_shell(command, cwd):
    return subprocess.run(
        ["bash", "-lc", command],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def collect_machine():
    out = {}
    probes = {
        "cpu": "lscpu | sed -n '1,20p'",
        "mem": "free -h",
        "os": "uname -a",
        "python": "source source.sh >/dev/null 2>&1 && python --version && python - <<'PY'\nimport importlib.metadata as m\nfor p in ['numpy','tables','h5py','matplotlib','scipy','mdtraj']:\n    try:\n        print(f'{p}=={m.version(p)}')\n    except Exception as e:\n        print(f'{p}: not installed ({e.__class__.__name__})')\nPY",
        "upside": "sha256sum obj/upside obj/libupside.so && stat -c '%n %s bytes %y' obj/upside obj/libupside.so",
    }
    for key, cmd in probes.items():
        out[key] = run_shell(cmd, ROOT).stdout
    out["platform"] = platform.platform()
    return out


def summarize_artifacts():
    summary = {}
    for ex in sorted((ROOT / "example").iterdir()):
        if not ex.is_dir() or ex.name.startswith("00.") or ex.name.startswith("11."):
            continue
        files = []
        for sub in ["inputs", "outputs", "results"]:
            p = ex / sub
            if p.exists():
                count = sum(1 for q in p.rglob("*") if q.is_file())
                files.append({"path": str(p.relative_to(ROOT)), "files": count})
        up_files = [str(p.relative_to(ROOT)) for p in ex.rglob("*.up")]
        summary[ex.name] = {"dirs": files, "up_files": up_files[:25], "up_file_count": len(up_files)}
    return summary


def inspect_hdf5():
    code = r"""
import json
from pathlib import Path
import numpy as np
try:
    import tables as tb
except Exception as exc:
    print(json.dumps({"error": f"tables import failed: {exc}"}))
    raise SystemExit
root = Path(".")
out = {}
for p in sorted(root.glob("example/[0-9][0-9].*/**/*.up")):
    if "11.BigSystem" in str(p) or "00.AnalysisScripts" in str(p):
        continue
    item = {"groups": [], "arrays": {}}
    try:
        with tb.open_file(p, "r") as h:
            item["groups"] = [g._v_pathname for g in h.walk_groups("/")][:20]
            for node in h.walk_nodes("/", classname="Array"):
                name = node._v_pathname
                if any(k in name.lower() for k in ["temperature", "energy", "potential", "kinetic", "pos", "time"]):
                    item["arrays"][name] = list(node.shape)
    except Exception as exc:
        item["error"] = str(exc)
    out[str(p)] = item
print(json.dumps(out, indent=2, sort_keys=True))
"""
    proc = run_shell(f"source source.sh >/dev/null 2>&1 && python - <<'PY'\n{code}\nPY", ROOT)
    try:
        return json.loads(proc.stdout)
    except Exception:
        return {"raw": proc.stdout}


def main():
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    results = []
    for idx, (example, argv) in enumerate(COMMANDS, 1):
        rel_cmd = " ".join(shlex.quote(a) for a in argv)
        log_name = f"{idx:02d}_{example}_{argv[-1].replace('/', '_')}.log"
        log_path = LOG_ROOT / log_name
        cwd = ROOT / "example" / example
        command = f"source {shlex.quote(str(ROOT / 'source.sh'))} >/dev/null 2>&1 && {rel_cmd}"
        start = time.time()
        proc = run_shell(command, cwd)
        elapsed = time.time() - start
        log_path.write_text(proc.stdout)
        results.append({
            "index": idx,
            "example": example,
            "command": rel_cmd,
            "elapsed_sec": round(elapsed, 3),
            "returncode": proc.returncode,
            "log": str(log_path.relative_to(ROOT)),
        })
        print(json.dumps(results[-1]), flush=True)
    payload = {
        "run_id": RUN_ID,
        "machine": collect_machine(),
        "commands": results,
        "artifacts": summarize_artifacts(),
        "hdf5": inspect_hdf5(),
    }
    (LOG_ROOT / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"SUMMARY {LOG_ROOT / 'summary.json'}")


if __name__ == "__main__":
    main()
