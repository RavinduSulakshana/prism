# DESIGN SPEC — single source of truth for the report AND the code

Author: P R S Perera (Student ID 29243), BSc (Hons) Computer Science (UGC)
Supervisor: Ms. Hirushi Dilpriya
Title: **PRISM: A LiDAR-Driven, PCU-Weighted Pressure-Based Adaptive Traffic Signal Controller for Heterogeneous Sri Lankan Traffic — A Drone-Calibrated SUMO Study of the Maviththara Junction**
(PRISM = Pressure-based Real-time Intersection Signal Management)

Report is written in past tense "as built". Every number that must later be replaced by a measured
value is wrapped in `\est{...}` (renders highlighted; switch off in main.tex with `\estfinaltrue`).
Algorithm parameters (design choices) are NOT wrapped — they are the spec.

---------------------------------------------------------------------------------------------------
## 1. Study site
- Maviththara Junction, Piliyandala, on the Piliyandala bypass road, Colombo District, Western Province.
- 4-arm signalised intersection. Each arm: 2 lanes inbound + 2 lanes outbound (undivided/divided, no
  dedicated turn pockets). Left-hand traffic (Sri Lanka drives on the left), so RIGHT turns cross opposing flow.
- Arms named North (N), East (E), South (S), West (W). (Report says arm-to-road mapping in Appendix; user fills.)
- Current control: fixed-time. At severe congestion traffic police switch lights off and direct traffic manually
  (outside scope of simulation; discussed as motivation + limitation).
- Current fixed-time plan (as observed from footage): cycle `\est{120 s}`, split phasing, greens
  N `\est{32}`, E `\est{24}`, S `\est{32}`, W `\est{12}` s, each phase followed by 3 s amber + 2 s all-red
  (4 × 5 = 20 s lost) → 32+24+32+12+20 = 120 s.

## 2. Data collection
- DJI-class drone hovering, nadir (straight-down) view, fixed position over the junction.
- Date: 2 October 2026. Session M (morning peak, high congestion) 07:00–08:00. Session A (afternoon, moderate) 13:30–14:30.
- Video: `\est{3840×2160 @ 30 fps}`, altitude `\est{≈90 m}`. Processed at 10 fps (every 3rd frame).
- Development order (MUST be stated): (1) mock-data phase first — synthetic demand split evenly across the four
  approaches and fixed turning ratios — used to develop and unit-test the controller and the simulated LiDAR;
  (2) drone-data phase LAST — real demand extracted from footage replaced the mock demand and calibrated the model.
- Ethics: altitude makes faces/number plates unidentifiable; no personal data stored; only anonymous trajectories; permission/ CAA rules for drone flight mentioned (user to confirm).

## 3. Vehicle classes and PCU (Sri Lanka)
| class | SUMO vClass | length m | PCU | max speed km/h |
|---|---|---|---|---|
| motorcycle | motorcycle | 2.0 | 0.5 | 70 |
| three-wheeler | (custom vType "threewheeler", vClass passenger, guiShape "passenger/hatchback"?) use vClass=private? -> use `vClass="passenger"` with width 1.4 | 2.7 | 0.8 | 50 |
| car | passenger | 4.5 | 1.0 | 70 |
| van / SUV | delivery | 5.0 | 1.0 | 70 |
| bus | bus | 11.5 | 3.0 | 60 |
| lorry / truck | truck | 8.5 | 2.5 | 55 |
| bicycle | bicycle | 1.8 | 0.3 | 20 |
PCUs adapted from Sri Lankan RDA / literature for urban mixed traffic (state as "adopted values").
Observed composition (placeholder, `\est{}`): Morning: motorcycle 38%, three-wheeler 24%, car 21%, van 7%, bus 6%, lorry 3%, bicycle 1%.
Afternoon: motorcycle 34%, three-wheeler 27%, car 22%, van 8%, bus 5%, lorry 3%, bicycle 1%.

