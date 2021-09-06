from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

'''
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)'''
cpath = "C:\python\chromedriver.exe"
driver = webdriver.Chrome(cpath)
driver.get("https://www.indiansuperleague.com/schedule-fixtures")
driver.maximize_window()
time.sleep(2)
driver.find_element_by_id("cookiebtn").click()
time.sleep(2)

driver.find_element_by_class_name("btn-topscroll").click()
time.sleep(2)
driver.find_element_by_css_selector("div[class='si-dropdwn si-btn-radius ']").click()
driver.find_element_by_css_selector("li[data-value='All']").click()
time.sleep(3)
driver.find_element_by_class_name("btn-topscroll").click()
time.sleep(2)
#matches = driver.find_elements_by_class_name("si-fix-body")
ml = driver.find_elements_by_css_selector("a[class='si-btn si-btn-secondary-outline si-btn-radius']")
mtchlnk = []
for i in range(0,len(ml)):
    mtchlnk.append(ml[i].get_attribute("href"))
print(mtchlnk)
data = []

for i in range(0,len(mtchlnk)):
    #mtchlnk = ml[i].get_attribute("href")
    driver.get(mtchlnk[i])
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='siMtcTabs']/div/ul/li[4]").click()
    time.sleep(2)
    hposs = driver.find_element_by_class_name("si-mc-evntSats-teamA-Scr").text
    aposs = driver.find_element_by_class_name("si-mc-evntSats-teamB-Scr").text
    hpass = driver.find_element_by_xpath("//*[@id='siMtcTabsClickContainer']/div[2]/div/div/div[4]/div[1]/div[1]/div/div[1]/span").text
    apass = driver.find_element_by_xpath("//*[@id='siMtcTabsClickContainer']/div[2]/div/div/div[4]/div[1]/div[2]/div/div[1]/span").text
    time.sleep(2)
    hlist = driver.find_elements_by_class_name("si-mc-evntSats-pgrStats")
    htscore = hlist[0].text
    atscore = hlist[1].text
    hoff = hlist[2].text
    aoff = hlist[3].text
    hsot = hlist[4].text
    asot = hlist[5].text
    hsofft = hlist[6].text
    asofft = hlist[7].text
    hnop = hlist[8].text
    anop = hlist[9].text
    ht = hlist[10].text
    at = hlist[11].text
    hf = hlist[12].text
    af = hlist[13].text
    hi = hlist[14].text
    ai = hlist[15].text
    hcross = hlist[16].text
    across = hlist[17].text
    hcorn = hlist[18].text
    acorn = hlist[19].text
    hrc = hlist[20].text
    arc = hlist[21].text
    hyc = hlist[22].text
    ayc = hlist[23].text
    x = mtchlnk[i]
    y = (x.split("-", 1))[1]
    y = y.replace("-", "")
    hteam = (y.split("vs"))[0]
    ateam = (y.split("vs"))[1]
    data.append([hteam, ateam, htscore, atscore, hposs, aposs, hpass, apass, hoff, aoff, hsot, asot, hsofft, asofft,
                 hnop, anop, ht, at, hf, af, hi, ai, hcross, across, hcorn, acorn, hrc, arc, hyc, ayc])

finaldata = pd.DataFrame(data, columns=['HomeTeam', 'AwayTeam', 'HometeamScore', 'AwayteamScore', 'HomePossesion', 'AwayPossesion',
                                        'HomePassingAccuracy', 'AwayPassingAccuracy', 'HomeOffSides', 'AwayOffSides', 'HomeShotsOnGoal',
                                        'AwayShotsOnGoal', 'HomeShotsOffTarget', 'AwayShotsOffTarget', 'HomePasses', 'AwayPasses',
                                        'HomeTouches', 'AwayTouches', 'HomeFouls', 'AwayFouls', 'HomeInterceptions', 'AwayInterceptions',
                                        'HomeCrosses', 'AwayCrosses', 'HomeCorners', 'AwayCorners', 'HomeRedCards', 'AwayRedCards',
                                        'HomeYellowCards', 'AwayYellowCards'])
finaldata.to_csv('isl.csv',index=False)
driver.close()

'''for i in range(0,len(matches)):
    ml = matches[i].find_element_by_css_selector("a.si-btn")
    mtchlnk = ml.get_attribute("href")
    ht = matches[i].find_element_by_class_name("si-team-one")
    hteam = ht.find_element_by_class_name("si-team-name")
    at = matches[i].find_element_by_class_name("si-team-two")
    ateam = at.find_element_by_class_name("si-team-name")
    sc = matches[i].find_element_by_class_name("si-team-vs")
    score = sc.find_elements_by_tag_name("span")
    htscore = (score[0].text)
    atscore = (score[2].text)
    driver.get(mtchlnk)
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='siMtcTabs']/div/ul/li[4]").click()
    time.sleep(2)
    #driver.execute_script("window.history.go(-1)")
    #data.append([hteam.text,htscore,atscore,ateam.text])'''