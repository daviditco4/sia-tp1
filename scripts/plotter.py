import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker

# Directory containing the CSV files
csv_directory = '.'

if __name__ == "__main__":
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

    # Load each CSV file into a DataFrame and store them in a list
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dataframes, ignore_index=True)

    # Ensure the x-axis variable is treated as integers
    df['Board'] = df['Board'].astype(int)

    aggregated_df = df.groupby(['Algorithm', 'Board']).agg(
        {'AmountOfMovesToWin': 'mean', 'NodesExpanded': 'mean', 'FrontierNodes': 'mean'}).reset_index()

    sns.set_theme()

    plt.figure()
    # Use seaborn's lineplot with standard deviation bands
    elapsed_seconds_plot = sns.lineplot(
        data=df,
        x='Board',
        y='ElapsedSeconds',
        hue='Algorithm',  # Color by algorithm
        style='Algorithm',  # Different markers for each algorithm
        markers=True,  # Use markers for each data point
        dashes=False,  # Solid lines
        errorbar=('sd', 2)
    )
    # Ensure x-axis labels are integers
    elapsed_seconds_plot.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig("elapsed_seconds_lineplot.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure()
    amount_of_moves_to_win_plot = sns.lineplot(data=aggregated_df, x='Board', y='AmountOfMovesToWin', hue='Algorithm',
                                               style='Algorithm', marker=True, dashes=False)
    # Ensure x-axis labels are integers
    amount_of_moves_to_win_plot.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig("amount_of_moves_to_win_lineplot.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure()
    nodes_expanded_plot = sns.lineplot(data=aggregated_df, x='Board', y='NodesExpanded', hue='Algorithm',
                                       style='Algorithm',
                                       marker=True, dashes=False)
    # Ensure x-axis labels are integers
    nodes_expanded_plot.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig("nodes_expanded_lineplot.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure()
    frontier_nodes_plot = sns.lineplot(data=aggregated_df, x='Board', y='FrontierNodes', hue='Algorithm',
                                       style='Algorithm',
                                       marker=True, dashes=False)
    # Ensure x-axis labels are integers
    frontier_nodes_plot.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig("frontier_nodes_lineplot.png", dpi=300, bbox_inches='tight')
    plt.close()
