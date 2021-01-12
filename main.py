# written by Sunhyeok Jung ( between0n1 )
#

import requests
import time
import pandas as pd
from datetime import date


#This gives you the number of players in a specific division (GOLD IV) in a region
def players(region, queue, tier, division):
    accumulated_players_by_division = 0
    for page_num in range(0,50000):
        URL = "https://"+region+".api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier + "/" + division + "?page=" + \
              str(page_num)
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        while res.status_code == 429:  # rate limit for personal keys is 100 requests every 2 minutes.
            print("wating........")
            time.sleep(10)
            URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier + "/" + division + "?page=" + \
                  str(page_num)
            res = requests.get(URL, headers={"X-Riot-Token": api_key})
        if len(res.json()) == 0:
            break
        accumulated_players_by_division += len(res.json())
    return(accumulated_players_by_division)

def total_players(region):
    queue = "RANKED_SOLO_5x5"
    tier_list = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
    division_list = ["I", "II", "III", "IV"]
    for tier in tier_list:
        for division in division_list:
            asd = players(region, queue, tier, division)
            print("Completed the calculation of " + tier + " " + division + ":" + str(asd))
            df = pd.DataFrame([[tier + " " + division, asd]])
            df.to_csv(region + "result" + str(today.strftime("%m%d%y")) + ".csv", mode='a', header=False)


# Calculates the average tier of a region.
def average_tier(filename):
    result = 0
    agg_num = 0
    header_list = ["Index", "Tiers", "Players"]
    data = pd.read_csv(filename, names=header_list)
    cus_mmr = pd.read_csv("DIA1~IRN4customized_mmr.csv", names = ['MMR'])
    for i in range(24):
        agg_num += data.iloc[i]['Players']
        result = result + (data.iloc[i]['Players'] * cus_mmr.iloc[i]['MMR'])
    avg_tier = result / agg_num
    return avg_tier

queue = "RANKED_SOLO_5x5"
tier_list = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
division_list = ["I","II","III","IV"]
region = "kr" # <--------- edit this to attain data from another region ex: kr
today = date.today()
api_key = None




