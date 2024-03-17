from pymatgen.core.composition import Composition
import pandas as pd
import re

# Example lists
# list1 = ["Zr99.9Cu0.05Ni0.05", "Zr99.999Cu0.0005Ni0.0005", "Zr99.5Cu0.5", "Zr99Cu1Ni0.01", "C0.3Si0.7"]
# list2 = ["Zr99.9Cu0.05Ni0.05", "Zr99.99Cu0.005Ni0.005", "Zr99.5Cu0.5", "Zr99Cu1Ni0.01", "Si14 C6"]

def check_equivalence(list1, list2):
    duplicates = set()
    print("\t\t| List1 -> List2 |")
    state = False
    for element1 in list1:
        # print(element1[0]) # for debugging
        composition1 = Composition(element1[0])
        normalized_composition1 = composition1.get_integer_formula_and_factor()[0]

        for element2 in list2:
            composition2 = Composition(element2)
            normalized_composition2 = composition2.get_integer_formula_and_factor()[0]

            if normalized_composition1 == normalized_composition2:
                if element1[0] in duplicates:
                    continue
                duplicates.add(element1[0])
                print(f"Equivalent: {element1[0]} and {element2}")
                # If you only want to check if any equivalence exists, you can return True here
                state = True
    # If no equivalence is found after looping through both lists
    print("No equivalence found.") if not state else None
    return state

def read_GPT():
    alloys = []
    # Open the text file
    with open('Metallicglasscriticalcastingdiameter_2024_03_11-012720.txt', 'r') as file:
        lines = file.readlines()

        pattern = r'\|\s*([^Material][\w\d.]+)\s*\|\s*([^Value][a-z\.\d\s]+)\s*\|'

        # Loop through the lines in the file
        for line in lines:
            match = re.match(pattern, line)  # Match the pattern in the line
            if match:
                material, value = match.group(1), match.group(2)  # Extract material and value
                alloys.append((material, value))  # Append to the alloys list
    
    return alloys

def main():
    # Print the list of alloys
    list1 = read_GPT()
    
    df = pd.read_csv("full_data.csv")

    # df = pd.read_csv("MDF_DMREF_Metallic_Glasses_v7.csv")
    list2 = df.iloc[:, 0].tolist()
    print(check_equivalence(list1, list2))

# Check for equivalence
if __name__ == "__main__":
    main()
