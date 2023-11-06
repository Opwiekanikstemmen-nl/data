# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
from datetime import timedelta
import re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

combined_json = pd.read_json('personen_filtered.json')
combined_json = combined_json.astype(str)
combined_json = combined_json.drop(['Nummer', 'GewijzigdOp', 'Overlijdensdatum', 'Overlijdensplaats', 'ContentType', 'ContentLength', 'GewijzigdOp', 'ApiGewijzigdOp', 'Verwijderd'], axis=1)

############### CONTACTINFO TOEVOEGEN ###################################################

contact_json = pd.read_json('source_jsons/personen_contactinformatie.json')
# Iterate over the rows in the 'contactinformatie' dataframe
for index, row in contact_json.iterrows():
        # Get the column name from the 'Soort' value
        column_name = row['Soort']

        # If the column doesn't exist in 'Personen', create it
        if column_name not in combined_json.columns:
            combined_json[column_name] = None

        # Find the corresponding row in 'Personen' by 'Id'
        personen_row = combined_json.loc[combined_json['Id'] == row['Persoon_Id']]

        # If the row exists, copy the 'Waarde' value to the new column
        if not personen_row.empty:
            combined_json.loc[personen_row.index, column_name] = row['Waarde']
    
############## GENOTEN OPLEIDINGEN TOEVOEGEN ################################################

onderwijs_json = pd.read_json('source_jsons/personen_onderwijs.json')

# Save the original 'Van' values
original_van = onderwijs_json['Van'].copy()
original_tm = onderwijs_json['TotEnMet'].copy()

# Convert 'Van' column to datetime, with 'NaT' for 'None'
onderwijs_json['Van'] = pd.to_datetime(onderwijs_json['Van'], errors='coerce')
onderwijs_json['TotEnMet'] = pd.to_datetime(onderwijs_json['TotEnMet'], errors='coerce')

# Replace 'NaT' in 'Van' with the corresponding 'TotEnMet' value
onderwijs_json.loc[onderwijs_json['Van'].isna(), 'Van'] = onderwijs_json.loc[onderwijs_json['Van'].isna(), 'TotEnMet']

# Sort 'onderwijs_json' by 'Van' (with 'NaT' considered as the lowest date)
onderwijs_json = onderwijs_json.sort_values('Van', na_position='first')

# Replace 'Van' with the original values
onderwijs_json['Van'] = original_van
onderwijs_json['TotEnMet'] = original_tm


for index, row in onderwijs_json.iterrows():
        # Create the new column value by joining the specified columns with a slash
        new_value = f"{row['OpleidingNl']}/{row['Instelling']}/{row['Van']}/{row['TotEnMet']}"

        # Find the corresponding row in 'Personen' by 'Id'
        personen_row = combined_json.loc[combined_json['Id'] == row['Persoon_Id']]

        # If the row exists, add the new value to the appropriate column
        if not personen_row.empty:
            # Determine the column name ('Opleiding', 'Opleiding2', 'Opleiding3', etc.)
            column_index = 1
            while f"Opleiding{column_index if column_index > 1 else ''}" in combined_json.columns and \
                  pd.notna(combined_json.loc[personen_row.index, f"Opleiding{column_index if column_index > 1 else ''}"]).any():
                column_index += 1
            column_name = f"Opleiding{column_index if column_index > 1 else ''}"

            # If the column doesn't exist in 'Personen', create it
            if column_name not in combined_json.columns:
                combined_json[column_name] = None

            # Add the new value to the column
            combined_json.loc[personen_row.index, column_name] = new_value
            
            
############ LOOPBAAN TOEVOEGEN ##########################################################

loopbaan_json = pd.read_json('source_jsons/personen_loopbaan.json')

# Save the original 'Van' values
original_van = loopbaan_json['Van'].copy()
original_tm = loopbaan_json['TotEnMet'].copy()

# Convert 'Van' and 'TotEnMet' columns to datetime, with 'NaT' for 'None'
loopbaan_json['Van'] = pd.to_datetime(loopbaan_json['Van'], errors='coerce')
loopbaan_json['TotEnMet'] = pd.to_datetime(loopbaan_json['TotEnMet'], errors='coerce')

    # Replace 'NaT' in 'Van' with the corresponding 'TotEnMet' value
loopbaan_json.loc[loopbaan_json['Van'].isna(), 'Van'] = loopbaan_json.loc[loopbaan_json['Van'].isna(), 'TotEnMet']

    # Sort 'loopbaan_json' by 'Van' (with 'NaT' considered as the lowest date)
loopbaan_json = loopbaan_json.sort_values('Van', na_position='first')

    # Replace 'Van' with the original values
