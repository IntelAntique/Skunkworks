import pandas as pd
from pymatgen.core.composition import Composition

# Read data from CSV files
llm_data = pd.read_csv('metallic.csv')
gtd_data = pd.read_csv('full_data.csv')

# Function to check if two compositions are the same
def is_same_composition(comp1, comp2):
    return Composition(comp1).reduced_formula == Composition(comp2).reduced_formula

# Function to check if the values deviate from the database by within 100%
def is_within_0_5(value1, value2):
    return abs(value1 - value2) <= value2

if False:
# Initialize counters
    true_count = 0
    false_count = 0
    unknown_count = 0

    # Keep track of unique LLM materials
    processed_materials = set()

    # Iterate through each row in the llm_data DataFrame
    for index, llm_row in llm_data.iterrows():
        llm_material = llm_row['Material']

        # Skip if the material has already been processed
        if llm_material in processed_materials:
            continue

        processed_materials.add(llm_material)

        llm_value = llm_row['Value']

        # Check if LLM material matches a GTD entry
        matching_gtd_entries = gtd_data[gtd_data['composition'].apply(lambda x: is_same_composition(x, llm_material))]

        if not matching_gtd_entries.empty:
            # LLM material matches a GTD entry
            for _, gtd_row in matching_gtd_entries.iterrows():
                gtd_value = gtd_row['dmax']

                # Check if the values are within 0.5
                if is_within_0_5(llm_value, gtd_value):
                    true_count += 1
                else:
                    false_count += 1
        else:
            # LLM material does not match any GTD entry
            unknown_count += 1

    # Calculate total entries excluding duplicates
    total_entries_without_duplicates = len(processed_materials)

    # Calculate fractions out of total entries without duplicates
    fraction_true = true_count / total_entries_without_duplicates
    fraction_false = false_count / total_entries_without_duplicates
    fraction_unknown = unknown_count / total_entries_without_duplicates

    # Print results
    print(f"Total Entries without Duplicates: {total_entries_without_duplicates}")
    print(f"Fraction True: {fraction_true}")
    print(f"Fraction False: {fraction_false}")
    print(f"Fraction Unknown: {fraction_unknown}")
