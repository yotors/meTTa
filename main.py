from hyperon import *
import glob

metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f'''
                !(load-ascii &space {path})
                ''')
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    print(f"Finished loading {len(paths)} datasets.")

# Example usage:
try:
    dataset = load_dataset("./Data")
   
except Exception as e:
    print(f"An error occurred: {e}")

# 2 Points
def get_transcript(node):
     #TODO Implement the logic to fetch the transcript
    transcript = metta.run(f'''
    ! (match &space (transcribed_to ({node[0]}) $x) (transcribed_to ({node[0]}) $x))
''')
    return transcript[0]

#2 Points
def get_protein(node):
    #TODO Implement the logic to fetch the protein
    protein = metta.run(f'''
    ! (match &space (transcribed_to ({node[0]}) $x) (match &space 
(translates_to $x $y) 
(translates_to $x $y)))
''') 
    return protein[0]

#6 Points
def metta_seralizer(metta_result):
    #TODO Implement logic to convert the Metta output into a structured format  (e.g., a list of dictionaries) that can be easily serialized to JSON.
    
    resul = metta_result[0].get_children()
    source = " ".join([i.get_name() for i in resul[1].get_children()])
    target = " ".join([i.get_name() for i in resul[2].get_children()])
    result = {"edge": resul[0].get_name(), "source": source, "target": target}
    return result



#1
transcript_result= (get_transcript(['gene ENSG00000166913']))
print(transcript_result) 
"""
Expected Output Format::
# [[(, (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))), (, (transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)))]]
""" 

#2
protein_result= (get_protein(['gene ENSG00000166913']))
print(protein_result) 
"""
Expected Output Format::
# [[(, (translates_to (transcript ENST00000353703) (protein P31946))), (, (translates_to (transcript ENST00000372839) (protein P31946)))]]
"""

#3
parsed_result = metta_seralizer(transcript_result)
print(parsed_result) 
"""
Expected Output Format:
[
    {'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}
]
"""

