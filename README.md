# STL-SVPIO — Reproduction Notes

This repository documents an attempt to reproduce the results of the `stl-svpio` paper.

---
## Table I — single-agent reach-avoid

**Finding: the committed pipeline does not reproduce its own reference CSV.**

A clean checkout was installed in an isolated environment with the locked `stljax==1.1.3` and run on CPU. Result versus the committed reference (`results/reference/table1_reach_avoid_summary.csv`), robustness values:

| method | reference | CPU | GPU |
|---|---|---|---|
| stl_svpio | **+0.108** | −2.471 | −2.471 |
| mppi | **+0.005** | −0.7972100 | −0.797210 |
| dpi | **+0.179** | crashes (see below) | −3.500 |

Two points make this a firm conclusion rather than an environment artifact:

1. **MPPI and STL-SVPIO is bit-identical** between the CPU run (−0.797210) and the local GPU run (−0.797210). The pipeline is deterministic, and the local environment faithfully reproduces the committed code. What fails to match is the reference, not the machine.
2. **DPI, SVMPC, and STLCG-GD cannot run as committed.** Their configs set `stl_temperature: null` while inheriting `stl_approx_method: logsumexp`, and `stljax` raises `AssertionError: need a temperature value` for that combination. A clean checkout crashes on these methods.

### Feasibility strips (reach-avoid, STL-SVPIO)

Feasibility of the single-agent reach-avoid task as `svgd_iters` is swept from 20 to 200, one strip per fixed `stl_temperature`. Feasibility is judged by the exact STL Boolean (`specification.eval`). Black = feasible, white = infeasible (convention determined by cross-checking temperature 200, the committed default, which is independently infeasible at the committed 20-iteration setting). Temperatures with no feasible iteration are omitted. Detailed band analysis is pending the full sweep.

![temperature 5](stl-svpio-results/docs/feasibility_temp_5.0.png)
![temperature 8](docs/feasibility_temp_8_0.png)
![temperature 10](docs/feasibility_temp_10_0.png)
![temperature 20](docs/feasibility_temp_20_0.png)
![temperature 50](docs/feasibility_temp_50_0.png)
![temperature 100](docs/feasibility_temp_100_0.png)
![temperature 200](docs/feasibility_temp_200_0.png)
![temperature 500](docs/feasibility_temp_500_0.png)

---

## Sweep Outcome

After setting the `stl_approx_method: "true"`, and running the sweep, from where we choose the smallest iteration where feasibility is observed (`stl_temprature: 8`, `iterations: 30`), running the experiment again yields the following table: 

| Method | Robustness | Satisifed | Runtime (ms) |
|---|---|---|---|
| stl_svpio | -0.065891 | true | 1193.984 |
| mppi | -0.924563 | false | 669.433 |
| svmpc | -1.702659 | false | 1455.776 |
| dpi | -3.500000 | false | 768.426 |
| stlcg_gradient_descent | -3.498310 | false | 412.975 |

## What is and is not claimed (Table I)

**Supported directly by data:**
- The committed repo does not regenerate its Table I reference (clean-install run; MPPI bit-identical to local; DPI/SVMPC/STLCG-GD crash on `stl_temperature: null`).

**Hypothesis (labelled, not asserted as fact):**
- The reference numbers were produced by original/dev code rather than these repackaged entry points.

---
