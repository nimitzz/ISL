import time
from selenium import webdriver
import pandas as pd
cpath = "C:\python\chromedriver.exe"
driver = webdriver.Chrome(cpath)
driver.get("https://www.indiansuperleague.com/stats")
driver.maximize_window()
time.sleep(2)
driver.find_element_by_id("cookiebtn").click()
time.sleep(2)

def get_data(url):
    driver.get(url)

    time.sleep(2)
    more = driver.find_element_by_css_selector("div[class='si-btn si-btn-radius si-stats-more-btn']")
    for h in range(1, 12):
        try:
            #driver.execute_script("arguments[0].scrollIntoView();", more)
            more.click()
            time.sleep(5)
        except:
            pass

    awrd = driver.find_element_by_class_name("si-awdPlyrName")
    pl = awrd.find_element_by_class_name("si-fullName").text
    club = driver.find_element_by_class_name("si-plyrClubnm")
    cl = club.find_element_by_class_name("si-fullName").text
    pm = driver.find_element_by_class_name("si-plyStats-gamePlyd-cel").text
    gs = driver.find_element_by_class_name("si-points").text
    data = []
    data.append([pl,cl,pm,gs])
    olis = driver.find_elements_by_css_selector("div[class = 'si-fullName ']")
    pnlist = []
    tlist = []
    for i in range(0,len(olis)):
        if i == 0:
            pnlist.append(olis[i].text)
        elif (i % 2) != 0:
            tlist.append(olis[i].text)
        elif (i % 2) == 0:
            pnlist.append(olis[i].text)
    mplist = driver.find_elements_by_css_selector("div[class = 'si-tCel si-gamplyd ']")
    gslist = driver.find_elements_by_css_selector("div[class = 'si-tCel si-gamplyd si-plyStats-gamplyd']")
    for j in range(0,len(gslist)):
        data.append([pnlist[j],tlist[j], mplist[j].text, gslist[j].text])
    return data

datagoals =get_data("https://www.indiansuperleague.com/stats/148-138-goals-player-statistics")
datacleansheets = get_data("https://www.indiansuperleague.com/stats/148-141-clean-sheets-player-statistics")
dataassist = get_data("https://www.indiansuperleague.com/stats/148-153-assists-player-statistics")
datainterceptions = get_data("https://www.indiansuperleague.com/stats/148-149-interceptions-player-statistics")
datasaves = get_data("https://www.indiansuperleague.com/stats/148-140-saves-player-statistics")
datatackles = get_data("https://www.indiansuperleague.com/stats/148-147-tackles-player-statistics")

fd1 = pd.DataFrame(datagoals, columns=['Name', 'Club', 'Matches', 'Goals'])
fd2  = pd.DataFrame(datacleansheets, columns=['Name', 'Club', 'Matches', 'CleanSheets'])
fd3  = pd.DataFrame(dataassist, columns=['Name', 'Club', 'Matches', 'Assists'])
fd4  = pd.DataFrame(datainterceptions, columns=['Name', 'Club', 'Matches', 'Interceptions'])
fd5  = pd.DataFrame(datasaves, columns=['Name', 'Club', 'Matches', 'Saves'])
fd6  = pd.DataFrame(datatackles, columns=['Name', 'Club', 'Matches', 'Tackles'])

fd2 = fd2.drop(['Club', 'Matches'], axis=1)
fd7 = pd.merge(fd2, fd5, on='Name')

fd8 = pd.merge(fd3, fd1, on='Name', how='outer')
fd9 = pd.merge(fd6, fd4, on='Name', how='outer')


def milaap(df, col):
    c1 = col + '_x'
    c2 = col + '_y'
    df[col] = list(zip(df[c1], df[c2]))
    df[col] = df[col].apply(lambda x: x[1])


milaap(fd8, 'Club')
milaap(fd8, 'Matches')
fd8 = fd8.drop(['Club_x', 'Club_y', 'Matches_x', 'Matches_y'], axis=1)
milaap(fd9, 'Club')
milaap(fd9, 'Matches')
fd9 = fd9.drop(['Club_x', 'Club_y', 'Matches_x', 'Matches_y'], axis=1)
fd10 = pd.merge(fd9, fd8, on='Name', how='outer')
milaap(fd10, 'Club')
milaap(fd10, 'Matches')
fd10 = fd10.drop(['Club', 'Club_y', 'Matches', 'Matches_y'], axis=1)
fd10['Club'] = fd10['Club_x']
fd10['Matches'] = fd10['Matches_x']
fd10 = fd10.drop(['Club_x', 'Matches_x'], axis=1)

final_data = pd.concat([fd10,fd7], axis=0)
final_data = final_data.fillna(0)
cmn = final_data.columns.tolist()
colm = []
colm.append(cmn[0])
colm.append(cmn[5])
colm.append(cmn[6])
colm.append(cmn[1])
colm.append(cmn[2])
colm.append(cmn[3])
colm.append(cmn[4])
colm.append(cmn[7])
colm.append(cmn[8])
final_data = final_data[colm]
final_data.to_csv('stat.csv',index=False)

driver.close()