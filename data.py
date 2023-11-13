import pandas as pd

def get_data():
    # Read Excel files
    df_1 = pd.read_excel('data/schule_kita/kitaliste_aktuell.xlsx')

    # Drop the last row
    df_1 = df_1.iloc[:-1]

    # Convert columns to the appropriate data types
    df_1['PLZ'] = df_1['PLZ'].astype(int)
    df_1['Einrichtungsnummer'] = df_1['Einrichtungsnummer'].astype(int)

    # Combine columns to create 'FullAddress'
    df_1['FullAddress'] = df_1['Einrichtungsadresse'] + ' ' + df_1['PLZ'].astype(str) + ' Berlin'

    # Replace values in 'Trägerart' column
    df_1['Trägerart'] = df_1['Trägerart'].replace(['EKT'], 'Elterninitiativ-Kinderladen')

    # Read CSV file
    df_2 = pd.read_csv('data/kita_aktuell.csv')

    # Merge dataframes on 'FullAddress'
    df_3 = pd.merge(df_1, df_2, on="FullAddress")

    # Drop rows with NaN values
    df_3.dropna(inplace=True)

    # Rename column
    df_3.rename(columns={'Anzahl Plätze': 'Plätze'}, inplace=True)

    return df_3
