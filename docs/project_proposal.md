# Project Proposal: Evaluation of Metal AM Infrastructure Strategies
**Prepared by:** [Rahul Saini/ TecX Research Group]  
**Date:17 May 2026  

## 1. Objective
To determine the optimal procurement and development strategy for establishing high-precision Metal Additive Manufacturing (AM) capabilities targeting 316L Stainless Steel and Ti-6Al-4V material tracking research.

## 2. Option A: In-House Custom Open-Source Platform
This strategy leverages our established open architecture to build a specialized, transparent research bed.

### Advantages:
- **Granular Sensor Instrumentation**: Integrates custom pyrometers with custom post-processing software pipelines (`src/analysis/thermal_pipeline.py`) to map melt-pool cooling profiles in real time.
- **Microcontroller Adaptability**: Custom Arduino/C++ loops handle direct sync between galvanometer pulses and safety interlocks, allowing for non-standard laser path testing.
- **Deep Academic Value**: Students and engineers master structural hardware-software handshakes rather than treating the machine as a closed black box.

### Disadvantages:
- Prolonged development loops before achieving repeatable print densities.
- High risk of structural mechanical bottlenecks (e.g., powder layer shearing or gas purging leaks).

## 3. Option B: Commercial Readymade Infrastructure
This strategy bypasses development cycles by installing an industrial workhorse system.

### Advantages:
- **Immediate Repeatability**: Guaranteed structural print density metrics out of the box.
- **Established Support Networks**: Manufacturer warranties cover optical and high-voltage power components.
- **Built-in Safety**: Sealed atmosphere management limits toxic metallic dust and high-power optical hazards natively.

### Disadvantages:
- Prohibitive licensing fees for open-parameter software tools.
- Proprietary data structures prevent custom mathematical validation of laser-track thermodynamics.

## 4. Strategic Recommendation
For standard, high-volume production parts with verified properties, **Option B (Commercial)** is mandatory. However, for novel alloy development, deep physical research, and data integration with custom analytics pipelines, the **In-House Custom Build (Option A)** yields superior proprietary knowledge at a fraction of the hardware purchase cost.
