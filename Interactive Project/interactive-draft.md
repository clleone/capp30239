# American Childcare Affordability and Female Labor Force Participation

Callie Leone

## Goal

I, per usual, am running behind, so this is going to be a bit of a hybrid of
Milestones One and Two

I definitely want to use D3 for my project, and I'm thinking of doing a central
visual that then the viewer can cut into to see some more granular visualizations.

One of the visualizations I found most compelling while working on my static project
was a heat map looking at labor force participation rates for mothers with
children under six by county and a childcare cost indicator. I contrasted this
with an analogous heat map looking at the general female labor force participation
rate. What I found was that there was a lot more variation in the first chart,
and the nucleus of the heatmap suggested that mothers of young children might
be more likely to participate in the labor market than the general female pop
in many counties. There were also some really interesting outlier counties where
no mothers worked at all despite costs being relatively low or counties where
many mothers worked despite relative costs being quite high. 

I tried to dig into this in my static project by binning counties and putting 
them in scatter plots looking at variables like Female Median Income, the poverty
rate of that county, and the percentage of women in that county employed in
educationally intensive careers. The results were pretty lackluster in terms of
insight.  

I was thinking that I could recreate one or several of the heatmaps, and then
viewers could select a cell of the heatmap and generate a "report" or mini dashboard
that would examine trends of the counties in that cell.

So far, I have been able to generate a heat map with synthetic data that has
functioning mousovers, but not yet clicks to prompt the dash generator. I have
not yet made the miniviz.

There are a couple design/data challenges I have encountered with this idea,
please see below. 

## Data Challenges

A more technical design question I have is related to JavaScript not being a 
language well-suited for data cleaning and manipulation (at least as much as 
Python is). I need to think carefully about how I generate my data and load it
into the JavaScript knowing that once it's in there, I can't sort or filter it
as dynamically.

Would it be best to have a minicsv or json for each cell of the heat map to load
in when that cell is called to generate the dash? That's the best way I can figure
it, and that would mean having to make ~60 minicsvs or json.

## Walk Through

{Walk us through an interaction, either in words and pictures or you can record a quick 2-3 minute video.}

## Questions

There are a couple design/data challenges I have encountered with this idea.

1. In terms of concept, part of me wonders if maybe this kind of visualization is 
only interesting to me, someone who is overly familiar with the data. Is it valuable
to a general user to see graphs about collections of what they might consider
"random" counties? This is something I intend to seek feedback from my critique
group on as well.
2. Another design challenge I'm anticipating is that due to the variability, there
may be cells with as few as 5 counties, and others with as many as 100, depending
on how I split the cells. The same dashboard "template" may not make as good graphics
for each of these cases. Would it be too much work to make two different dash templates
for scant cells versus overflowing ones? 
3. I have scheduled a meeting because I have some pernicious JS/D3 questions!