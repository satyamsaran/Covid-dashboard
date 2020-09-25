# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Projections of ICU need by Country
# > Modeling current and future ICU demand.
#
# - categories: [overview, map, interactive]
# - author: <a href=https://github.com/artdgn/>artdgn</a>
# - image: images/covid-progress-projections.png
# - permalink: /covid-progress-projections/
# - toc: true
# - hide: false

# > Warning: This dashboard contains the results of a predictive model that was not built by an epidemiologist.

# > Note: Click a country name to open a search results page for that country's COVID-19 news.

# +
#hide
import pandas as pd
import overview_helpers


covid_data = overview_helpers.CovidData()
stylers = overview_helpers.PandasStyling
df_all, debug_dfs = covid_data.table_with_projections(debug_dfs=True)
df = covid_data.filter_df(df_all)
df.columns
# -

#hide_input
from IPython.display import Markdown
Markdown(f"***Based on data up to: {covid_data.cur_date}***")

#hide
geo_helper = overview_helpers.GeoMap
df_geo = geo_helper.make_geo_df(df_all, cases_filter=1000, deaths_filter=20)
fig = geo_helper.make_map_figure(df_geo)

#hide
df_geo['affected_ratio.change.monthly.rate'] = (df_geo['affected_ratio.est.+7d'] -
                                                df_geo['affected_ratio.est']) * 30 / 7

#hide_input
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['transmission_rate'], 'Transmission rate<br>percent (blue-red)',
                    colorscale='Bluered', scale_max=10, percent=True,
                    subtitle='Transmission rate: over 5% (red) spreading, under 5% (blue) recovering',
                    err_series=df_geo['transmission_rate_std']),
                geo_helper.button_dict(
                    df_geo['transmission_rate'], 'Transmission rate<br>percent',
                    colorscale='YlOrRd', scale_max=33, percent=True,
                    subtitle='Transmission rate (related to R0)',
                    err_series=df_geo['transmission_rate_std']),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k.est'], 'Recent cases<br>estimated per 100k',
                    colorscale='YlOrRd',
                    subtitle='Estimated recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new.est'], 'Recent cases<br>(estimated)',
                    colorscale='YlOrRd',
                    subtitle='Estimated recent cases in last 5 days'),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k'], 'Recent cases<br>reported per 100k',
                    colorscale='YlOrRd',
                    subtitle='Reported recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new'], 'Recent cases<br>(reported)',
                    colorscale='YlOrRd',
                    subtitle='Reported recent cases in last 5 days'),
            ],
            direction="down", bgcolor='#efe9da',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.07, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['affected_ratio.est'], 'Affected percent<br>(Current)',
                    colorscale='Bluyl', percent=True,
                    subtitle='Estimated current affected population percentage'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+14d'], 'Affected percent<br>(in 14 days)',
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 14 days',
                    err_series=df_geo['affected_ratio.est.+14d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+30d'], 'Affected percent<br>(in 30 days)',
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 30 days',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.change.monthly.rate'],
                    title='Affected percent<br>montly change rate',
                    colorscale='Bluyl', scale_max=10, percent=True,
                    subtitle='Current affected population percentage monthly change rate',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k.est'], 'Total cases<br>estimated per 100k',
                    colorscale='YlOrRd',
                    subtitle='Estimated total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total.est'], 'Total cases<br>(estimated)', colorscale='YlOrRd',
                    subtitle='Estimated total cases'),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k'], 'Total cases<br>reported per 100k',
                    colorscale='YlOrRd',
                    subtitle='Reported total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total'], 'Total cases<br>(reported)', colorscale='YlOrRd',
                    subtitle='Reported total cases'),
            ],
            direction="down", bgcolor='#dceae1',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.29, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['needICU.per100k'], 'ICU need<br>(current)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Estimated current ICU need per 100k population'),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+14d'],  'ICU need<br>(in 14 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 14 days',
                    err_series=df_geo['needICU.per100k.+14d.err']),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+30d'],  'ICU need<br>(in 30 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 30 days',
                    err_series=df_geo['needICU.per100k.+30d.err']),
                geo_helper.button_dict(
                    df_geo['icu_capacity_per100k'], 'Pre-COVID<br>ICU Capacity',
                    colorscale='Blues',
                    subtitle='Pre-COVID ICU capacity per 100k population'),
            ],
            direction="down", bgcolor='#efdaee',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.515, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['Deaths.total.per100k'], 'Deaths<br>per 100k', colorscale='Reds',
                    subtitle='Total deaths per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.total'], 'Deaths<br>Total', colorscale='Reds',
                    subtitle='Total deaths'),
                geo_helper.button_dict(
                    df_geo['Deaths.new.per100k'], 'Recent deaths<br>per 100k', colorscale='Reds',
                    subtitle='Recent deaths in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.new'], 'Recent deaths<br>total', colorscale='Reds',
                    subtitle='Recent deaths in last 5 days'),
                geo_helper.button_dict(
                    df_geo['lagged_fatality_rate'], 'Fatality rate %<br>(lagged)',
                    colorscale='Reds', scale_max=20, percent=True,
                    subtitle='Reported fatality rate (relative to reported cases 8 days ago)'),
            ],
            direction="down", bgcolor='#efdbda',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.69, xanchor="left", y=1.1, yanchor="top"),
    ]);

