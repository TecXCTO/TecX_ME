import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def process_melt_pool_data(file_path, output_dir="assets/diagrams"):
    """
    Parses melt pool pyrometer logs, filters out thermal noise,
    and exports a layer thermal profile plot.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Sensor log not found at {file_path}")
        
    # Read telemetry data: columns = [timestamp_ms, laser_power_w, pyrometer_temp_c]
    df = pd.read_csv(file_path)
    
    # Filter sensor noise using a rolling median window
    df['clean_temp'] = df['pyrometer_temp_c'].rolling(window=5, center=True).median()
    
    # Calculate key thermal research metrics
    peak_temp = df['clean_temp'].max()
    mean_temp = df['clean_temp'].mean()
    cooling_rate = np.gradient(df['clean_temp'].values, df['timestamp_ms'].values / 1000.0)
    max_cooling_rate = np.min(cooling_rate) # Most negative value represents fastest cooling
    
    # Generate Academic-grade Validation Plot
    plt.figure(figsize=(8, 4.5), dpi=300)
    plt.plot(df['timestamp_ms'] / 1000.0, df['clean_temp'], color='#d95f02', label='Filtered Pyrometer Data')
    plt.axhline(y=1370, color='black', linestyle='--', label='316L Stainless Steel Melting Point (1370°C)')
    
    plt.title("Melt Pool Thermal History Validation", fontsize=12, fontweight='bold')
    plt.xlabel("Time (s)", fontsize=10)
    plt.ylabel("Temperature (°C)", fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, "thermal_profile.png")
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    
    return {
        "peak_temperature_c": float(peak_temp),
        "mean_temperature_c": float(mean_temp),
        "max_cooling_rate_c_per_s": float(max_cooling_rate)
    }

if __name__ == "__main__":
    # Create mock dummy data folder structure for test validation if missing
    os.makedirs("data/raw", exist_ok=True)
    mock_path = "data/raw/layer_001_telemetry.csv"
    
    if not os.path.exists(mock_path):
        time_steps = np.linspace(0, 10, 100)
        # Simulate heating up past melting point, then rapid cooling
        temp_sim = 25 + 1500 / (1 + np.exp(-2 * (time_steps - 3))) - 400 / (1 + np.exp(-1 * (time_steps - 7)))
        mock_df = pd.DataFrame({
            "timestamp_ms": time_steps * 1000,
            "laser_power_w": [200 if 2 < t < 7 else 0 for t in time_steps],
            "pyrometer_temp_c": temp_sim + np.random.normal(0, 15, len(time_steps))
        })
        mock_df.to_csv(mock_path, index=False)
        
    metrics = process_melt_pool_data(mock_path)
    print(f"Data Pipeline Verified successfully.\nMetrics: {metrics}")
  
