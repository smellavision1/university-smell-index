import json
import os
import pubchempy as pcp
import sys

def check_all_scents():
    error_found = False
    # Look through every file in the current folder
    for filename in os.listdir('.'): 
        # Only check .json files, but skip the ones that aren't scents
        if filename.endswith('.json') and filename not in ['package.json', 'package-lock.json']:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            print(f"Checking {filename}...")
            try:
                compound = pcp.Compound.from_cid(data['cid'])
                official = compound.iupac_name.lower()
                
                if data['chemical'].lower() not in official:
                    print(f"❌ Error in {filename}: '{data['chemical']}' doesn't match PubChem name")
                    error_found = True
            except:
                print(f"❌ Error in {filename}: CID {data['cid']} is invalid!")
                error_found = True

    if error_found:
        sys.exit(1)
    else:
        print("✅ All smells verified!")

if __name__ == "__main__":
    check_all_scents()