import json
import os
import pubchempy as pcp
import sys

def check_all_scents():
    error_found = False
    for filename in os.listdir('.'):
        if filename.endswith('.json') and filename not in ['package.json', 'package-lock.json']:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # .strip() removes hidden spaces, .lower() ignores Capitals
            user_chem = data['chemical'].strip().lower()
            print(f"Checking {filename}...")
            
            try:
                compound = pcp.Compound.from_cid(data['cid'])
                official = compound.iupac_name.lower()
                
                # We check if your name is PART of the official name to be safe
                if user_chem not in official and official not in user_chem:
                    print(f"❌ {filename}: '{user_chem}' != official '{official}'")
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