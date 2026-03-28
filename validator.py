import json
import os
import pubchempy as pcp
import sys

def check_all_scents():
    error_found = False
    for filename in os.listdir('.'):
        # Only check scent JSON files in the main folder
        if filename.endswith('.json') and filename not in ['package.json', 'package-lock.json']:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # This removes ALL spaces and makes it lowercase
            user_chem = str(data['chemical']).replace(" ", "").lower()
            print(f"Checking {filename}...")
            
            try:
                compound = pcp.Compound.from_cid(data['cid'])
                # This also removes ALL spaces from the official name
                official = compound.iupac_name.replace(" ", "").lower()
                
                if user_chem not in official and official not in user_chem:
                    print(f"❌ {filename}: '{data['chemical']}' doesn't match official '{compound.iupac_name}'")
                    error_found = True
            except:
                print(f"❌ {filename}: CID {data['cid']} is invalid!")
                error_found = True

    if error_found:
        sys.exit(1)
    else:
        print("✅ All smells verified!")

if __name__ == "__main__":
    check_all_scents()
