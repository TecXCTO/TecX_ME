import os
import time

def run_galvo_calibration_sweep(target_dimension_mm=50.0):
    """
    Simulates a calibration matrix sweep across the F-Theta scan lens field.
    Verifies command scaling bounds before triggering the high-power laser.
    """
    print(f"=== INITIALISING OPTICAL FIELD CALIBRATION CYCLE ({target_dimension_mm}x{target_dimension_mm}mm) ===")
    
    # 4-point corner verification coordinates (Bounding box limit checks)
    test_points = [
        {"x": 0.0, "y": 0.0, "label": "Center Origin"},
        {"x": -target_dimension_mm/2, "y": -target_dimension_mm/2, "label": "Bottom-Left"},
        {"x": -target_dimension_mm/2, "y": target_dimension_mm/2, "label": "Top-Left"},
        {"x": target_dimension_mm/2, "y": target_dimension_mm/2, "label": "Top-Right"},
        {"x": target_dimension_mm/2, "y": -target_dimension_mm/2, "label": "Bottom-Right"},
        {"x": 0.0, "y": 0.0, "label": "Center Return"}
    ]
    
    # Validation constraint flags
    calibration_successful = True
    
    for pt in test_points:
        print(f"Moving mirror optics array to [{pt['label']}] -> X: {pt['x']}mm, Y: {pt['y']}mm...")
        time.sleep(0.2) # Mimic physical motor step delays
        
        # Check electrical/mechanical threshold limits
        if abs(pt['x']) > 50.0 or abs(pt['y']) > 50.0:
            print(f"[CRITICAL ERROR] Coordinate limit breached on {pt['label']}!")
            calibration_successful = False
            break
            
    return calibration_successful

if __name__ == "__main__":
    # Test valid boundary loop
    is_safe = run_galvo_calibration_sweep(50.0)
    print(f"Optical Validation Status: {'PASSED' if is_safe else 'FAILED'}")
  
