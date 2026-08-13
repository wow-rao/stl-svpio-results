from __future__ import annotations
from pathlib import Path
import yaml
from stl_svpio.tasks.pointmass import run_pointmass_trial
from hyperopt import fmin, tpe, Trials, hp, STATUS_OK

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

def evaluation(temp, svgd_step_size, svgd_step_final):
    payload = yaml.safe_load(find_config().read_text(encoding="utf-8"))
    base = dict(payload["base"])
    method_cfg = dict(payload["methods"][METHOD])
    task_id = str(payload["task_id"])
    cfg = {**base, **method_cfg, "stl_temperature": temp, "svgd_step_size": svgd_step_size, "svgd_step_final": svgd_step_final}
    r = run_pointmass_trial(task_id, METHOD, cfg, seed=0, jit=True)
    return -r.true_robustness
    
def objective(args):
    return evaluation(*args)


if __name__ == "__main__":
    trials = Trials()
    best = fmin(objective, space=[hp.uniform('temp', 0.01, 1000), 
    hp.uniform('svgd_step_size', 10, 1000), 
    hp.uniform('svgd_step_final', 0.01, 1)], algo=tpe.suggest, max_evals=1000, trials=trials)

    # svgd_step_final: 0.9061219970388112
    # svgd_step_size: 910.172348945071
    # stl_temperature: 8.483839075094636
    print(best)
