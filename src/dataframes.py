import pandas as pd

##These functions create dataframes used to generate visualizations.

#National Database of Childcare Prices (NDCP)
#NDCP state-level summary data
state_lvl_df = pd.read_excel(r'c:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/data/state_level_est.xlsx')
#NDCP county-level data for each state
big_22_ndcp_df = pd.read_excel(r'C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/data/ndcp2022.xlsx')
#Census state-level Median Household Income
census_mhi_df = pd.read_csv(r'C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/data/census_mhi_2022.csv')
#Regulatory ranking data from West Virginia University and
#thinktank Child Care Aware of America
regulations_df = pd.read_csv(r"C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/data/regulatory rankings.csv")

###################### GRAPH ONE : TIME TRENDS LINE GRAPH ######################

def clear_incomplete_states(df): #helper
    '''
    Filter states that only have complete data for each cohort for all years.
    '''
    prices = ['MEDIAN_SCHOOLAGE_PRICE', 'MEDIAN_PRESCHOOL_PRICE',
              'MEDIAN_TODDLER_PRICE', 'MEDIAN_INFANT_PRICE']
    #drop NAs
    df_clean = df.dropna(subset=prices)
    #count number of unique years per state
    years_per_state = df_clean.groupby('STATE_NAME')['STUDYYEAR'].nunique()
    #total possible years
    expected_years = df['STUDYYEAR'].nunique()
    #states with total possible years
    states_with_all_years = years_per_state[years_per_state == expected_years].index
    #filter to only states with total possible years
    df_clean = df_clean[df_clean['STATE_NAME'].isin(states_with_all_years)]

    return df_clean

def add_region(df):
    '''
    Maps states to regions for line graph faceted on region.
    '''
    SOUTHEAST = ['Alabama', 'Florida', 'Kentucky', 'Louisiana', 'Tennessee',
                 'West Virginia']
    MIDWEST = ['Illinois', 'Kansas', 'Michigan', 'Minnesota', 'North Dakota',
               'South Dakota', 'Wisconsin']
    WEST = ['Arizona', 'Oklahoma', 'Oregon', 'Utah', 'Washington']
    NORTHEAST = ['Connecticut', 'Delaware', 'Massachusetts', 'New Jersey']

    region_map = {}
    for state in NORTHEAST:
        region_map[state] = 'Northeast'
    for state in MIDWEST:
        region_map[state] = 'Midwest'
    for state in SOUTHEAST:
        region_map[state] = 'South'
    for state in WEST:
        region_map[state] = 'West'

    df['REGION'] = df['STATE_NAME'].map(region_map)

    return df

def time_trends_df():
    '''
    Formats NDCP data for time_trends faceted line graph. 
    '''
    #center-based childcare only
    tt_df = state_lvl_df[state_lvl_df['TYPE'] == 'Center']

    #keep only necessary columns
    tt_df = tt_df[['STATE_NAME', 'TYPE', 'STUDYYEAR', 'MEDIAN_SCHOOLAGE_PRICE',
                   'MEDIAN_PRESCHOOL_PRICE', 'MEDIAN_TODDLER_PRICE',
                   'MEDIAN_INFANT_PRICE']]
    
    #see above for helper functions
    tt_df = clear_incomplete_states(tt_df)
    tt_df = add_region(tt_df)

    return tt_df

##################### GRAPH TWO: COST BURDEN GROUPED BAR #######################

SELECTED_STATES = ['Illinois', 'Massachussets', 'Texas', 'Montana', 'California']

#state avg cost data
def state_avg_costs_df():
    '''
    Cleaning NDCP dataset.
    '''
    df = state_lvl_df
    
    #2022 center data
    #eliminate states that don't have data for all four age groups
    #eliminate states where less than 90% of kids are living in counties w data
    clean_df = df[(df['STUDYYEAR'] == 2022) & (df['MEDIAN_INFANT_PRICE'].notna()) & (
        df['TYPE'] == 'Center') & (df['PCT_VALID_INFANT'] >= .9) & (
            df['PCT_VALID_TODDLER'] >= .9) & (df['PCT_VALID_PRESCHOOL'] >= .9) & (
                df['PCT_VALID_SCHOOLAGE'] >= .9)]
    
    select_columns_df = clean_df[['STATE_NAME', 'MEDIAN_INFANT_PRICE',
                                  'MEDIAN_TODDLER_PRICE', 'MEDIAN_PRESCHOOL_PRICE',
                                  'MEDIAN_SCHOOLAGE_PRICE']]
    
    return select_columns_df

def grouped_bar_df():
    '''
    Pulling in MHI info from the Census and normalizing average costs.
    '''
    df = state_avg_costs_df()
    census_df = census_mhi_df
    
    #restructure df to long form
    df = df.melt(
        id_vars=['STATE_NAME'],
        value_vars=['MEDIAN_INFANT_PRICE',
                    'MEDIAN_TODDLER_PRICE', 'MEDIAN_PRESCHOOL_PRICE',
                    'MEDIAN_SCHOOLAGE_PRICE'],
        var_name='age',
        value_name='price'
    )

    #make variables nicer looking
    df['age'] = df['age'].str.replace('_PRICE', '').str.replace('MEDIAN_', '').str.lower()
    #add census mhi info
    merged = pd.merge(df, census_df, "left", "STATE_NAME")
    #create normalized cost column
    merged["adjusted price"] = merged['price'] * 52 / merged['MHI']

    return merged

