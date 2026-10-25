import sys

print("Paste your FModel paths below.")
print("When you are done, press Enter, then Ctrl+Z, then Enter again (on Windows):")

try:
    input_text = sys.stdin.read()
except KeyboardInterrupt:
    sys.exit()

lines = input_text.strip().split('\n')
output_lines = ["Name,Path"]

for line in lines:
    line = line.strip()
    if not line: 
        continue
    
    # 1. Remove .uasset if it's there
    path = line.replace(".uasset", "")
    
    # 2. Get the item name (the last part of the path)
    item_name = path.split("/")[-1]
    
    # 3. Convert to UE internal path format
    if path.startswith("TallProject/Content/"):
        ue_path = path.replace("TallProject/Content/", "/Game/")
    else:
        # Fallback if it starts differently
        ue_path = "/" + path.lstrip("/")
        
    # 4. Format: Name,Path.Name_C
    final_string = f"{item_name},{ue_path}.{item_name}_C"
    output_lines.append(final_string)

csv_output = '\n'.join(output_lines)

print("\n--- YOUR CSV DATA ---\n")
print(csv_output)

# Automatically save it to a file
with open("ActorDump1.csv", "w") as f:
    f.write(csv_output)
print("\n(Saved to ActorDump1.csv in the current folder)")
