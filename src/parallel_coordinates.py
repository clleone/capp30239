import altair as alt
from dataframes import reg_rankings_df

################# GRAPH FOUR: REGULATION, QUALITY, AND COST ####################

# PARALLEL COORDINATES PLOTS SHOWING REGULATION, QUALITY, AND EXPENSE RANKINGS

def parallel_plots(cohort, title):
    '''
    Parallel coordinate plots following five most and five least expensive states
    and comparing their rankings in regulatory restrictiveness, quality, and
    expense for a given childcare age cohort.

    Trying to do labels for these was very bad for my mental health, so I opted
    to finish text editing on these manually outside altair.
    '''
    df = reg_rankings_df(cohort)

    #color assignment
    state_domain = df['STATE_NAME'].unique()
    color_range = ["#4a58dd", "#dedd32", "#2f9df5", "#f65f18", "#4df884", "#7bda3c", "#ffa423", "#27d7c4", "#ba2208", "#cb3bc6"]

    chart = alt.Chart(
        df, title=alt.Title([f'{cohort.capitalize()} Children'], anchor='middle', offset=40))

    #lines go from restrictiveness ranking to quality ranking to expensive ranking
    lines = chart.mark_line().encode(
    alt.X("Rank_Type:O", title=None, axis=None),
    alt.Y("value:O", axis=None),
    alt.Color("STATE_NAME:N", legend=None, scale=alt.Scale(
        domain=state_domain, range=color_range))).properties(width=375)
    
    #labels indicating states in lieu of legend
    label = chart.encode(
        alt.X('max(Rank_Type):O'),
        alt.Y('value:O').aggregate(argmax='Rank_Type'),
        text='STATE_NAME'
    )

    #vertical lines which ranking is being considered at that point in the graph
    vertical_lines = chart.mark_rule(color='black').encode(
        x='Rank_Type:O'
    )

    #text labels for states
    text = label.mark_text(align='left', dx=4, dy=0)

    final = lines + text + vertical_lines

    final.configure_axis(grid=False).properties(
        title=f"{title}").configure_view(stroke=None).show()

