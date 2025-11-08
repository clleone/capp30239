from time_trends import time_trends
from grouped_bar import groupedbar
from parallel_coordinates import parallel_plots
from heat_map import flpr_heatmap
from scatter_plot import earn_industry_scatter

def generate_viz():
    '''
    Creates list of final visualizations.
    '''
    viz = []
    
    #time trends
    timetrends = time_trends()
    viz.append(timetrends)

    #grouped bar
    grouped_bar = groupedbar()
    viz.append(grouped_bar)

    #parallel coordinates
    sch_para = parallel_plots('SCHOOLAGE', "Most and Least Expensive States for School Age Childcare Ranked")
    inf_para = parallel_plots('INFANT', "Most and Least Expensive States for Infant Childcare Ranked")
    viz.append(sch_para)
    viz.append(inf_para)

    #heat_map
    m_flpr = flpr_heatmap(True, "Preschool Cost Burden and Maternal Labor Force Participation by County")
    g_flpr = flpr_heatmap(False, "Preschool Cost Burden and Female Labor Force Participation by County")
    viz.append(m_flpr)
    viz.append(g_flpr)

    #scatter_plot
    scatter = earn_industry_scatter("Female Median Earnings and Percentage of Women Employed in Select Industries", 'FEMP_M')
    viz.append(scatter)

    return viz