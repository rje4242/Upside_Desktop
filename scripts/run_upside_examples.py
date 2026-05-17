#!/usr/bin/env python3
"""Run and report on the default Upside numbered examples.

The default mode is intentionally long-running and has no per-command timeout.
Existing generated inputs, outputs, and results for the selected examples are
archived before execution so the report describes this run's artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "example"
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_ROOT = ROOT / "example_run_logs" / RUN_ID
ARCHIVE_ROOT = ROOT / "example_run_archives" / RUN_ID
REPORT_PATH = ROOT / f"EXAMPLE_RUN_REPORT_{RUN_ID}.md"
SUMMARY_PATH = LOG_ROOT / "summary.json"

GENERATED_DIRS = ("inputs", "outputs", "results")
NOTABLE_SUFFIXES = {
    ".up",
    ".vtf",
    ".rmsd",
    ".png",
    ".pdf",
    ".dat",
    ".h5",
    ".hdf5",
    ".npy",
    ".txt",
    ".csv",
    ".log",
}


@dataclass(frozen=True)
class ExampleCommand:
    example: str
    argv: tuple[str, ...]

    @property
    def shell_text(self) -> str:
        return " ".join(shlex.quote(a) for a in self.argv)


COMMANDS: tuple[ExampleCommand, ...] = (
    ExampleCommand("01.GettingStarted", ("bash", "0.run.sh")),
    ExampleCommand("01.GettingStarted", ("bash", "1.ana.sh")),
    ExampleCommand("02.ReplicaExchangeSimulation", ("python", "run.py")),
    ExampleCommand("04.HDX", ("python", "0.run.py")),
    ExampleCommand("04.HDX", ("python", "1.config.py")),
    ExampleCommand("04.HDX", ("bash", "2.traj_ana.sh")),
    ExampleCommand("04.HDX", ("bash", "3.get_protaction_states.sh")),
    ExampleCommand("04.HDX", ("python", "4.calc_HDX.py")),
    ExampleCommand("05.Advanced_config.py", ("bash", "0.run.sh")),
    ExampleCommand("05.Advanced_config.py", ("bash", "1.ana.sh")),
    ExampleCommand("06.PullingSimulation", ("python", "0.run.py")),
    ExampleCommand("06.PullingSimulation", ("python", "1.get_force.py")),
    ExampleCommand("07.MoreRestraints", ("python", "0.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "0.normal.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "1.channel.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "2.lateral_pressure.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "3.fixed_curvature.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "4.curvature_dynamics1.run.py")),
    ExampleCommand("08.MembraneSimulation", ("python", "5.curvature_dynamics2.run.py")),
    ExampleCommand("09.IsomerizationPRO", ("python", "0.run.py")),
    ExampleCommand("09.IsomerizationPRO", ("python", "recal_omega.py")),
    ExampleCommand("09.IsomerizationPRO", ("python", "recal_potential.py")),
    ExampleCommand("09.IsomerizationPRO", ("python", "plot_two_wall.py")),
    ExampleCommand("10.SelfAvoidRandomWalk", ("python", "run.py")),
    ExampleCommand("12.MultistepIntegrator", ("python", "0.run.py")),
    ExampleCommand("12.MultistepIntegrator", ("bash", "1.ana.sh")),
    ExampleCommand("13.RestartSimulation", ("python", "0.run.py")),
    ExampleCommand("13.RestartSimulation", ("python", "0.continue.py")),
    ExampleCommand("15.SpatialTransformation", ("bash", "0.run.sh")),
    ExampleCommand("15.SpatialTransformation", ("bash", "1.ana.sh")),
)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_shell(command: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", command],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def source_prefix() -> str:
    return f"source {shlex.quote(str(ROOT / 'source.sh'))} >/dev/null 2>&1"


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_fingerprint(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False}
    st = path.stat()
    return {
        "path": rel(path),
        "exists": True,
        "size_bytes": st.st_size,
        "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "sha256": sha256(path),
    }


def selected_examples() -> list[str]:
    return sorted({cmd.example for cmd in COMMANDS})


def archive_generated_dirs() -> list[dict[str, Any]]:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    archived: list[dict[str, Any]] = []
    for example in selected_examples():
        example_dir = EXAMPLE_ROOT / example
        for dirname in GENERATED_DIRS:
            src = example_dir / dirname
            if not src.exists():
                continue
            dst = ARCHIVE_ROOT / example / dirname
            dst.parent.mkdir(parents=True, exist_ok=True)
            file_count = sum(1 for p in src.rglob("*") if p.is_file())
            shutil.move(str(src), str(dst))
            archived.append(
                {
                    "example": example,
                    "name": dirname,
                    "from": rel(src),
                    "to": rel(dst),
                    "files": file_count,
                }
            )
    return archived


def collect_machine() -> dict[str, Any]:
    probes = {
        "os": "uname -a",
        "cpu": "lscpu | sed -n '1,25p'",
        "memory": "free -h",
        "python_and_packages": (
            f"{source_prefix()} && python --version && python - <<'PY'\n"
            "import importlib.metadata as m\n"
            "for p in ['numpy','tables','h5py','matplotlib','scipy','mdtraj']:\n"
            "    try:\n"
            "        print(f'{p}=={m.version(p)}')\n"
            "    except Exception as exc:\n"
            "        print(f'{p}: not installed ({exc.__class__.__name__})')\n"
            "PY"
        ),
    }
    out: dict[str, Any] = {
        "platform": platform.platform(),
        "python_executable": sys.executable,
        "upside_binary": file_fingerprint(ROOT / "obj" / "upside"),
        "libupside": file_fingerprint(ROOT / "obj" / "libupside.so"),
    }
    for key, cmd in probes.items():
        proc = run_shell(cmd, ROOT)
        out[key] = {"returncode": proc.returncode, "output": proc.stdout.strip()}
    return out


def summarize_artifacts() -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for example in selected_examples():
        ex = EXAMPLE_ROOT / example
        dirs = []
        notable: dict[str, list[str]] = {}
        for dirname in GENERATED_DIRS:
            p = ex / dirname
            if p.exists():
                dirs.append(
                    {
                        "path": rel(p),
                        "files": sum(1 for q in p.rglob("*") if q.is_file()),
                        "bytes": sum(q.stat().st_size for q in p.rglob("*") if q.is_file()),
                    }
                )
        for p in sorted(ex.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in NOTABLE_SUFFIXES:
                continue
            notable.setdefault(p.suffix.lower(), []).append(rel(p))
        summary[example] = {
            "generated_dirs": dirs,
            "notable_counts": {k: len(v) for k, v in sorted(notable.items())},
            "notable_files": {k: v[:30] for k, v in sorted(notable.items())},
        }
    return summary


def inspect_hdf5() -> dict[str, Any]:
    code = r"""
