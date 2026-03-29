import json
import os
import pubchempy as pcp
import sys

def check_all_scents():
    error_found = False
    # Get files and sort them so the log is predictable
    files = sorted(os.listdir('.'))
    
    for filename in files:
        if filename.endswith('.json') and filename not in ['package.json', 'package-lock.json']:
            # PRINT FIRST so we know which file we are attempting to open
            print(f"Opening {filename}...") 
            
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                user_chem = str(data.get('chemical', '')).replace(" ", "").lower()
                
                try:
                    compound = pcp.Compound.from_cid(data['cid'])
                    official = compound.iupac_name.replace(" ", "").lower()
                    
                    if user_chem not in official and official not in user_chem:
                        print(f"❌ {filename}: '{data['chemical']}' doesn't match official '{compound.iupac_name}'")
                        error_found = True
                except Exception as e:
                    print(f"❌ {filename}: CID {data.get('cid')} is invalid or PubChem error!")
                    error_found = True
                    
            except json.JSONDecodeError as e:
                print(f"❌ {filename} has a syntax error: {e}")
                error_found = True
                # Continue to next file instead of crashing the whole script
                continue 

    if error_found:
        sys.exit(1)
    else:
        print("✅ All smells verified!")

if __name__ == "__main__":
    check_all_scents()
