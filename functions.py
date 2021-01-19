import requests
import time
import pandas as pd
from datetime import date

tier_list = ["Challenger","Grand Master", "Master", "DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
division_list = ["I","II","III","IV"]
today = date.today()
api_key = "your-api-here"
queue = "RANKED_SOLO_5x5" # "RANKED_FLEX_SR" or "RANKED_FLEX_TT"



#This gives you the number of players in a specific division (GOLD IV) in a region
def players(region, queue, tier, division):
    result = 0
    if tier == "Challenger":
        URL = "https://" + region + ".api.riotgames.com/lol/league/v4/challengerleagues/by-queue/" + queue
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        result =  len(res.json()["entries"])
    elif tier == "Grand Master":
        URL = "https://" + region + ".api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/" + queue
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        result =  len(res.json()["entries"])
    elif tier == "Master":
        URL = "https://" + region + ".api.riotgames.com/lol/league/v4/masterleagues/by-queue/" + queue
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        result =  len(res.json()["entries"])
    else: # rest tiers
        for page_num in range(0,50000):
            URL = "https://"+region+".api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier + "/" + division + "?page=" + \
                  str(page_num)
            res = requests.get(URL, headers={"X-Riot-Token": api_key})
            while res.status_code == 429:                             # rate limit for personal keys is 100 requests every 2 minutes.
                time.sleep(5)                                           # to avoid rate limit error
                res = requests.get(URL, headers={"X-Riot-Token": api_key})
            result += len(res.json())
            if len(res.json()) == 0:                                # break the for statement after reached the last page
                break
    return(result)

def total_players(region):
    global tier_list
    global division_list
    global queue
    data = pd.DataFrame(columns= ['Tier', 'numberofplayers'])
    for tier in tier_list:
        if tier == "Challenger" or tier == "Grand Master" or tier == "Master":          # Challenger, Grand Master, and Master tier have only one page
            asd = players(region, queue, tier, 'I')
            print("Completed the calculation of " + tier + ":" + str(asd))
            data = data.append({'Tier' : tier , 'numberofplayers' : asd} , ignore_index = True)
            data.to_csv(region + "_result.csv")
        else:
            for division in division_list:
                asd = players(region, queue, tier, division)
                print("Completed the calculation of " + tier + " " + division + ":" + str(asd))
                data = data.append({'Tier' : tier + " " + division , 'numberofplayers' : asd} , ignore_index = True)
                data.to_csv(region + "_result.csv")

    data.to_csv(region + "_result.csv")


# # Calculates the average tier of a region.
# def average_tier(filename):
#     result = 0
#     agg_num = 0
#     header_list = ["Index", "Tiers", "Players"]
#     data = pd.read_csv(filename, names=header_list)
#     cus_mmr = pd.read_csv("DIA1~IRN4customized_mmr.csv", names = ['MMR'])
#     for i in range(24):
#         agg_num += data.iloc[i]['Players']
#         result = result + (data.iloc[i]['Players'] * cus_mmr.iloc[i]['MMR'])
#     avg_tier = result / agg_num
#     return avg_tier
# to be changed