# # World map (interactive)
# > Includes only countries with at least 1000 reported cases or at least 20 reported deaths.
#
# - Details of estimation and prediction calculations are in [Appendix](#appendix) and in [Tables](#tables), as well as [Plots of model predictions](#examples).
# - New cases and new deaths refer to cases or deaths in the last 5 days.

# > Tip: Select columns to show on map to from the dropdown menus. The map is zoomable and draggable.

#hide_input
fig.show()

# # Tables
# <a id='tables'></a>
# ## Projected need for ICU beds
# > Countries sorted by current estimated need, split into Growing and Recovering
# countries by current transmission rate. Only for countries with ICU need higher
# than 0.1 beds per 100k. More details in [Appendix](#appendix).

# +
#hide

def style_icu_table(df):
    df_icu = df.sort_values('needICU.per100k', ascending=False)

    cols = {'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
            'transmission_rate': 'Estimated<br>daily<br>transmission<br>rate',
            'needICU.per100k.+14d': 'Projected<br>ICU need<br>per 100k<br>In 14 days',
            'needICU.per100k.+30d': 'Projected<br>ICU need<br>per 100k<br>In 30 days',
            'icu_capacity_per100k': 'Pre-COVID<br>ICU<br>capacity<br> per 100k',
            }
    df_show = stylers.country_index_emoji_link(df_icu, font_size=1)
    df_show['needICU.per100k.+14d'] = stylers.with_errs_float(
        df_show, 'needICU.per100k.+14d', 'needICU.per100k.+14d.err')
    df_show['needICU.per100k.+30d'] = stylers.with_errs_float(
        df_show, 'needICU.per100k.+30d', 'needICU.per100k.+30d.err')
    df_show['transmission_rate'] = stylers.with_errs_ratio(
        df_show, 'transmission_rate', 'transmission_rate_std')
    df_show = df_show[cols.keys()].rename(columns=cols)
    return (df_show.style
        .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)
        .apply(stylers.add_bar, color='#f43d64',
               s_v=df_icu['needICU.per100k.+14d']/10, subset=cols['needICU.per100k.+14d'])
        .apply(stylers.add_bar, color='#ef8ba0',
               s_v=df_icu['needICU.per100k.+30d']/10, subset=cols['needICU.per100k.+30d'])
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df_icu['transmission_rate']/0.33, subset=cols['transmission_rate'])
        .bar(subset=[cols['icu_capacity_per100k']], color='#3ab1d8', vmin=0, vmax=40)
        .applymap(lambda _: 'color: blue', subset=cols['icu_capacity_per100k'])
        .format('<b>{:.1f}</b>', subset=cols['icu_capacity_per100k'], na_rep="-")
        .format('<b>{:.2f}</b>', subset=cols['needICU.per100k']))

# -

# ### Growing countries (transmission rate above 5%)

#hide_input
style_icu_table(df[(df['transmission_rate'] > 0.05) & (df['needICU.per100k'] > 0.1)])

# ### Recovering countries (tranmission rate below 5%)

#hide_input
style_icu_table(df[(df['transmission_rate'] < 0.05) & (df['needICU.per100k'] > 0.1)])

# # Appendix
# <a id='appendix'></a>

# <a id='examples'></a>
#
# ## Interactive plot of model predictions and past data
#
# > Tip: Choose a country from the drop-down menu to see the calculations used in the tables above and the dynamics of the model.

#hide_input
df_alt = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
df_alt_filt = df_alt[(df_alt['day'] > -60) & (df_alt['country'].isin(df.index))]
overview_helpers.altair_sir_plot(df_alt_filt, df['Deaths.new.per100k'].idxmax())

# ## Projected Affected Population percentages
# > Top 20 countries with most estimated recent cases. Sorted by number of estimated recent cases during the last 5 days. More details in [Appendix](#appendix).

# +
#hide_input
df_cases = df.sort_values('Cases.new.est', ascending=False).head(20)

cols = {'Cases.new.est': 'Estimated <br> <i>recent</i> cases<br>during<br>last 5 days',
       'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
       'transmission_rate': 'Estimated<br>daily<br>transmission<br>rate',
       'affected_ratio.est.+14d': 'Projected<br><i>total</i><br>affected<br>percentage<br>In 14 days',
       'affected_ratio.est.+30d': 'Projected<br><i>total</i><br>affected<br>percentage<br>In 30 days',
       'lagged_fatality_rate': 'Lagged<br>fatality <br> rate',
      }