import json
from pathlib import Path
import numpy as np
try:
    import tables as tb
except Exception as exc:
    print(json.dumps({"error": f"tables import failed: {exc}"}))
    raise SystemExit(0)

selected = {
    "01.GettingStarted", "02.ReplicaExchangeSimulation", "04.HDX",
    "05.Advanced_config.py", "06.PullingSimulation", "07.MoreRestraints",
    "08.MembraneSimulation", "09.IsomerizationPRO", "10.SelfAvoidRandomWalk",
    "12.MultistepIntegrator", "13.RestartSimulation", "15.SpatialTransformation",
}
out = {}
for p in sorted(Path("example").glob("[0-9][0-9].*/**/*.up")):
    if p.parts[1] not in selected:
        continue
    item = {"groups": [], "datasets": {}, "finite_numeric": {}}
    try:
        with tb.open_file(p, "r") as h:
            item["has_input"] = bool("/input" in h)
            item["has_output"] = bool("/output" in h)
            item["groups"] = [g._v_pathname for g in h.walk_groups("/")][:40]
            for node in h.walk_nodes("/", classname="Array"):
                name = node._v_pathname
                lname = name.lower()
                interesting = any(k in lname for k in [
                    "pos", "time", "temperature", "potential", "kinetic", "energy"
                ])
                if not interesting:
                    continue
                shape = [int(x) for x in node.shape]
                item["datasets"][name] = {"shape": shape, "dtype": str(node.dtype)}
                try:
                    arr = node.read()
                    if np.issubdtype(arr.dtype, np.number) and arr.size:
                        finite = np.isfinite(arr)
                        item["finite_numeric"][name] = {
                            "finite": bool(finite.all()),
                            "finite_fraction": float(finite.mean()),
                            "min": float(np.nanmin(arr)),
                            "max": float(np.nanmax(arr)),
                        }
                except Exception as exc:
                    item["finite_numeric"][name] = {"error": str(exc)}
    except Exception as exc:
        item["error"] = str(exc)
    out[str(p)] = item