## 4. Data-extraction algorithm (drone → SUMO). Name: **DTX (Drone Trajectory eXtractor)**
1. Frame stabilisation: ORB features + RANSAC homography to a reference frame (first frame) every frame; warp. Removes hover drift.
2. Detection: **YOLOv8s** (Ultralytics), initialised from weights pre-trained on **VisDrone2019-DET** (aerial dataset; its
   "awning-tricycle"/"tricycle" classes are close to Sri Lankan three-wheelers), then **fine-tuned** on frames from our own footage:
   `\est{450}` frames manually annotated in CVAT/Roboflow, 7 classes above, split 70/15/15, 100 epochs, imgsz 1280,
   SAHI-style tiling (slicing 2×2 tiles with overlap 0.2) because vehicles are small (motorbike ≈ 20 px).
   Justification vs YOLO11/RT-DETR/Faster R-CNN: maturity, speed, tooling, small-object performance with tiling, single-stage; anchor-free.
   Results (placeholders): mAP@0.5 `\est{0.86}`, mAP@0.5:0.95 `\est{0.58}`; per-class AP@0.5 motorcycle `\est{0.81}`, three-wheeler `\est{0.88}`,
   car `\est{0.93}`, van `\est{0.84}`, bus `\est{0.95}`, lorry `\est{0.87}`, bicycle `\est{0.62}`.
3. Tracking: **ByteTrack** (associates high- and low-confidence boxes; good under occlusion, no re-ID network needed since top-down).
   Track params: track_thresh 0.5, match_thresh 0.8, track_buffer 30 frames. Class of a track = majority vote over its frames.
   Tracking quality (placeholder on a 2-minute manually annotated clip): MOTA `\est{0.82}`, IDF1 `\est{0.79}`, ID switches `\est{14}`.
4. Pixel→metre: planar homography H from ≥4 ground control points (lane-marking corners, stop-line ends) whose metre
   coordinates come from measured lane widths (3.5 m) / satellite imagery. Ground sample distance ≈ `\est{2.6 cm/px}`.
5. Trajectory smoothing: Savitzky–Golay filter (window 11 samples, order 2) on x,y; speed v = |Δp|/Δt.
6. Zoning: polygons for each approach (inbound) and each exit (outbound), plus stop-line segments. Movement = (entry arm, exit arm)
   → turning movement counts (left / through / right / U).
7. Waiting time (user's original idea refined): a vehicle "waits" in any sample where v < 0.1 m/s (same threshold SUMO uses for
   waitingTime) while inside an approach zone. Per-vehicle waiting time W = Σ Δt over those samples. Also time-in-frame
   T_frame = t_exit − t_entry, and control delay d = T_frame − L_path / v_free. Tracks that start or end inside the
   frame at video boundaries are censored and excluded from averages (but included in counts).
8. Derived calibration quantities: arrival flow per approach per class per 5-min bin (veh/h and PCU/h);
   turning ratios; saturation flow s from queue discharge headways (headways of 4th+ vehicle after green start), giving
   `\est{1850 PCU/h/lane}`; max/avg queue length per approach (m); free-flow speed `\est{38 km/h}`; observed signal timings.
9. Output: SUMO `.rou.xml` (vTypeDistribution per session + `<flow>` per movement per 5-min bin) and a CSV of observed
   KPIs for calibration.
Observed (placeholder) demand: Morning total `\est{3,420 veh/h}` (`\est{2,610 PCU/h}`); Afternoon `\est{2,280 veh/h}` (`\est{1,720 PCU/h}`).
Observed avg waiting time under existing fixed-time: Morning `\est{104.7 s}`, Afternoon `\est{46.3 s}`.

## 5. SUMO model
- SUMO `\est{1.20.0}` (user to confirm), Python 3.11, TraCI (libsumo for speed in batch runs).
- Network: OpenStreetMap export (osmWebWizard / netconvert) of ≈ 400 m on each arm, cleaned in netedit: 2+2 lanes, lefthand=true,
  junction type traffic_light, custom TLS program.
- Heterogeneous traffic: **sublane model** (`--lateral-resolution 0.8`), `lcSublane`, `minGapLat 0.3` for motorcycles so they
  filter between cars and reach the stop line (typical Sri Lankan behaviour). Car-following Krauss; sigma 0.5 (Sri Lankan driver
  imperfection), tau 1.0; three-wheeler accel 1.8 m/s², motorcycle accel 2.8 m/s².