df_show = stylers.country_index_emoji_link(df_cases, font_size=1)
df_show['affected_ratio.est.+14d'] = stylers.with_errs_ratio(
    df_show, 'affected_ratio.est.+14d', 'affected_ratio.est.+14d.err')
df_show['affected_ratio.est.+30d'] = stylers.with_errs_ratio(
    df_show, 'affected_ratio.est.+30d', 'affected_ratio.est.+30d.err')
df_show['transmission_rate'] = stylers.with_errs_ratio(
    df_show, 'transmission_rate', 'transmission_rate_std')
df_show = df_show[cols.keys()].rename(columns=cols)
(df_show.style
    .apply(stylers.add_bar, color='#719974',
           s_v=df_cases['affected_ratio.est.+14d'], subset=cols['affected_ratio.est.+14d'])
    .apply(stylers.add_bar, color='#a1afa3',
           s_v=df_cases['affected_ratio.est.+30d'], subset=cols['affected_ratio.est.+30d'])
    .apply(stylers.add_bar, color='#f49d5a',
           s_v=df_cases['transmission_rate']/0.33, subset=cols['transmission_rate'])
    .bar(subset=cols['Cases.new.est'], color='#b57b17')
    .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
    .bar(subset=cols['lagged_fatality_rate'], color='#420412', vmin=0, vmax=0.2)
    .applymap(lambda _: 'color: red', subset=cols['lagged_fatality_rate'])
    .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])
    .format('<b>{:.1%}</b>', subset=[cols['lagged_fatality_rate'], cols['affected_ratio.est']]))
# -

# <a id='methodology'></a>
# ## Methodology
# - I'm not an epidemiologist. This is an attempt to understand what's happening, and what the future looks like if current trends remain unchanged.
# - Everything is approximated and depends heavily on underlying assumptions.
# - Projection is done using a simple [SIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model) (see [examples](#examples)) combined with the approach in [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases):
#     - Growth rate is calculated over the 5 past days by averaging the daily growth rates.
#     - Confidence bounds are calculated by from the weighted standard deviation of the growth rate over the last 5 days. Model predictions are calculated for growth rates within 1 STD of the weighted mean. The maximum and minimum values for each day are used as confidence bands.
#     - Transmission rate, and its STD are calculated from growth rate and its STD using active cases estimation mentioned above.
#     - For projections (into future) very noisy projections (with broad confidence bounds) are not shown in the tables.
#     - Where the rate estimated from [Total Outstanding Cases](https://covid19dashboards.com/outstanding_cases/#Appendix:-Methodology-of-Predicting-Recovered-Cases) is too high (on down-slopes) recovery probability if 1/20 is used (equivalent 20 days to recover).
# - Total cases are estimated from the reported deaths for each country:
#     - Each country has a different testing policy and capacity and cases are under-reported in some countries. Using an estimated IFR (fatality rate) we can estimate the number of cases some time ago by using the total deaths until today.
#     - IFRs for each country is estimated using the age adjusted IFRs from [May 1 New York paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3590771) and [UN demographic data for 2020](https://population.un.org/wpp/Download/Standard/Population/). These IFRs can be found in `df['age_adjusted_ifr']` column. Some examples: US - 0.98%, UK - 1.1%, Qatar - 0.25%, Italy - 1.4%, Japan - 1.6%.
#     - The average fatality lag is assumed to be 8 days on average for a case to go from being confirmed positive (after incubation + testing lag) to death. This is the same figure used by ["Estimating The Infected Population From Deaths"](https://covid19dashboards.com/covid-infected/).
#     - Testing bias adjustment: the actual lagged fatality rate is than divided by the IFR to estimate the testing bias in a country. The estimated testing bias then multiplies the reported case numbers to estimate the *true* case numbers (*=case numbers if testing coverage was as comprehensive as in the heavily tested countries*).
# - ICU need is calculated and age-adjusted as follows:
#     - UK ICU ratio was reported as [4.4% of active reported cases](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf).
#     - Using UKs ICU ratio, UK's testing bias, and IFRs corrected for age demographics we can estimate each country's ICU ratio (the number of cases requiring ICU hospitalisation).
#     - Active cases for ICU estimation are taken from the SIR model.
#     - Pre COVID-19 ICU capacities are from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_hospital_beds) (OECD countries mostly) and [CCB capacities in Asia](https://www.researchgate.net/publication/338520008_Critical_Care_Bed_Capacity_in_Asian_Countries_and_Regions).
#     The current capacities are likely much higher as some countries already doubled or even quadrupled their ICU capacities.
# ![](https://artdgn.goatcounter.com/count?p=c19d-projections)
