import altair as alt
from dataframes import young_flpr_df

#################### GRAPH FIVE: MATERNITY & LABOR FORCE #######################

# HEAT MAPS COMPARING MATERNAL/GENERAL FLPR WITH PRESCHOOL CHILDCARE COST BURDEN

def heat_y_var(young_mothers,title): #helper
    '''
    Toggle for mothers with child/children under six vs general female population.
    '''
    if young_mothers:
        y_var = 'FLFPR_20to64_UNDER6'
        y_title = "LFPR for Mothers with Children Under Age Six"
        title = "Preschool Cost Burden and Maternal Labor Force Participation Rates"
        subtitle = ["Looking at county level preschool cost compared",
                    "to labor force participation rates for mothers of",
                    "young children."]
    else:
        y_var = 'FLFPR_20to64'
        y_title = "LFPR for General Female Population"
        title = "Preschool Cost Burden and Female Labor Force Participation Rates"
        subtitle = ["Looking at county level preschool cost compared to",
        "labor force participation rates for the general", 
        "female population ages 20 to 64."]

    return y_var, y_title, title, subtitle

def flpr_heatmap(young_mothers, title):
    '''
    Generate heatmaps comparing preschool cost burden to FLPR.
    '''
    df = young_flpr_df()
    y_var, y_title, title, subtitle = heat_y_var(young_mothers, title)
    
    #custom sequential colors for heat map based on colors used in other plots
    county_bins = [1, 20, 40, 60, 80, 100]
    color_range = ["#befbd1", "#A5D9D2", "#6FC0CE", "#6A8DCE",
                   "#5269CF", "#3847cd"]
    
    
    alt.Chart(df, title=alt.Title(title, subtitle=subtitle)).mark_rect(
    ).encode(alt.X('adj_preschool:Q').bin(step=.01).axis(format="%").title(
            "Preschool Age Childcare Cost Burden Normalized by MHI"),
        alt.Y(f'{y_var}:Q').bin(step=.05).scale(domain=(0.0, 1.0)).axis(
            format="%").title(y_title),
        alt.Color('count():Q').scale(domain=county_bins, range=color_range).legend(
            title='Number of US Counties')).properties(title=title).show()

