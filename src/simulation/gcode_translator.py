import os
import re

def translate_gcode_to_laser_commands(gcode_path, output_path="src/control/laser_commands.h"):
    """
    Parses standard 3D printer G-Code and extracts coordinates 
    to generate timing variables for the laser optics array.
    """
    if not os.path.exists(gcode_path):
        raise FileNotFoundError(f"G-Code file not found at {gcode_path}")
        
    commands = []
    
    # Regular expressions to catch coordinates and laser states
    # G1 = Move, X/Y = Coordinates, E = Extrusion (Laser On)
    g1_pattern = re.compile(r"G1\s+X([-+]?\d*\.\d+|\d+)\s+Y([-+]?\d*\.\d+|\d+)(?:\s+E([-+]?\d*\.\d+|\d+))?")
    
    with open(gcode_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(";"): # Ignore comments
                continue
                
            match = g1_pattern.match(line)
            if match:
                x_val = float(match.group(1))
                y_val = float(match.group(2))
                # If extrusion (E) value is positive, trigger laser high
                laser_state = "HIGH" if match.group(3) and float(match.group(3)) > 0 else "LOW"
                commands.append(f"    {{ {x_val:.3f}, {y_val:.3f}, {laser_state} }}")
                
    # Format commands directly into an include header file for the Arduino compiler
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as out_file:
        out_file.write("// Automatically generated instruction matrix for Metal AM Laser\n")
        out_file.write("struct LaserInstruction {\n    float x;\n    float y;\n    int state;\n};\n\n")
        out_file.write(f"const int INSTRUCTION_COUNT = {len(commands)};\n")
        out_file.write("const LaserInstruction instructionMap[] PROGMEM = {\n")
        out_file.write(",\n".join(commands))
        out_file.write("\n};")
        
    return len(commands)

if __name__ == "__main__":
    # Generate a sample mock G-Code layer print path for execution testing
    os.makedirs("src/simulation", exist_ok=True)
    mock_gcode = "src/simulation/sample_layer.gcode"
    
    with open(mock_gcode, 'w') as f:
        f.write("; Layer 1 Test Path\n")
        f.write("G1 X0.000 Y0.000 E0.0\n")  # Travel move (Laser Off)
        f.write("G1 X10.500 Y20.300 E1.0\n") # Sintering line (Laser On)
        f.write("G1 X30.000 Y20.300 E1.0\n") # Sintering line (Laser On)
        f.write("G1 X0.000 Y0.000 E0.0\n")  # Travel move (Laser Off)
        
    count = translate_gcode_to_laser_commands(mock_gcode)
    print(f"Successfully processed {count} vectors into machine instructions header.")
