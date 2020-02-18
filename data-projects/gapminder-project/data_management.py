import pandas as pd

education = {'primary_school_cost': 'data/education/expenditure_per_student_primary_percent_of_gdp_per_person.csv',
             'primary_school_completion': 'data/education/primary_completion_rate_total_percent_of_relevant_age_group.csv'}

health = {'sanitation_access': 'data/health/at_least_basic_sanitation_overall_access_percent.csv',
          'water_access': 'data/health/at_least_basic_water_source_overall_access_percent.csv',
          'life_expectancy': 'data/health/life_expectancy_years.csv'}

population = {'child_mortality': 'data/population/child_mortality_0_5_year_olds_dying_per_1000_born.csv',
              'ratio_child_and_elderly': 'data/population/children_and_elderly_per_100_adults.csv',
              'children_per_mother': 'data/population/children_per_woman_total_fertility.csv',
              'median_age': 'data/population/median_age_years.csv',
              'population_density': 'data/population/population_density_per_square_kn.csv',
              'population': 'data/population/population_total.csv'}

wealth = {'av_age_billionaires': 'data/wealth/average_age_of_dollar_billionaires_years.csv',
          'gdp_yearly_growth': 'data/wealth/gdp_total_yearly_growth.csv',
          'income_per_person': 'data/wealth/income_per_person_gdppercapita_ppp_inflation_adjusted.csv',
          'inflation': 'data/wealth/inflation_annual_percent.csv',
          'people_in_poverty': 'data/wealth/number_of_people_in_poverty.csv',
          'tax_perc_gdp': 'data/wealth/tax_revenue_percent_of_gdp.csv',
          'amount_billionaires': 'data/wealth/total_number_of_dollar_billionaires.csv'}

other = {'co2_emissions': 'data/other/co2_emissions_tonnes_per_person.csv',
         'corruption_ind': 'data/other/corruption_perception_index_cpi.csv',
         'hdi': 'data/other/hdi_human_development_index.csv'}

data_locations = dict(education, **health, **population, **wealth, **other)


def get_country_data(country, attr=[], from_param=1800, to=2018):
    attr = ['Year'] + attr
    structure = [(attr, []) for attr in attr]
    for x in range(from_param, to + 1):
        structure[0][1].append(x)

    for i in range(1, len(attr)):
        path = data_locations.get(attr[i], "wrong")

        if path == "wrong":
            print("Bad attribute input: " + attr[i])
            return

        df = pd.read_csv(path, index_col='country')
        attr_values = df.loc[country, [str(x) for x in range(from_param, to + 1)]].tolist()

        for j in range(len(attr_values)):
            structure[i][1].append(attr_values[j])

    Dict = {title: columns for (title, columns) in structure}
    new_df = pd.DataFrame(Dict).set_index('Year')

    new_df.name = country

    return new_df


def get_global_data(attr=[], from_param=1800, to=2018):
    df_pop = pd.read_csv('data/population/population_total.csv', index_col='country')[[str(x) for x in range(from_param, to + 1)]]
    total_pop_per_year = df_pop.sum(axis=0, skipna=True).tolist()

    attr = ['Year'] + attr
    structure = [(attr, []) for attr in attr]

    for x in range(from_param, to + 1):
        structure[0][1].append(x)

    for i in range(1, len(attr)):
        path = data_locations.get(attr[i], "wrong")

        if path == "wrong":
            print("Bad attribute input: " + attr[i])
            return

        df = pd.read_csv(path, index_col='country')[[str(x) for x in range(from_param, to + 1)]]

        df_rel = df * df_pop / total_pop_per_year
        av_values = df_rel.sum(axis=0, skipna=True).tolist()

        for val in av_values:
            structure[i][1].append(val)

    Dict = {title: columns for (title, columns) in structure}
    new_df = pd.DataFrame(Dict).set_index('Year')

    new_df.name = 'Global'

    return new_df


def get_data(countries=[], attr=[], from_param=1800, to=2018):
    Dict = {}
    for country in countries:
        if country == 'Global':
            df = get_global_data(attr, from_param, to)
        else:
            df = get_country_data(country, attr, from_param, to)

        Dict[df.name] = df

    return Dict
