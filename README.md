# STL-SVPIO — Reproduction Notes

This repository documents an attempt to reproduce the results of the `stl-svpio` paper.

---
## Table I — single-agent reach-avoid

**Finding: the committed pipeline does not reproduce its own reference CSV.**

A clean checkout was installed in an isolated environment with the locked `stljax==1.1.3` and run on CPU. Result versus the committed reference (`results/reference/table1_reach_avoid_summary.csv`), robustness values:

| method | reference | CPU | GPU |
|---|---|---|---|
| stl_svpio | **+0.108** | −2.471 | −0.399 |
| mppi | **+0.005** | −0.797210 | −0.797210 |
| dpi | **+0.179** | crashes (see below) | −3.500 |

Two points make this a firm conclusion rather than an environment artifact:

1. **MPPI is bit-identical** between the clean CPU run (−0.797210) and the local GPU run (−0.797210). MPPI has no gradient path, so it is deterministic given the seed, and the local environment reproduces the committed code exactly — yet it does not match the reference. STL-SVPIO is *not* bit-identical across devices (−2.471 CPU vs −0.399 GPU) because it is gradient-based and sensitive to platform/math-library differences, but both values still fail. What fails to match the reference is the committed code, not the machine.
2. **DPI, SVMPC, and STLCG-GD cannot run as committed.** Their configs set `stl_temperature: null` while inheriting `stl_approx_method: logsumexp`, and `stljax` raises `AssertionError: need a temperature value` for that combination. A clean checkout crashes on these methods.

### Feasibility strips (reach-avoid, STL-SVPIO)

Feasibility of the single-agent reach-avoid task as `svgd_iters` is swept from 20 to 200, one strip per fixed `stl_temperature`. Feasibility is judged by the exact STL Boolean (`specification.eval`). Black = feasible, white = infeasible. Temperatures with no feasible iteration are omitted. A surprising result here is that though we see feasibility occur early in the run, it eventually looses the feasibility before coming back, this fluctuation is present across all temperature ranges.

![temperature 5](./docs/feasibility_temp_5.0.png)

![temperature 8](./docs/feasibility_temp_8.0.png)

![temperature 10](./docs/feasibility_temp_10.0.png)

![temperature 20](./docs/feasibility_temp_20.0.png)

![temperature 50](./docs/feasibility_temp_50.0.png)

![temperature 100](./docs/feasibility_temp_100.0.png)

![temperature 200](./docs/feasibility_temp_200.0.png)

![temperature 500](./docs/feasibility_temp_500.0.png)

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

---

## Figure 3 — point-mass benchmark (STL-SVPIO, before vs after sweep-tuning)

The committed Figure 3 presets do not reproduce the paper's near-total satisfaction for STL-SVPIO. Re-running STL-SVPIO with the sweep-tuned configuration (`stl_approx_method: "true"`, larger step / higher temperature from the per-task sweep) improves some tasks substantially but does **not** recover the paper's result uniformly. All values are satisfaction rate and mean STL robustness over 100 seeds; the paper reference is the target.

| task | satisfaction (before) | satisfaction (after) | paper | mean ρ (before) | mean ρ (after) |
|---|---|---|---|---|---|
| multiagent_corridor_6_agents | 0.39 | **0.77** | 1.00 | +0.002 | **+0.064** |
| multiagent_sync_goals | 1.00 | 1.00 | 1.00 | +0.335 | +0.409 |
| multiagent_button | 0.47 | 0.38 | 1.00 | −0.171 | −0.064 |
| single_visit_goals_long_horizon | 0.01 | 0.02 | 0.97 | −1.126 | −1.261 |
| **mean** | **0.47** | **0.54** | 0.99 | | |

![figure 3 before vs after](./docs/figure3_before_after.png)

**What the data shows (precisely):**

- **Corridor improved markedly:** 0.39 → 0.77, with mean robustness moving from the boundary (+0.002) to clearly positive (+0.064). This is the main gain from tuning.
- **Sync goals stayed solved:** 1.00 → 1.00; mean robustness rose (+0.335 → +0.409). It was already at the ceiling, so tuning could not improve the rate.
- **Button did not improve:** satisfaction fell 0.47 → 0.38, even though its mean robustness rose (−0.171 → −0.064). The per-seed distribution tightened (std 0.488 → 0.305) around a mean that is still below zero, so fewer seeds cross the feasibility boundary despite the better average. Higher mean, lower satisfaction.
- **Single-visit (long horizon) remains unsolved:** 0.01 → 0.02, mean robustness essentially unchanged and still strongly negative (−1.126 → −1.261).

> The "after" run covers STL-SVPIO only; the baseline methods were not re-run.

The following graph was constructed from the first run of the codebase without tuning and actually compares between baselines. The graph clearly shows that though the quantitative results of the paper does not hold from the given configuration, the qualitative result that STL-SVPIO is superior to other methods still hold.  

![figure 3 before vs after](./docs/figure3_reproduction.png)

---
