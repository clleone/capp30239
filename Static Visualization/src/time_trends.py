import altair as alt
from dataframes import time_trends_df

###################### GRAPH ONE : TIME TRENDS LINE GRAPH ######################

NONOVERLAP = ['Arizona', 'Connecticut', 'Delaware', 'Kansas', 'Massachusetts',
 'Michigan', 'Minnesota', 'New Jersey', 'North Dakota', 'Oklahoma', 'Oregon',
 'South Dakota', 'Tennessee', 'Utah', 'Washington', 'West Virginia', 'Wisconsin']

##GRAPH ONE: CHILDCARE COST TRENDS OVER TIME (FACETED LINE GRAPH)

def time_color_scheme(df): #helper
    '''
    Creates color schemes parameters for states based on region for time_trends graph.
    '''
    seven_scheme = ["#4569ee", "#ff821d", "#3ff393",
                    "#cb2f0d", "#26bce1", "#ecd12e", "#7bda3c"]
    regions = list(df['REGION'].unique())
    region_lsts = []

    for region in regions:
        st_in_region = list(df[df['REGION'] == region]['STATE_NAME'].unique())
        region_lsts.append(st_in_region)

    color_range = []
    state_domain = []
    for region in region_lsts:
        for i, state in enumerate(region):
            color_range.append(seven_scheme[i])
            state_domain.append(state)

    return state_domain, color_range

def time_labels(chart): #helper
    '''
    Manual handling of overlapping labels in time_trends graph.
    '''
    #nonoverlapping regular labels
    norm_text = chart.mark_text(align='left', dx=10).transform_filter(
        alt.FieldOneOfPredicate(field='STATE_NAME', oneOf=NONOVERLAP)
    )
    #unoverlaps are labels that had to be manually adjusted
    unoverlap_1 = chart.mark_text(align='left', dx=10, dy=12).transform_filter(
        alt.FieldOneOfPredicate(field='STATE_NAME', oneOf=['Florida', 'Alabama'])
    )
    unoverlap_2 = chart.mark_text(align='left', dx=10, dy=3).transform_filter(
        alt.FieldOneOfPredicate(field='STATE_NAME', oneOf=['Kentucky', 'Illinois'])
    )
    unoverlap_3 = chart.mark_text(align='left', dx=10, dy=-6).transform_filter(
        alt.FieldOneOfPredicate(field='STATE_NAME', oneOf=['Louisiana'])
    )

    #combine into one set of labels
    text = norm_text + unoverlap_1 + unoverlap_2 + unoverlap_3

    return text

def time_trends():
    '''
    Produces line graph representing trends in childcare costs over time by
    state, faceted on region.
    '''
    tt_df = time_trends_df()

    chart = alt.Chart(tt_df)

    # manual color scheme
    state_domain, color_range = time_color_scheme(tt_df)

    # create line graph
    line = chart.mark_line().encode(
            alt.X('STUDYYEAR:O').title("Year"),
            alt.Y('MEDIAN_SCHOOLAGE_PRICE:Q').scale(
                domain=(0, 240)).title(
                    "Weekly Cost of Childcare for One School-aged Child"
                    ),
            alt.Color('STATE_NAME:N', legend=None,
                      scale=alt.Scale(domain=state_domain, range=color_range))
            )

    # this identifies where labels will go by finding the last spot on the lines
    label = chart.encode(
        alt.X('max(STUDYYEAR):O'),
        alt.Y('MEDIAN_SCHOOLAGE_PRICE:Q').aggregate(argmax='STUDYYEAR'),
        text='STATE_NAME'
    )

    # create text labels and handle overlapping
    text = time_labels(label)

    final = line + text

    #facet, put labeled axes on each plot, title 
    final = final.facet(facet='REGION:N', columns=2).properties(
            title="Weekly School Age Childcare Costs by State and Region, 2008-2022"
            ).resolve_scale(x= 'independent', y='independent')
    
    return final
