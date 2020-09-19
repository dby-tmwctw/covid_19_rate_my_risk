import pandas as pd
import time

# incident = pd.read_csv("database/Incident_Rate.csv")
# siv = pd.read_csv("database/SVI2016_US.csv")
# zip_to_fips = pd.read_csv("database/ZIP-COUNTY-FIPS.csv")
#
# minimum = incident["Incidence_Rate"].min()
# maximum = incident["Incidence_Rate"].max()

def init():
    incident = pd.read_csv("database/Incident_Rate.csv")
    siv = pd.read_csv("database/SVI2016_US.csv")
    zip_to_fips = pd.read_csv("database/ZIP-COUNTY-FIPS.csv")

    minimum = incident["Incidence_Rate"].min()
    maximum = incident["Incidence_Rate"].max()

    return incident, siv, zip_to_fips, minimum, maximum

def get_score(zip_code, incident, siv, zip_to_fips, minimum, maximum):
    fips_values = zip_to_fips[zip_to_fips["ZIP"] == 77025]["STCOUNTYFP"].values
    if (len(fips_values) == 0):
        return -1
    fips = fips_values[0]
    rpl_values = siv[siv["STCNTY"] == fips]["RPL_THEMES"].values
    if (len(rpl_values) == 0):
        return -2
    incident_values = incident[incident["FIPS"] == fips]["Incidence_Rate"].values
    incident_value = incident_values[0]
    incidence_score = ((incident_value - minimum) / (maximum - minimum)) * 15
    return rpl_values[0] * 15 + incidence_score

# incident, siv, zip_to_fips, minimum, maximum = init()
#
# print(get_score(77025, incident, siv, zip_to_fips, minimum, maximum))