loopbaan_json['Van'] = original_van
loopbaan_json['TotEnMet'] = original_tm

    # Iterate over the rows in the 'loopbaan_json' dataframe
for index, row in loopbaan_json.iterrows():
        # Create the new column value by joining the specified columns with a slash
        new_value = f"{row['Functie']}/{row['Werkgever']}/{row['Van']}/{row['TotEnMet']}"

        # Find the corresponding row in 'Personen' by 'Id'
        personen_row = combined_json.loc[combined_json['Id'] == row['Persoon_Id']]

        # If the row exists, add the new value to the appropriate column
        if not personen_row.empty:
            # Determine the column name ('Loopbaan', 'Loopbaan2', 'Loopbaan3', etc.)
            column_index = 1
            while f"Loopbaan{column_index if column_index > 1 else ''}" in combined_json.columns and \
                  pd.notna(combined_json.loc[personen_row.index, f"Loopbaan{column_index if column_index > 1 else ''}"]).any():
                column_index += 1
            column_name = f"Loopbaan{column_index if column_index > 1 else ''}"

            # If the column doesn't exist in 'Personen', create it
            if column_name not in combined_json.columns:
                combined_json[column_name] = None

            # Add the new value to the column
            combined_json.loc[personen_row.index, column_name] = new_value

############# FRACTIES TOEVOEGEN  ############################################################

fractiezetel_persoon_json = pd.read_json('source_jsons/fractiezetel_persoon.json')
fractiezetel_json = pd.read_json('source_jsons/fractiezetel.json')
fractie_json = pd.read_json('source_jsons/fractie.json')

# Merge 'fractiezetel_persoon_json' and 'fractiezetel_json' on 'FractieZetel_Id'
merged_df = pd.merge(fractiezetel_persoon_json, fractiezetel_json, left_on='FractieZetel_Id', right_on='Id')

    # Merge 'merged_df' and 'fractie_json' on 'Fractie_Id'
merged_df = pd.merge(merged_df, fractie_json, left_on='Fractie_Id', right_on='Id')

# Save the original 'Van' values
original_van = merged_df['Van'].copy()
original_tm = merged_df['TotEnMet'].copy()

# Convert 'Van' and 'TotEnMet' columns to datetime
merged_df['Van'] = pd.to_datetime(merged_df['Van'])
merged_df['TotEnMet'] = pd.to_datetime(merged_df['TotEnMet'])

# Sort 'merged_df' by 'Van' (with 'NaT' considered as the lowest date)
merged_df = merged_df.sort_values('Van', na_position='first')


print(merged_df)
# Create a copy of the dataframe to iterate over
df_copy = merged_df.copy()

# Iterate over the rows in the dataframe
for index, row in merged_df.iterrows():
    if row['TotEnMet']:
        # Find rows further down with identical 'Persoon_Id'
        identical_rows = df_copy[(df_copy.index > index) & (df_copy['Persoon_Id'] == row['Persoon_Id'])]
        # Iterate over the identical rows

        for identical_index, identical_row in identical_rows.iterrows():
            # Check if 'Afkorting' is identical and 'TotEnMet' is at most one week before 'Van'
            if identical_row['Afkorting'] == row['Afkorting'] and \
               identical_row['Van'] - row['TotEnMet'] <= timedelta(days=7):
                # Update 'TotEnMet' in the current row
                merged_df.loc[index, 'TotEnMet'] = identical_row['TotEnMet']

                # Delete the identical row
                merged_df = merged_df.drop(identical_index)
                df_copy = merged_df.copy()


# Iterate over the rows in the 'merged_df' dataframe
for index, row in merged_df.iterrows():
        # Create the new column value by joining the specified columns with a slash
        new_value = f"{row['NaamNL']}/{row['Van']}/{row['TotEnMet']}"

        # Find the corresponding row in 'Personen' by 'Id'
        personen_row = combined_json.loc[combined_json['Id'] == row['Persoon_Id']]

        # If the row exists, add the new value to the appropriate column
        if not personen_row.empty:
            # Determine the column name ('Fractie', 'Fractie2', 'Fractie3', etc.)
            column_index = 1
            while f"Fractie{column_index if column_index > 1 else ''}" in combined_json.columns and \
                  pd.notna(combined_json.loc[personen_row.index, f"Fractie{column_index if column_index > 1 else ''}"]).any():
                column_index += 1
            column_name = f"Fractie{column_index if column_index > 1 else ''}"

            # If the column doesn't exist in 'Personen', create it
            if column_name not in combined_json.columns:
                combined_json[column_name] = None

            # Add the new value to the column
            combined_json.loc[personen_row.index, column_name] = new_value

################# COMBINED_JSON OPSLAAN #######################################################

combined_json.to_json(r'combined_json.json', orient='index')