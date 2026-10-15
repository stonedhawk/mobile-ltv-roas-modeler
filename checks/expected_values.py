"""Independent expected values for the LTV & ROAS Modeler's worked examples.

Written from the formulas in the README and the in-tool Model section, not
from index.html, so the two share no code. The fits use numpy.polyfit in log
space. Compare the printed values with what the page shows for the same
inputs (see "Checking the math" in the README).

    pip install numpy
    python checks/expected_values.py
"""
import json
import math

import numpy as np

out = {}

ANCH = [1, 3, 7, 14, 30]


def fit(model, days, rets):
    days, rets = np.array(days, float), np.array(rets, float)
    bp, lnAp = np.polyfit(np.log(days), np.log(rets), 1)
    be, lnAe = np.polyfit(days, np.log(rets), 1)
    P = lambda d: min(max(math.exp(lnAp) * d ** bp, 0), 1)
    E = lambda d: min(max(math.exp(lnAe) * math.exp(be * d), 0), 1)
    return {"power": P, "exp": E, "blend": lambda d: min(max((P(d) + E(d)) / 2, 0), 1)}[model]


def ltv_model(rets_pct, arpdau, ecpi, model="power", g_pct=0, anchor=None, tgt=100, tgt_day=360, obs=35, obs_day=7):
    days, rets = list(ANCH), [r / 100 for r in rets_pct]
    if anchor:
        days.append(anchor[0]); rets.append(anchor[1] / 100)
    R = fit(model, days, rets)
    g = g_pct / 100
    # LTV(N) = sum_{d=0..N} ARPDAU(d) * R(d), R(0)=1
    rev = [arpdau] + [arpdau * (1 + g) ** (d / 30) * R(d) for d in range(1, 721)]
    ltv = np.cumsum(rev)
    active = np.cumsum([1] + [R(d) for d in range(1, 721)])
    pb = next((d for d in range(721) if ltv[d] >= ecpi), None)
    L = lambda n: float(ltv[n])
    be = next((y for y in range(obs_day, 721) if obs * L(y) / L(obs_day) >= 100), None)
    return dict(
        ltv30=L(30), ltv180=L(180), ltv360=L(360), ltv720=L(720), payback=pb,
        table={n: dict(active=float(active[n]), ltv=L(n), roas=L(n) / ecpi * 100) for n in [7, 14, 30, 60, 90, 180, 360, 720]},
        req_d7=tgt * L(7) / L(tgt_day), req_d14=tgt * L(14) / L(tgt_day), req_d30=tgt * L(30) / L(tgt_day),
        req_arpdau=arpdau * (ecpi * tgt / 100) / L(tgt_day), max_ecpi=L(tgt_day) * 100 / tgt,
        proj180=obs * L(180) / L(obs_day), proj360=obs * L(360) / L(obs_day), proj720=obs * L(720) / L(obs_day), be_day=be,
    )


out["ltv"] = {
    "hypercasual_preset": ltv_model([38, 18, 10, 5, 2.5], 0.06, 0.30),
    "casual_preset": ltv_model([45, 28, 18, 12, 8], 0.14, 2.00),
    "midcore_preset_h720": ltv_model([50, 35, 26, 20, 14], 0.40, 7.50, g_pct=5, tgt_day=720),
    "custom_blend_anchor": ltv_model([42, 25, 16, 10, 6], 0.20, 3.00, model="blend", g_pct=3, anchor=(90, 3),
                                     tgt=120, tgt_day=180, obs=20, obs_day=14),
    "custom_exp": ltv_model([40, 22, 14, 9, 5], 0.10, 1.20, model="exp", tgt=100, tgt_day=180, obs=30, obs_day=7),
}

print(json.dumps(out, indent=1, default=float))
