import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

# Directory containing the CSV files
csv_directory = '..'

if __name__ == "__main__":
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

    # Load each CSV file into a DataFrame and store them in a list
    dataframes = [pd.read_csv(file) for file in csv_files]
    
    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dataframes, ignore_index=True)

    sns.set_theme()

    # Use seaborn's lineplot with standard deviation bands
    sns.lineplot(
        data=df,
        x='Board',
        y='ElapsedSeconds',
        hue='Algorithm',        # Color by algorithm
        style='Algorithm',     # Different markers for each algorithm
        markers=True,          # Use markers for each data point
        dashes=False,          # Solid lines
        errorbar=('sd', 2)
    )
