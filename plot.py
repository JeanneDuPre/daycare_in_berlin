import matplotlib.pyplot as plt

###Pie chart: Trägerarten in Berlin###
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