print(json.dumps(out, indent=2, sort_keys=True))
"""
    proc = run_shell(f"{source_prefix()} && python - <<'PY'\n{code}\nPY", ROOT)
    try:
        parsed = json.loads(proc.stdout)
    except Exception:
        parsed = {"raw": proc.stdout}
    return {"returncode": proc.returncode, "files": parsed}


def write_json(payload: dict[str, Any]) -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True))


def run_commands(limit: int | None = None) -> tuple[list[dict[str, Any]], bool]:
    results: list[dict[str, Any]] = []
    failed_examples: dict[str, str] = {}
    interrupted = False
    commands = COMMANDS[:limit] if limit is not None else COMMANDS
    for idx, cmd in enumerate(commands, 1):
        log_name = f"{idx:02d}_{cmd.example}_{cmd.argv[-1].replace('/', '_')}.log"
        log_path = LOG_ROOT / log_name
        cwd = EXAMPLE_ROOT / cmd.example
        if cmd.example in failed_examples:
            result = {
                "index": idx,
                "example": cmd.example,
                "command": cmd.shell_text,
                "status": "skipped",
                "returncode": None,
                "elapsed_sec": 0.0,
                "log": None,
                "note": f"Skipped because earlier command failed: {failed_examples[cmd.example]}",
            }
            results.append(result)
            print(json.dumps(result), flush=True)
            continue
        shell_command = f"{source_prefix()} && {cmd.shell_text}"
        start = time.time()
        try:
            proc = run_shell(shell_command, cwd)
            elapsed = time.time() - start
            log_path.write_text(proc.stdout)
            status = "passed" if proc.returncode == 0 else "failed"
            result = {
                "index": idx,
                "example": cmd.example,
                "command": cmd.shell_text,
                "status": status,
                "returncode": proc.returncode,
                "elapsed_sec": round(elapsed, 3),
                "log": rel(log_path),
                "note": "" if status == "passed" else "Later commands in this example are skipped.",
            }
            if status == "failed":
                failed_examples[cmd.example] = cmd.shell_text
        except KeyboardInterrupt:
            elapsed = time.time() - start
            result = {
                "index": idx,
                "example": cmd.example,
                "command": cmd.shell_text,
                "status": "interrupted",
                "returncode": None,
                "elapsed_sec": round(elapsed, 3),
                "log": rel(log_path) if log_path.exists() else None,
                "note": "Run interrupted by KeyboardInterrupt; report generated from partial results.",
            }
            results.append(result)
            interrupted = True
            print(json.dumps(result), flush=True)
            break
        results.append(result)
        print(json.dumps(result), flush=True)
    return results, interrupted


def elapsed_text(seconds: float) -> str:
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}m {sec:.0f}s"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {sec:.0f}s"


def format_code_block(text: str, limit: int = 2500) -> str:
    text = (text or "").strip()
    if len(text) > limit:
        text = text[:limit] + "\n... truncated ..."
    return f"```\n{text}\n```"


def write_report(payload: dict[str, Any]) -> None:
    commands = payload.get("commands", [])
    total = sum(c.get("elapsed_sec") or 0 for c in commands)
    slowest = sorted(
        [c for c in commands if c.get("elapsed_sec") is not None],
        key=lambda c: c.get("elapsed_sec", 0),
        reverse=True,
    )[:8]
    failures = [c for c in commands if c.get("status") in {"failed", "interrupted"}]
    lines = [
        f"# Upside Example Run Report {payload['run_id']}",
        "",
        "## Scope",
        "",
        "Ran selected numbered examples with default scripts and durations. Excluded `00.AnalysisScripts`, `03.TrajectoryAnalysis`, and `11.BigSystem`.",
        "",
        f"- Repository: `{ROOT}`",
        f"- Log directory: `{rel(LOG_ROOT)}`",
        f"- Archive directory: `{rel(ARCHIVE_ROOT)}`",
        f"- Summary JSON: `{rel(SUMMARY_PATH)}`",
        f"- Status: `{payload.get('status', 'unknown')}`",
        "",
        "## Archive",
        "",
    ]
    archive = payload.get("archive", [])
    if payload.get("archive_skipped"):
        lines.append("Archive step skipped by `--no-archive`.")
    elif archive:
        lines += ["| Example | Directory | Files | Archived To |", "|---|---:|---:|---|"]
        lines += [
            f"| `{a['example']}` | `{a['name']}` | {a['files']} | `{a['to']}` |"
            for a in archive
        ]
    else:
        lines.append("No pre-existing generated `inputs/`, `outputs/`, or `results/` directories were found for the selected examples.")

    lines += [
        "",
        "## Machine Snapshot",
        "",
        f"- Platform: `{payload['machine'].get('platform', '')}`",
        f"- Python executable used by runner: `{payload['machine'].get('python_executable', '')}`",
        f"- `obj/upside`: `{json.dumps(payload['machine'].get('upside_binary', {}))}`",
        f"- `obj/libupside.so`: `{json.dumps(payload['machine'].get('libupside', {}))}`",
        "",
        "### OS",
        format_code_block(payload["machine"].get("os", {}).get("output", "")),
        "### CPU",
        format_code_block(payload["machine"].get("cpu", {}).get("output", "")),
        "### Memory",
        format_code_block(payload["machine"].get("memory", {}).get("output", "")),
        "### Python Packages",
        format_code_block(payload["machine"].get("python_and_packages", {}).get("output", "")),
        "",
        "## Commands",
        "",
        "| # | Example | Command | Status | Return | Elapsed | Log | Notes |",
        "|---:|---|---|---|---:|---:|---|---|",
    ]
    for c in commands:
        lines.append(
            "| {index} | `{example}` | `{command}` | {status} | {returncode} | {elapsed} | {log} | {note} |".format(
                index=c["index"],
                example=c["example"],
                command=c["command"],
                status=c["status"],
                returncode="" if c.get("returncode") is None else c["returncode"],
                elapsed=elapsed_text(c.get("elapsed_sec") or 0),
                log="" if not c.get("log") else f"`{c['log']}`",
                note=c.get("note", ""),
            )
        )

    lines += ["", "## Artifacts", ""]
    for example, item in payload.get("artifacts", {}).items():
        dirs = item.get("generated_dirs", [])
        counts = item.get("notable_counts", {})
        lines.append(f"### {example}")
        lines.append("")
        if dirs:
            lines.extend(
                f"- `{d['path']}`: {d['files']} files, {d['bytes']} bytes" for d in dirs
            )
        else:
            lines.append("- No generated `inputs/`, `outputs/`, or `results/` directory was present.")
        if counts:
            lines.append(f"- Notable file counts: `{json.dumps(counts, sort_keys=True)}`")
        lines.append("")

    hdf5 = payload.get("hdf5", {})
    files = hdf5.get("files", {})
    lines += [
        "## Data-Flow Verification",
        "",
        f"HDF5 inspection return code: `{hdf5.get('returncode')}`.",
        "",
    ]
    if isinstance(files, dict) and files:
        lines += ["| File | /input | /output | Interesting Datasets | Numeric Check |", "|---|---:|---:|---|---|"]
        for path, item in list(files.items())[:80]:
            if not isinstance(item, dict):
                continue
            datasets = item.get("datasets", {})
            finite = item.get("finite_numeric", {})
            finite_bad = [k for k, v in finite.items() if isinstance(v, dict) and not v.get("finite", True)]
            numeric = "finite" if finite and not finite_bad else ("non-finite values present" if finite_bad else "not checked")
            lines.append(
                f"| `{path}` | {item.get('has_input', '')} | {item.get('has_output', '')} | {len(datasets)} matched | {numeric} |"
            )
    else:
        lines.append("No `.up` HDF5 files were inspected, or HDF5 inspection was unavailable.")

    lines += [
        "",
        "## Scientific Sanity Notes",
        "",
        "- Energy, temperature, position, and time-like arrays in representative `.up` files are checked for finite numeric values when PyTables can read them.",
        "- REMD examples should produce multiple replica `.up` files under `outputs/REMD`; inspect logs and HDF5 temperatures for exchange workflow health.",
        "- HDX should produce configured REMD analysis outputs, protection-state files, and final HDX calculations after the four analysis stages complete.",
        "- Pulling examples should produce force data from `1.get_force.py`; plot or inspect the generated `.dat` files for force-extension behavior.",
        "- Membrane examples are independent six-script variants; compare generated `.up` files and logs by numbered membrane mode.",
        "- Restart simulation should contain both initial and continued trajectory artifacts; check continuity in output time arrays.",
        "- Isomerization and multistep-integrator workflows rely on their recalculation/analysis products in addition to raw `.up` trajectories.",
        "",
        "## Visualization Guidance",
        "",
        "- Open `.vtf` files in VMD where analysis scripts generated them.",
        "- Use `py/extract_vtf.py` for trajectory extraction, `py/mdtraj_upside.py` for MDTraj-based inspection, and `py/attr_overview.py` for HDF5 attribute browsing.",
        "- Use PyTables, HDFView, or another HDF5 viewer to inspect `/input`, `/output`, position, time, temperature, potential, and kinetic datasets.",
        "- Review example-specific `.png`, `.pdf`, `.dat`, `.rmsd`, and table outputs for workflow-specific plots and summaries.",
        "",
        "## Performance",
        "",
        f"- Total measured command wall time: {elapsed_text(total)}.",
        f"- Completed commands: {sum(1 for c in commands if c.get('status') == 'passed')} / {len(commands)}.",
        f"- Failed or interrupted commands: {len(failures)}.",
        "",
    ]
    if slowest:
        lines += ["| Example | Command | Elapsed | Status |", "|---|---|---:|---|"]
        lines += [
            f"| `{c['example']}` | `{c['command']}` | {elapsed_text(c.get('elapsed_sec') or 0)} | {c.get('status')} |"
            for c in slowest
        ]
    lines += [
        "",
        "Elapsed times are machine-specific and include setup, simulation, analysis, and Python startup overhead. For coarse throughput, inspect each command log for progress lines and compare elapsed time against generated frame counts in the corresponding `.up` files.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n")


def build_payload(
    *,
    archive: list[dict[str, Any]],
    commands: list[dict[str, Any]],
    status: str,
    started_at: str,
    ended_at: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "started_at": started_at,
        "ended_at": ended_at,
        "status": status,
        "args": vars(args),
        "excluded_examples": ["00.AnalysisScripts", "03.TrajectoryAnalysis", "11.BigSystem"],
        "selected_examples": selected_examples(),
        "archive": archive,
        "archive_skipped": bool(args.no_archive),
        "commands": commands,
        "machine": collect_machine(),
        "artifacts": summarize_artifacts(),
        "hdf5": inspect_hdf5(),
        "report": rel(REPORT_PATH),
        "summary": rel(SUMMARY_PATH),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List selected commands and exit.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run only the first N commands. Useful for smoke testing; default runs all commands.",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Do not archive existing generated directories before running.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list:
        print("Selected examples:")
        for example in selected_examples():
            print(f"  {example}")
        print("\nCommands:")
        for idx, cmd in enumerate(COMMANDS, 1):
            print(f"{idx:02d}. {cmd.example}: {cmd.shell_text}")
        return 0

    if args.limit is not None and args.limit < 0:
        raise SystemExit("--limit must be non-negative")

    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().isoformat(timespec="seconds")
    archive: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    status = "completed"
    try:
        if not args.no_archive:
            archive = archive_generated_dirs()
        commands, interrupted = run_commands(args.limit)
        if interrupted:
            status = "interrupted"
        elif any(c.get("status") == "failed" for c in commands):
            status = "completed_with_failures"
    finally:
        ended_at = datetime.now().isoformat(timespec="seconds")
        payload = build_payload(
            archive=archive,
            commands=commands,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
            args=args,
        )
        write_json(payload)
        write_report(payload)
        print(f"SUMMARY {SUMMARY_PATH}")
        print(f"REPORT {REPORT_PATH}")
    return 0 if status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