- Simulation: step length 0.5 s... (use 1.0 s for controller decisions, SUMO step 0.5 s). Warm-up 300 s discarded, 3600 s measured.
- 10 random seeds per scenario. Output via tripinfo + summary + queue outputs + emissions (HBEFA4).
- Calibration: GEH statistic on hourly approach counts (GEH < 5 for ≥ 85% of movements: achieved `\est{100% approaches / 91.7% movements}`),
  and queue length / travel time error. Tuned params: sigma, tau, minGap, lcSublane, speedFactor distribution (normc(1,0.1)).
  Calibrated mean absolute percentage error (MAPE) of avg waiting time vs observed: `\est{8.4%}` morning, `\est{6.9%}` afternoon.

## 6. Simulated LiDAR — **VLS (Virtual LiDAR Sensor)**
- Pole-mounted virtual 360° LiDAR at junction centre, height 6 m; effective range R = 75 m (modelled on a 32-channel unit,
  e.g. Ouster OS1-32 / Velodyne class; name as "comparable to").
- Each control step (1 s) via TraCI: get all vehicles; keep those with distance ≤ R.
- Error model:
  - Position noise: Gaussian σ = 0.10 m + 0.002·r (r = range).
  - Range-dependent dropout: p_miss(r) = 0.01 + 0.04·(r/R)².
  - Occlusion: 2-D ray casting in the horizontal plane; target hidden if a vehicle of height ≥ 2.5 m (bus/lorry) is between
    sensor and target and overlaps ≥ 70% of target's angular extent. (Sensor height 6 m means low vehicles do not occlude.)
  - Class confusion: output "size class" from bounding-box length: small (<3.2 m: motorcycle/bicycle/3W), medium (3.2–6 m), large (>6 m);
    PCU from size class: small→0.6, medium→1.0, large→2.8 (controller never sees ground-truth class).
  - Clutter/false positives: Poisson λ = 0.2 per scan placed uniformly in range.
- Perception tracker: nearest-neighbour association with gating (2.5 m) + α–β filter (α=0.85, β=0.005... use α=0.5, β=0.1)
  to estimate speed; tracks confirmed after 2 hits, deleted after 3 misses.
- Output per scan: list of objects {x, y, v, heading, size class, PCU, lane/approach (map-matched by polygon), distance to stop line}.

## 7. Control algorithm — **PRISM** (pure math, no ML)
Phases: 4-phase split phasing φ ∈ {N, E, S, W} (each approach gets its own green serving L/T/R; required because no turn pockets
and right turns conflict). Interphase: amber Y = 3 s, all-red R = 2 s.
Constraints: G_min = 10 s, G_max = 60 s (morning heavy mode G_max = 75 s), max red (starvation cap) T_starve = 120 s,
pedestrian minimum: if pedestrian demand flag then G_min_ped = 15 s (future work/push buttons; parameter only).

State per approach a (from VLS only):
- Q_a = Σ PCU of objects in approach a with v < 1.4 m/s (≈5 km/h) and distance to stop line ≤ 75 m (queued).
- A_a = Σ PCU of moving objects in approach a with ETA = d/v ≤ H, horizon H = 10 s (arriving soon).
- D_a = PCU occupancy of the outbound links fed by a (weighted by turning ratios r_{a→b} from DTX), normalised by downstream
  capacity C_b (PCU that fit in 75 m × 2 lanes ≈ 2·75/6.5 ≈ 23 PCU).
- R_a = time since approach a last had green (red time), seconds.
- W_a = max accumulated waiting time of any vehicle in approach a (from VLS tracks).

Pressure (Varaiya max-pressure adapted to PCU and to partial observability):
  P_a = (Q_a + γ·A_a) · (1 − min(1, D_a / C_down)) ...
Final form used:
  P_a = Q_a + γ·A_a − δ·Σ_b r_{a→b}·O_b ,  γ = 0.5, δ = 0.6, O_b = outbound PCU occupancy on exit b.
