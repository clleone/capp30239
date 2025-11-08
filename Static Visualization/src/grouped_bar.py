import altair as alt
from dataframes import grouped_bar_df

##################### GRAPH TWO: COST BURDEN GROUPED BAR #######################

# GROUPED BAR GRAPHS SHOWING COST BURDEN BY AGE COHORT

def groupedbar():
    '''
    Grouped bar graph of cost burden by age cohort for a selection of states.
    '''
    #load in data
    df = grouped_bar_df()
    examples = ['Illinois', 'Massachusetts', 'Texas', 'Montana', 'California']
    df = df[df['STATE_NAME'].isin(examples)]
    
    #order for bars
    age_order = ['infant', 'toddler', 'preschool', 'schoolage']
    
    chart = alt.Chart(df)
    
    #form bars
    bars = chart.mark_bar().encode(
        alt.X('age:N', sort=age_order).title('Age Group'),
        alt.Y('adjusted price:Q').axis(format='%').title('Percentage Income Spent for One Child'),
        alt.Color('age:N').scale(scheme='turbo').sort(age_order).title('Age Group'),
    )
    
    #DHHS 7% line
    line = chart.mark_rule(color='black', strokeDash=[4,2]).encode(y=alt.datum(0.07))

    final = bars + line

    final = final.facet(facet=alt.Facet('STATE_NAME:N',title=None), columns=5).properties(
        title="2022 Childcare Costs Normalized by State Median Family Income"
        ).show()
