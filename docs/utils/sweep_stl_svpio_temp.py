from __future__ import annotations
from pathlib import Path
import yaml
from stl_svpio.tasks.pointmass import run_pointmass_trial

METHOD = "stl_svpio"
TEMPS = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 0.5, 0.8, 1.0,
         2.0, 3.0, 5.0, 8.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0]
ITERS = [i for i in range(20, 201, 10)]


def find_config() -> Path:
    for start in (Path.cwd(), Path(__file__).resolve().parent):
        for d in (start, *start.parents):
            p = d / "configs/paper/table1_reach_avoid.yaml"
            if p.exists():
                return p


def main() -> None:
    payload = yaml.safe_load(find_config().read_text(encoding="utf-8"))
    base = dict(payload["base"])
    method_cfg = dict(payload["methods"][METHOD])
    task_id = str(payload["task_id"])

    print(f"{'stl_temp':>10} | {'robustness(smoothed)':>20} | {'feasible(true)':>14} | {'iters':>8}")
    winner = None
    iterations = 500
    for T in TEMPS:
        for I in ITERS:
            cfg = {**base, **method_cfg, "stl_temperature": T, "svgd_iters": I}
            try:
                r = run_pointmass_trial(task_id, METHOD, cfg, seed=0, jit=True)
                print(f"{T:>10.3f} | {r.robustness:>20.4f} | {('YES' if r.satisfied else 'no'):>14} | {I:>10.3f}")
                if r.satisfied and iterations > I:
                    winner = T
                    iterations = I

    print("-" * 52)
    if winner is not None:
        print(f"FEASIBLE stl_temperature found: {winner}  in iterations: {iterations}")
    else:
        print("No feasible temperature in this sweep -- temperature alone is not the fix.")


if __name__ == "__main__":
    main()
