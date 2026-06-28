# 📈 Mobile LTV & ROAS Modeler

[![▶ Live Demo](https://img.shields.io/badge/▶_Live_Demo-stonedhawk.github.io-7aa2f7?style=for-the-badge)](https://stonedhawk.github.io/mobile-ltv-roas-modeler/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![No dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Single file](https://img.shields.io/badge/build-none%20·%20single%20file-blue.svg)](#)

**A dependency-free, single-file LTV & ROAS modeler for mobile game UA.** Fit a retention curve from your D1–D30 numbers, project LTV & ROAS out to D720, find your payback day, and reverse-solve the early ROAS you need to break even. Everything runs in the browser — no SDK, no backend, no data leaves the page.

### ▶ Try it live: **[stonedhawk.github.io/mobile-ltv-roas-modeler](https://stonedhawk.github.io/mobile-ltv-roas-modeler/)**

---

## 🎯 What it answers

- **What's my D30 / D180 / D360 / D720 LTV** given retention and ARPDAU?
- **When does this cohort pay back** at a given eCPI?
- **What D7 / D14 ROAS do I need** to hit 100% ROAS by D180 / D360 / D720? *(the reverse solver)*
- **What will a live campaign mature to** — project a campaign's D360 ROAS from its observed D7 ROAS.
- **What's the max eCPI I can afford**, or the ARPDAU I'd need, to make the target work?

---

## 🧮 How the model works

| Step | Formula |
|------|---------|
| **Retention fit** | Least-squares on D1/D3/D7/D14/D30 (+ optional long-horizon anchor). Power-law `R(d)=A·d^b`, exponential `R(d)=A·e^(b·d)`, or a blend. Day 0 = 1.0. |
| **Active days** | `ActiveDays(N) = 1 + Σ R(d)` for d = 1…N |
| **LTV** | `LTV(N) = Σ ARPDAU(d)·R(d)`, with `ARPDAU(d) = ARPDAU₀·(1+g)^(d/30)` |
| **ROAS** | `ROAS(N) = LTV(N) / eCPI × 100%`; payback = first day LTV ≥ eCPI |
| **Reverse solver** | Required ROAS at day E for target T% by day H: `T × LTV(E)/LTV(H)` |
| **Campaign projection** | `ROAS(Y) = ROAS_obs × LTV(Y)/LTV(X)` |

---

## ⚠️ The honest caveat

Without a long-horizon anchor, the curve is fit on **≤30 days of data**, so D360 / D720 are pure extrapolation. Two things bite in reality:

1. **Long-tail retention flattens** — a pure power-law often *under*-counts long-term survivors.
2. **ARPDAU drifts up** as low-value users churn and payers concentrate.

To keep the model honest: add a real **D60 / D90 / D180 retention point** in the *Long-horizon anchor* field to pin the tail, use the **ARPDAU growth** input, and treat far-horizon numbers as a band, not a point. The tool warns you whenever you're extrapolating past your anchored data.

---

## 🚀 Run it

Use the **[hosted version](https://stonedhawk.github.io/mobile-ltv-roas-modeler/)**, or run it locally — it's one file with no build step:

```bash
git clone https://github.com/stonedhawk/mobile-ltv-roas-modeler.git
open mobile-ltv-roas-modeler/index.html
```

---

## 📄 License

[MIT](LICENSE) — use it inside your studio or fork it freely.

---

Built by [Rahul Shah](https://github.com/stonedhawk) — 16 years producing mobile games, packaging producer problems as tools.
