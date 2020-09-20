import pandas as pd
import time
import pickle

def init():
    incident = pd.read_csv("database/Incident_Rate.csv")
    siv = pd.read_csv("database/SVI2016_US.csv")
    zip_to_fips = pd.read_csv("database/ZIP-COUNTY-FIPS.csv")

    minimum = incident["Incidence_Rate"].min()
    maximum = incident["Incidence_Rate"].max()

    return incident, siv, zip_to_fips, minimum, maximum

def get_location_score(zip_code, incident, siv, zip_to_fips, minimum, maximum):
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

def precondition_risk(x):
    preconditionLogisticRegr = pickle.load(open("model/preconditionLogReg.pkl", "rb"))
    return preconditionLogisticRegr.predict_proba([x])[0][1]

def symptoms_risk(x):
    symptomsLogisticRegr = pickle.load(open("model/symptomsLogReg.pkl", "rb"))
    return symptomsLogisticRegr.predict_proba([x])[0][1]

def static_score(entry, incident, siv, zip_to_fips, minimum, maximum):
    loc_score = get_location_score(entry['location']['zipcode'], incident, siv, zip_to_fips, minimum, maximum)
    symptoms_input = [entry['symptoms']['difficultBreath'], 
                    entry['symptoms']['fever'],
                    entry['symptoms']['dryCough'],
                    entry['symptoms']['soreThroat'],
                    entry['symptoms']['runnyNose'],
                    entry['priorDisease']['asthma'],
                    entry['priorDisease']['chronicLungDisease'],
                    entry['symptoms']['headache'],
                    entry['priorDisease']['heartDisease'],
                    entry['priorDisease']['diabetes'],
                    entry['priorDisease']['hypertension'],
                    entry['symptoms']['fatigue'],
                    entry['priorDisease']['gastrointestinal'],
                    entry['contact']['abroadTravel'],
                    entry['contact']['contactCovid19'],
                    entry['contact']['largeGathering'],
                    entry['contact']['visitPublicExposedPlaces'],
                    entry['contact']['familyExposed'],
                    not entry['contact']['notWearMask'],
                    entry['contact']['sanitizationFromMarket']]

    symptoms_score = symptoms_risk([int(item) for item in symptoms_input])

    precondition_input = [entry['basicInfo']['gender'], 
                    entry['priorDisease']['pneumonia'],
                    entry['basicInfo']['age'],
                    entry['basicInfo']['preganancy'],
                    entry['priorDisease']['diabetes'],
                    entry['priorDisease']['copd'],
                    entry['priorDisease']['asthma'],
                    entry['priorDisease']['immunosuppression'],
                    entry['priorDisease']['hypertension'],
                    entry['priorDisease']['otherDiseases'],
                    entry['priorDisease']['cardiovascular'],
                    entry['priorDisease']['obesity'],
                    entry['priorDisease']['chronicKidneyDisease'],
                    entry['basicInfo']['smoking'],
                    entry['contact']['contactCovid19']]

    precondition_score = precondition_risk([int(item) for item in precondition_input])

    return 20 * precondition_score + 50 * symptoms_score + loc_score 


# incident, siv, zip_to_fips, minimum, maximum = init()
#
# print(get_score(77025, incident, siv, zip_to_fips, minimum, maximum))

# import json
# with open('./example.json', 'r') as f:
#     entry = json.load(f)

# incident, siv, zip_to_fips, minimum, maximum = init()
# print(static_score(entry, incident, siv, zip_to_fips, minimum, maximum))