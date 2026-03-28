import json
import os
import pubchempy as pcp
import sys

def check_all_scents():
    error_found = False
    # Look through every file in the scents folder
    for filename in os.listdir('scents'):
        if filename.endswith('.json'):
            with open(f'scents/{filename}', 'r') as f:
                data = json.load(f)
                
            # Ask PubChem if the CID is real
            try:
                compound = pcp.Compound.from_cid(data['cid'])
                official = compound.iupac_name.lower()
                
                # Check if the chemical name they typed matches the official one
                if data['chemical'].lower() not in official:
                    print(f"❌ Error in {filename}: '{data['chemical']}' doesn't match PubChem name '{official}'")
                    error_found = True
            except:
                print(f"❌ Error in {filename}: CID {data['cid']} is invalid!")
                error_found = True

    if error_found:
        sys.exit(1) # This tells GitHub to show a Red X
    else:
        print("✅ All smells verified and accurate!")

if __name__ == "__main__":
    check_all_scents()