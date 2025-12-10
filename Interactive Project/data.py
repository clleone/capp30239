import pandas as pd
import geopandas as gpd

##########################CODE TO GENERATE DATA#################################
#########################FOR INTERACTIVE PROJECT################################

#NDCP State Level Summaries
ndcp_df = pd.read_excel(r'C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/Static Visualization/data/state_level_est.xlsx')
#Census State Level MHI Data
mhi_df = pd.read_csv(r'C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/Static Visualization/data/census_mhi_2022.csv')
#Regulatory Restrictiveness and Childcare Center Quality Rankings
ranks_df = pd.read_csv(r'C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/Static Visualization/experimentation/childcarerankings.csv')

def pivot_prices(prices_df):
    '''
    Pivots ndcp pricing data to compatible format for join.
    '''
    #filter to most recent year
    filtered_df = prices_df[prices_df['STUDYYEAR'] == 2022]
    #sorry Puerto Rico (。-ω-)ﾉ
    filtered_df = filtered_df[(prices_df['STATE_NAME'] != 'Puerto Rico')]

    #getting column names to pivot
    age_cohorts = ['infant', 'toddler', 'preschool', 'schoolage']
    AGE_COLUMNS = [f'MEDIAN_{a.upper()}_PRICE' for a in age_cohorts]
    
    #this takes center and family care, which are listed vertically across four columns
    #and instead makes center (four age groups) family (four age groups) over
    #eight columns
    pivoted_df = filtered_df.pivot_table(
    index='STATE_NAME',
    columns='TYPE',
    values=AGE_COLUMNS)
    
    #rename columns
    new_cols = [f'{col[1].upper()}_{col[0].replace('_PRICE', '_COST').replace(
        'MEDIAN_', '')}' for col in pivoted_df.columns]
    pivoted_df.columns = new_cols

    #reset the index
    pivoted_df = pivoted_df.reset_index()
    
    return pivoted_df, new_cols

def produce_pop(df):
    '''
    Adds subpopulations to get total child population by state in 2022
    '''
    df = df[df['STUDYYEAR'] == 2022]
    df = df[(df['STATE_NAME'] != 'Puerto Rico')] #Puerto Rico kept sneaking in somehow
    #only look at one type of childcare to make STATE_NAME the primary key
    df = df[df['TYPE'] == 'Center']
    #get total population of children in 2022
    df['CHILD_POP'] = df['INFANT_POPULATION'] + df['TODDLER_POPULATION'] + df[
        'PRESCHOOL_POPULATION'] + df['SCHOOL_AGE_POPULATION']

    return df[['STATE_NAME', 'CHILD_POP']]

def prep_csv(prices_df, mhi_df, ranks_df):
    '''
    Joins nongeographic data into one dataframe.
    '''
    pivoted_df, new_cols = pivot_prices(prices_df)

    #merge ndcp data and census mhi data on state
    merged = pd.merge(pivoted_df, mhi_df, "right", "STATE_NAME")
    keep_cols = ['STATE_NAME', 'MHI', 'CHILD_POP']

    #merge in child population
    child_pop = produce_pop(prices_df)
    merged = pd.merge(merged, child_pop, 'left')

    #normalize raw childcare costs by income, we only want those columns
    for col in new_cols:
        to_keep = f'ADJ_{col}'
        keep_cols.append(to_keep)
        merged[f'ADJ_{col}'] = merged[col] * 52 / merged['MHI']

    #cut down csv to what we want
    merged = merged[keep_cols]
    merged = merged[(merged['STATE_NAME'] != 'Puerto Rico') & (
        merged['STATE_NAME'] != 'United States')]

    #join ranking data
    final_df = pd.merge(merged, ranks_df, 'left', 'STATE_NAME')
    keep_cols.extend(["R_Rank", "Qual_Rank"])
    final_df = final_df[keep_cols]

    return final_df

def get_data():
    '''
    Joins regular data to hexbin geojson for final data.
    '''
    #load in US hexgrid
    hexbin = gpd.read_file(r"C:/Users/calli/capp24/Fall 25/Data Visualization/capp30239/Static Visualization/experimentation/us_states_hexgrid.geojson")
    #create column that is clean state names to match dfs later
    hexbin['STATE_NAME'] = hexbin['google_name'].str.extract(
        r'([A-Z][a-z]+\s?[a-z]*\s?[A-Z]?[a-z]+)\s[(]')

    nongeo_df = prep_csv(ndcp_df, mhi_df, ranks_df)

    final_df = pd.merge(hexbin, nongeo_df, 'left', 'STATE_NAME')

    final_df.to_file('childcare.geojson', driver='GeoJSON')