Urgency (fairness) multiplier:
  U_a = 1 + κ·(R_a / T_starve)²,  κ = 1.5.
Score: S_a = max(P_a, 0) · U_a.

Green-time estimate for the chosen phase (queue-clearance, Webster/Greenshields style):
  G_req(a) = clip( l_s + Q_a · h_s / n_lanes + γ·A_a·h_s / n_lanes , G_min, G_max )
  with start-up lost time l_s = 2.0 s, saturation headway per PCU h_s = 3600/s = 3600/1850 ≈ 1.95 s, n_lanes = 2.

Decision procedure (runs every Δ = 1 s):
1. During green of phase g, elapsed t_g:
   a. if t_g < G_min → continue.
   b. if t_g ≥ G_max → terminate.
   c. if any approach j ≠ g has R_j ≥ T_starve → terminate (fairness override).
   d. Gap-out: if Q_g ≈ 0 (≤ 0.5 PCU) and no object in approach g with ETA ≤ gap time τ_gap = 3 s → terminate.
   e. Pressure switch: if max_{j≠g} S_j > (1 + θ)·S_g + ε (hysteresis θ = 0.25, ε = 2 PCU) AND t_g ≥ G_req(g)·ρ (ρ = 0.6,
      ensures the existing queue mostly discharged) → terminate.
   f. otherwise extend by 1 s.
2. On terminate: amber 3 s + all-red 2 s. Next phase = argmax_{j≠g} S_j evaluated at end of all-red (acyclic), except that
   any approach with R_j ≥ T_starve is served first (oldest first). Ties → fixed rotation order N→E→S→W.
3. Heavy-congestion (spillback) mode: if any exit occupancy O_b / C_b > 0.85, the controller reduces δ effect by holding
   phases that feed b to G_min (prevents gridlock in junction box) — "spillback guard".
4. Fail-safe: if VLS returns no data for 5 consecutive scans (sensor failure) → fall back to the observed fixed-time plan.
Complexity: O(n) per step in number of detected objects; < 1 ms per decision `\est{0.4 ms}` mean on laptop.

Mock-data phase parameters: demand per approach equal: low 300, medium 500, high 700 veh/h per approach; turning ratios
L 25% / T 50% / R 25%; composition equal to Sri Lankan national registration mix approximation (motorcycle 40, 3W 20, car 25,
van 7, bus 5, lorry 3). Used for: unit tests, verification of phase safety (no conflicting greens), parameter sweep.
Parameter tuning: grid search on mock + afternoon training seeds (seeds 1–5), evaluation on held-out seeds (6–15) → 10 eval seeds.

## 8. Baselines
B1 Fixed-time (observed current plan, §1). B2 SUMO built-in actuated (gap-based, `type="actuated"`, minDur 10, maxDur 60,
same phases). B3 Webster-optimised fixed-time (recomputed from DTX demand) — gives a fair "best fixed" comparison.
Proposed: PRISM with VLS (noisy). Also an "oracle" variant PRISM-GT (ground-truth sensor) to quantify sensor-noise cost.

