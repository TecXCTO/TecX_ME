# Firmware Array Debugging Documentation

When compiling the translated `laser_commands.h` data array inside your Arduino control loop environment, use this validation run template to identify array sizing errors.

### Potential Errors and Resolutions

1. **`PROGMEM` Memory Overflow Error**
   * *Symptom*: Red compiler alert indicating the data allocation sizes exceeded system flash boundaries.
   * *Resolution*: Ensure you are utilizing the `PROGMEM` macro to dump coordinates onto flash storage instead of eating system dynamic SRAM. Keep single-layer vector processing maps under 5,000 discrete points.

2. **Laser Timing Lag Issues**
   * *Symptom*: Sintered tracks show rounded edge errors on crisp internal mechanical corner structures.
   * *Resolution*: Adjust the `REFRESH_RATE_MS` interval setting down inside your main control loop (`src/control/main.ino`) to match the acceleration curves of your galvo mirrors.

3. **Data Type Mismatch Faults**
   * *Symptom*: Compilation fails on the instruction mapping arrays.
   * *Resolution*: Validate that your compiler configurations are parsing true numeric structures (`float` type variables) rather than unparsed structural characters left behind during translation.
   * 
