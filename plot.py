import matplotlib.pyplot as plt
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

