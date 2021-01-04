# written by Sunhyeok Jung ( between0n1 )
#

import requests
import time
import csv
import pandas as pd
from datetime import date


def get_numberofplayers_by_division(region,queue, tier, division):
    accumulated_players_by_division = 0
    page_num = 1
    isend = False
    while isend == False:
        URL = "https://"+region+".api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier + "/" + division + "?page=" + \
              str(page_num)
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        accumulated_players_by_division += len(res.json())
        page_num += 1
        if len(res.json()) == 0:
            isend = True
        if res.status_code == 429:
            time.sleep(10)
            page_num -= 1
    return(accumulated_players_by_division)

def total_number(region):
    queue = "RANKED_SOLO_5x5"
    tier_list = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
    division_list = ["I", "II", "III", "IV"]
    for tier in tier_list:
        for division in division_list:
            asd = get_numberofplayers_by_division(region, queue, tier, division)
            print("Completed the calculation of " + tier + " " + division + ":" + str(asd))
            df = pd.DataFrame([[tier + " " + division, asd]])
            df.to_csv(region + "result" + str(today.strftime("%m%d%y")) + ".csv", mode='a', header=False)

def average_tier(filename):
    result = 0
    agg_num = 0
    header_list = ["Index","Tiers","Players"]
    data = pd.read_csv(filename, names=header_list)
    cus_mmr = pd.read_csv("DIA1~IRN4customized_mmr.csv", names = ['MMR'])
    for i in range(24):
        agg_num += data.iloc[i]['Players']
        result = result + (data.iloc[i]['Players'] * cus_mmr.iloc[i]['MMR'])
    avg_tier = result / agg_num
    return avg_tier

api_key = "RGAPI-6650c092-f632-4f41-9e15-136268b20ccb" # <----- put your api key
queue = "RANKED_SOLO_5x5"
tier_list = ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
division_list = ["I","II","III","IV"]
region = "na1" # <--------- edit this to attain data from another region ex: kr
today = date.today()
total_number(region) # <---- make a csv file that contains the number of players in each divisions (ex GOLD I or GOLD II) in the region
asd = average_tier("na1result010421.csv") # <------------ the average_tier of the region







