import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv").head(10)
print(df)

# Add overweight column
df['overweight'] = ((df['weight'])/((df['height']/100)) ** 2).apply(lambda x:1 if x>25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1
df['cholesterol'].apply(lambda x:0 if x == 1 else 1)
df['gluc'].apply(lambda x:0 if x == 1 else 1)

# Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    # Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()
    
    fig = sns.catplot(x='variable', y='total', data=df_cat, hue='value', kind='bar', col='cardio').figure
    
    # 9
    fig.savefig('catplot.png')
    return fig


# Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    # Clean data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] <= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] <= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr(method="pearson")

    # Mask of the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,12))

    # heatmap with sns.heatmap()
    sns.heatmap(corr, linewidths=1, annot=True, square=True, mask=mask, fmt=".1f", center=0.08,cbar_kws={"shrink":0.5}, ax=ax)

    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()
draw_heat_map()