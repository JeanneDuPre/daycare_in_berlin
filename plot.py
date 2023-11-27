import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

###pie chart: Trägerarten in Berlin###
def plot_provider_distribution(df, excluded_value):
    # Calculate the value counts
    value_counts = df['Trägerart'].value_counts()

    # Define colors for the pie chart
    colors = ['#f59e20', '#27a598', '#c4544c', '#667496', '#4a6455', '#444a44', '#121514', '#d8ad7d']
    
    # Specify explode values for highlighting a specific segment
    explode = (0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0) 

    # Exclude the specified value from the pie chart
    value_counts = value_counts.drop(excluded_value, errors='ignore')
    
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(value_counts, labels=None, colors=colors, explode=explode, autopct=lambda p: f'{p:.2f}%\n' if p > 4 else None,
                                       startangle=140, textprops={'fontsize': '9'}, wedgeprops={'linewidth': 0.5, 'edgecolor': 'k'})
    
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.title('Distribution of Providers in Berlin')

    # Create a legend excluding the specified value
    legend_labels = value_counts.index
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(0.77, 0.85), fontsize='small')
    plt.show()

###bar chart: Verteilung der Trägerart bei Bezirk####
def plot_stacked_percentage_tragerart_kitas(df):
    # Create a copy of the dataframe with relevant columns
    df2 = df[['Trägerart', 'Betreuungsbezirk']].copy()

    # Calculate the percentages for each category within 'Trägerart'
    percentage_df = df2.groupby(['Betreuungsbezirk', 'Trägerart']).size().unstack().apply(lambda x: x / x.sum(), axis=1)

    # Define custom colors for each 'Trägerart'
    custom_colors = ['#444a44', '#121514', '#4a6455', '#667496', '#c4544c', '#27a598', '#f59e20', '#d8ad7d']

    # Create a stacked bar plot with custom colors
    fig, ax = plt.subplots(figsize=(10, 6))
    percentage_df.plot(kind='bar', stacked=True, ax=ax, color=custom_colors)
    
    plt.title('Distribution of Provider Types by District')
    plt.xlabel('District')
    plt.ylabel('Percentage')
    plt.xticks(rotation=90)

    # Create the legend next to the plot
    legend = ax.legend(loc='center left', bbox_to_anchor=(0.45, 0.77))
    legend.get_frame().set_alpha(0.5)  # Set the opacity of the legend

    # Add only horizontal grid lines to the plot
    ax.yaxis.grid(True)

    # Remove the upper and left spines
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Change y-axis labels to percentage format
    def percentage_formatter(x, pos):
        return f'{x:.0%}'

    ax.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))

    plt.show()

###bar chart: Verteilung der Kitaplätze bei Bezirk und Trägerart###
def plot_stacked_percentage_tragerart_platze(df):
    # Group the dataframe by 'Betreuungsbezirk' and 'Trägerart', then sum the 'Plätze'
    grouped_df = df.groupby(['Betreuungsbezirk', 'Trägerart'])['Plätze'].sum().reset_index()

    # Pivot the data to prepare it for a stacked bar chart
    pivot_df = grouped_df.pivot(index='Betreuungsbezirk', columns='Trägerart', values='Plätze')

    # Define custom colors for each 'Trägerart'
    custom_colors = ['#444a44', '#121514', '#4a6455', '#667496', '#c4544c', '#27a598', '#f59e20', '#d8ad7d']

    # Create a subplot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter the pivot_df to show values with more than 0
    pivot_df_filtered = pivot_df[pivot_df > 0].fillna(0)

    # Plot the stacked bar chart
    pivot_df_filtered.plot(kind='bar', stacked=True, ax=ax, color=custom_colors)

    # Set plot labels and title
    plt.title('Distribution of Daycare Slots by District and Provider Type')
    plt.xlabel('District')
    plt.ylabel('Daycare Slots')
    plt.xticks(rotation=90)

    # Filter legend labels based on pivot_df_filtered
    legend_labels = [label for label in pivot_df_filtered.columns if any(pivot_df_filtered[label] > 0)]

    # Create the legend next to the plot
    legend = ax.legend(labels=legend_labels, loc='center left', bbox_to_anchor=(0.4, 0.77))
    legend.get_frame().set_alpha(0.5)  # Set the opacity of the legend

    # Add only horizontal grid lines to the plot
    ax.yaxis.grid(True)

    # Remove the upper and left spines
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.show()

##combo chart (pie chart- zu betreuende Kinder, bar chart- Kitaplätze): Kitaplätze und zu betreuende Kinder in Berlin 
def plot_stacked_percentage_trägerart_plätze():
    # Load the datasets
    df = pd.read_csv('data/kitaliste_gesamt_Stand_2023-11-16.csv')
    mask = pd.read_csv('data/bevölkerung_ortsteile_gesamt_Stand_2023-11-16.csv')
    df_3 = pd.read_excel('data/2023_data.xlsx')

    # Transform the dataset
    grouped_df = df.groupby(['Betreuungsbezirk'])['Plätze'].sum().reset_index()

    # Create the figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot the bar chart
    ax1.bar(grouped_df['Betreuungsbezirk'], grouped_df['Plätze'], alpha=0.7)
    
    # Titles and labels
    plt.suptitle('Kitaplätze und zu betreuende Kinder in Berlin', fontsize=16)
    plt.title('''In Berlin wurden bisher lediglich in den Bezirken Mitte und Pankow ausreichend Kinderbetreuungsplätze bereitgestellt.
Hingegen zeigen zehn weitere Bezirke eine deutliche Unterversorgung in der Betreuung.
Die verfügbaren Daten beziehen sich ausschließlich auf die Altersspanne von 0 bis 5 Jahren.
Da in Berlin ein Anspruch auf einen Betreuungsplatz bereits ab dem ersten Lebensjahr besteht und Kinder
ab dem Alter von 6 Jahren nicht eigens erfasst werden, kann die Verschiebung an dieser Stelle unberücksichtigt bleiben.''', fontsize=10, color='grey')
    plt.ylabel('Kitaplätze', fontsize=12)
    plt.xticks(rotation=90)
    ax1.yaxis.grid(True)

    # Adjust spines
    for spine in ['top', 'left', 'right', 'bottom']:
        ax1.spines[spine].set_visible(False)

    # Create second y-axis for line chart
    ax2 = ax1.twinx()
    ax2.set_ylabel('Zahl der zu betreuenden Kinder', fontsize=12)
    ax2.plot(df_3['Betreuungsbezirk'], df_3['unter_6'], color='red', label='unter 6 (2023)', linewidth=3.0, alpha=0.9)
    ax2.plot(mask['Bez-Name'], mask['Kitaplätze'], color='blue', label='0 bis 5 (2020)', alpha=0.6)
    ax2.legend(loc=(0.8, 0.9))
    ax2.spines['top'].set_visible(False)

    # Set y-axis limits
    combined_data = np.concatenate([grouped_df['Plätze'], df_3['unter_6']], axis=None)
    valid_values = combined_data[~np.isnan(combined_data) & np.isfinite(combined_data)]
    max_value = max(valid_values)
    ax1.set_ylim(0, max_value + 1000)
    ax2.set_ylim(0, max_value + 1000)
    ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Adjust margins around the plot area
    plt.subplots_adjust(left=None, bottom=0.05, right=None, top=0.78, wspace=None, hspace=None)
    
    # Adding a footnote
    plt.figtext(0.8, -0.28, 'Graphik: JeanneDuPre | Daten: Berliner Senat | November 2023', ha='center', fontsize=10, color='grey')

    plt.show()
