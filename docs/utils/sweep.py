import yaml, itertools
from pathlib import Path
from stl_svpio.tasks.pointmass import run_pointmass_trial

r=None
for d in [Path.cwd(),*Path.cwd().parents]:
    if (d/"configs/paper/stl_svpio_pointmass.yaml").exists(): r=d; break
if r is None: raise SystemExit("run from repo root")

pl=yaml.safe_load((r/"configs/paper/stl_svpio_pointmass.yaml").read_text())
pre={str(x["id"]):dict(x["args"]) for x in pl["presets"]}

tg={"single_visit_goals_long_horizon":0.97,"multiagent_button":1.0,
    "multiagent_sync_goals":1.0,"multiagent_corridor_6_agents":1.0}

sss=[500.0,1000.0,2000.0,5000.0]
sfs=[1.0,50.0,100.0]
tps=[100.0,500.0,1000.0]
N=10

out={}
for t in tg:
    b=dict(pre[t]); done=None; bb=(-1.0,None)
    for ss,sf,tp in itertools.product(sss,sfs,tps):
        c=dict(b); c["svgd_step_size"]=ss; c["svgd_step_final"]=sf; c["stl_temperature"]=tp
        k=0
        for sd in range(N):
            rr=run_pointmass_trial(t,"stl_svpio",c,seed=sd,jit=True)
            k+=int(rr.satisfied)
        rate=k/N
        print(t,ss,sf,tp,rate,flush=True)
        if rate>bb[0]: bb=(rate,(ss,sf,tp))
        if rate>=min(0.9,tg[t]-0.05):
            done=(ss,sf,tp,rate); break
    out[t]=done if done else ("best",)+bb
    print("==>",t,out[t],flush=True)

print(out)