################# GRAPH THREE: REGULATION, QUALITY, AND COST ###################

def code_rank(row):
    '''
    Numerical codings to make distinguish ranking types with greater ease.
    '''
    if row['variable'] == "Restrictiveness":
        return 0
    elif row['variable'] == "Quality":
        return 1
    else:
        return 2

def reg_rankings_df(cohort):
    '''
    Create regulation and cost burden rankings for parallel coordinate plot.
    '''
    df = grouped_bar_df()
    reg_df = regulations_df

    #filter by cohort and sort by cost burden descending
    parallel_df = df[df["age"] == f'{cohort}'].sort_values(
        'adjusted price', ascending=False)
    #create cost ranking by attaching 1-41 on sorted df
    ranking = list(range(1,42))
    parallel_df['Cost Burden'] = ranking

    #filter to five most expensive and five least expensive
    parallel_df = parallel_df[(
        parallel_df["Cost Burden"] < 6) | (parallel_df["Cost Burden"] > 36)]
    
    #merge in regulatory rankings
    parallel_df = parallel_df.merge(reg_df, "left", "STATE_NAME")

    #change to long form
    parallel_df = pd.melt(parallel_df, id_vars=['STATE_NAME'],
                          value_vars=['Restrictiveness', 'Quality', 'Cost Burden'])
    
    parallel_df['Rank_Type'] = parallel_df.apply(code_rank, axis=1)

    return parallel_df


#################### GRAPH FOUR: MATERNITY & LABOR FORCE #######################

def young_flpr_df():
    '''
    Pull female labor force participation stats for heat map.
    '''
    df = big_22_ndcp_df
    
    #only 2022
    yflpr_df = df[(df['STUDYYEAR'] == 2022)]
    #relevant columns
    select_columns = ['STATE_NAME', 'COUNTY_NAME','COUNTY_FIPS_CODE', 'MHI',
                      'MCINFANT', 'MCTODDLER','MCPRESCHOOL', 'MCSA',
                      'FLFPR_20to64', 'FLFPR_20to64_UNDER6','FLFPR_20to64_6to17']
    yflpr_df = yflpr_df[select_columns]

    #convert to 20 to .2 for labor force stats
    pct_tidy = ['FLFPR_20to64', 'FLFPR_20to64_UNDER6', 'FLFPR_20to64_6to17']
    for col in pct_tidy:
        yflpr_df[col] = yflpr_df[col] / 100

    #reformat childcare cost column names to be more legible, normalize data
    adj_val = ['MCINFANT', 'MCTODDLER', 'MCPRESCHOOL', 'MCSA']
    for col in adj_val:
        nice_name = col[2:].lower()
        yflpr_df[f'adj_{nice_name}'] = (yflpr_df[col] * 52) / yflpr_df['MHI']

    return yflpr_df

############### GRAPH FIVE: FEMALE MEDIAN EARNINGS & INDUSTRY ##################

def earn_industry_df(industry):
    '''
    Female median earnings vs percent women employed in given sector for scatter plot.
    '''
    #only 2022
    earn_df = big_22_ndcp_df[big_22_ndcp_df['STUDYYEAR'] == 2022]
    #pull relevant columns
    earn_df = earn_df[['STATE_NAME', 'COUNTY_NAME', 'COUNTY_FIPS_CODE', 'FME', f'{industry}']]
    #change 20 to .2 for employment percentages
    earn_df[f'{industry}'] = earn_df[f'{industry}'] / 100

    return earn_df

######################## GRAPH SIX: COUNTY ANALYSIS ############################

def sort_counties(row): #helper
    '''
    Buckets counties into "Cost-Participation" groups.
    '''
    if (row['adj_preschool'] >= .16) & (row['FLFPR_20to64_UNDER6'] >= .5):
        return "High-High"
    elif (row['adj_preschool'] < .16) & (row['FLFPR_20to64_UNDER6'] >= .5):
        return "Low-High"
    elif (row['adj_preschool'] >= .16) & (row['FLFPR_20to64_UNDER6'] < .5):
        return "High-Low"
    elif (row['adj_preschool'] < .16) & (row['FLFPR_20to64_UNDER6'] < .5):
        return "Low-Low"
    else:
        return "Unclassified"

def county_df():
    '''
    Factors for county analysis scatter plots.
    '''
    #bin counties into classification matrix
    df = young_flpr_df()
    df['Classification'] = df.apply(sort_counties, axis=1)
    df = df[df['Classification'] != 'Unclassified']

    #bring in other socioeconomic indicators
    filtered = df[["STATE_NAME", "COUNTY_NAME", 'COUNTY_FIPS_CODE', "MHI", "FLFPR_20to64_UNDER6", "adj_preschool", "Classification"]]
    conditions = big_22_ndcp_df[big_22_ndcp_df['STUDYYEAR']==2022]
    conditions = conditions[["COUNTY_FIPS_CODE", "FEMP_M", "PR_F", "FME"]]
    final = filtered.merge(conditions, "left", "COUNTY_FIPS_CODE")
    
    #adjust percentages to decimal form again... oops
    final['FEMP_M'] = final['FEMP_M'] / 100
    final['PR_F'] = final['PR_F'] / 100

    return final

