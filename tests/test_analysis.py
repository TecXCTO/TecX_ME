# Unit tests for data pipeline


import unittest
import os
import pandas as pd
from src.analysis.thermal_pipeline import process_melt_pool_data

class TestThermalPipeline(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "data/raw/layer_001_telemetry.csv"
        self.output_dir = "assets/diagrams"
        
    def test_data_integrity(self):
        """Check if the sensor input file exists and contains valid numeric fields."""
        self.assertTrue(os.path.exists(self.test_file), "Test data tracking dependency failed.")
        df = pd.read_csv(self.test_file)
        self.assertIn('pyrometer_temp_c', df.columns)
        self.assertFalse(df['pyrometer_temp_c'].isnull().values.any(), "NaN values found in sensor logs.")

    def test_pipeline_execution(self):
        """Ensure analytics functions yield valid physical temperature thresholds."""
        metrics = process_melt_pool_data(self.test_file, self.output_dir)
        
        # Physical boundary checks for 316L stainless steel sintering
        self.assertGreater(metrics['peak_temperature_c'], 100.0)
        self.assertLess(metrics['peak_temperature_c'], 3000.0) # Below boiling point of iron
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "thermal_profile.png")))

if __name__ == '__main__':
    unittest.main()
  