## 9. Results (ALL placeholders, wrap every number in \est{}) — mean over 10 seeds (±sd)
Average waiting time per vehicle (s):
| scenario | Fixed | Actuated | Webster | PRISM | PRISM-GT | PRISM vs Fixed |
|---|---|---|---|---|---|---|
| Mock (500 veh/h/approach) | 41.8±1.9 | 35.6±1.7 | 37.9±1.8 | 32.1±1.5 | 31.4±1.4 | −23.2% |
| Afternoon (moderate) | 47.9±2.3 | 42.6±2.1 | 44.0±2.2 | 38.9±1.9 | 37.8±1.8 | −18.8% |
| Morning (high) | 108.6±5.4 | 103.9±5.9 | 101.7±5.1 | 96.2±4.8 | 94.5±4.6 | −11.4% |
Average travel time through 400 m arms (s): Afternoon Fixed 96.4 → PRISM 87.1 (−9.6%); Morning 168.2 → 155.3 (−7.7%).
Average queue length (m, mean over approaches): Afternoon 38.5 → 31.2 (−19.0%); Morning 92.4 → 83.7 (−9.4%).
Max queue (m): Afternoon 112 → 94; Morning 268 → 241.
Throughput (veh/h completed): Afternoon 2,262 → 2,271 (+0.4%, demand-limited); Morning 3,118 → 3,241 (+3.9%).
95th percentile waiting time (s): Afternoon 118 → 101; Morning 246 → 228.
Max waiting (fairness) — PRISM never exceeded T_starve-driven bound: max red 120 s.
Stops per vehicle: Afternoon 1.42 → 1.21; Morning 2.86 → 2.57.
CO2 (kg/h, HBEFA4): Afternoon 612 → 571 (−6.7%); Morning 1,104 → 1,048 (−5.1%).
Statistical test: Wilcoxon signed-rank on paired seeds, PRISM vs Fixed p < 0.01 both real scenarios; PRISM vs Actuated p < 0.05.
Per-class waiting (afternoon, s) Fixed→PRISM: motorcycle 39.2→31.5, 3W 46.0→37.8, car 48.7→39.6, bus 55.1→44.2, lorry 57.3→47.9.
Sensor sensitivity (afternoon, PRISM avg wait s) vs position noise σ0 ∈ {0, 0.1, 0.3, 0.5, 1.0} m: 37.8, 38.9, 39.4, 40.3, 42.7;
vs dropout p ∈ {0, 0.05, 0.1, 0.2, 0.3}: 37.9, 38.9, 39.8, 41.6, 44.9 (still better than Fixed 47.9 until ≈ 0.3).
Parameter sensitivity (afternoon): θ ∈ {0, 0.1, 0.25, 0.5}: 40.8 (oscillation, more switches), 39.3, 38.9, 39.7; G_max ∈ {45,60,75,90}: 39.6, 38.9, 39.1, 40.0.
Phase switches per hour: Fixed 120 (30 cycles × 4), PRISM afternoon 141, morning 108.
Controller compute time: mean 0.4 ms, max 2.1 ms per decision; VLS scan simulation 3.2 ms mean.
Sim wall clock: 1 h simulated ≈ 95 s with libsumo on a laptop (`\est{}`).

## 10. Code layout (to be built — describe in Implementation chapter)
```
prism-traffic/
  extraction/        # DTX
    stabilise.py  detect.py (YOLOv8+SAHI) track.py (ByteTrack) georef.py (homography) trajectories.py
    metrics.py (waiting, flows, turning, headways)  export_sumo.py  config/zones_maviththara.json
  sumo/
    net/maviththara.net.xml  routes/{mock,morning,afternoon}.rou.xml  vtypes.add.xml  maviththara.sumocfg
  sensing/
    virtual_lidar.py (VLS: noise, dropout, occlusion)  perception_tracker.py (NN + alpha-beta)
  control/
    prism.py (state estimation, pressure, decision) baselines.py (fixed, webster) phases.py
  experiments/
    run_experiment.py  scenarios.yaml  analysis.ipynb  stats.py
  tests/  (pytest: phase safety, VLS noise stats, pressure calc, gap-out, starvation)
```
Tools: Python 3.11, Ultralytics 8.x, SAHI, supervision (ByteTrack), OpenCV, NumPy/SciPy/Pandas, Matplotlib, SUMO + TraCI/libsumo,
pytest, Git/GitHub, CVAT or Roboflow for annotation, Google Colab GPU (T4) for fine-tuning.

## 11. Future work (user's vision)
City-scale: every junction equipped with LiDAR + PRISM; neighbouring junctions share predicted platoons (green-wave coordination,
decentralised max-pressure has network throughput-optimality guarantees); a cloud "junction graph" publishes predicted
per-junction delays; a route-planning app gives a commuter leaving home the minimum-time route (time-dependent shortest path,
e.g. time-dependent Dijkstra/A* using predicted signal delays) and optionally green-light speed advisory (GLOSA). Real LiDAR
pilot at Maviththara; pedestrian & emergency-vehicle priority; police override integration; bus priority; edge deployment on
Jetson; more drone sessions (weekends, rain, school-hours).
