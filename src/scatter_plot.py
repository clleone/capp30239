import altair as alt
from dataframes import earn_industry_df

################ GRAPH FIVE: FEMALE MEDIAN EARNINGS & INDUSTRY #################

# SCATTER PLOT JUXTAPOSING COUNTY LEVEL FME & PREVALENCE OF
# EDUCATION INTENSIVE EMPLOYMENT

def earn_industry_scatter(title, industry):
    '''
    Generate scatter plot+regression comparing FME and percentage of women employed
    in education-intensive industries in that county.
    '''
    df = earn_industry_df()
    
    chart = alt.Chart(df, title=alt.Title(
        title,subtitle=["Select industries include management, business,",
                        "science, and arts."]))
    
    dots = chart.mark_circle(color="#ff821d", opacity=.4,).encode(
        alt.X(f'{industry}').axis(format='%').title("Percentage of Women Employed in Select Industries"),
        alt.Y('FME').title("Female Median Earnings in Dollars"),
        )
    
    regression = dots.transform_regression(f'{industry}', 'FME').mark_line(color="#cb2f0d")

    final = dots + regression

    #input "Female Median Earnings and Percentage of Women Employed in Select Industries"
    #variable 'FEMP_M'
    final.show()
