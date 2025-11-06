import altair as alt
from dataframes import county_df

######################## GRAPH SIX: COUNTY ANALYSIS ############################

#Scatter plots with binned counties on "Cost-Maternal LFPR"

def domain_dict(df, condition): #helper
    '''
    Creates domain dictionaries for charts.
    '''
    dt = {}

    for condition in ['FEMP_M', 'PR_F', 'FME']:
        dt[condition] = (df[condition].min(), df[condition].max())

    return dt

def econ_condition_mscatter(condition, title):
    '''
    Scatter plots with binned counties on "Cost-Maternal LFPR"
    '''
    df = county_df()
    range = domain_dict(df, condition)
    chart = alt.Chart(df)

    #formatting guidance for pct vs nonpct variables
    if (condition == 'FME') or (condition == 'MHI'):
        format = '.0f'
    else:
        format='%'
    
    mscatter = chart.mark_circle(opacity=.5).encode(
        alt.X(f'{condition}').axis(format=format).scale(domain=range[condition]).title(f"{title}"),
        alt.Y('FLFPR_20to64_UNDER6').axis(format='%').scale(domain=(0, 1)).title(
            "FLPR for Mothers of Young Children"),
        alt.Color('Classification', legend=None, scale=alt.Scale(
            range=["#7bda3c", "#ff821d", "#2f9df5", "#cb3bc6"]))
    )

    mscatter.facet(
        facet=alt.Facet('Classification', title=None), columns=2).resolve_scale(
        x= 'independent', y='independent').properties(title=title).show()
