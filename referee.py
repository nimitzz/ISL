import time
from selenium import webdriver
import pandas as pd
cpath = "C:\python\chromedriver.exe"
driver = webdriver.Chrome(cpath)
driver.get("https://www.indiansuperleague.com/stats/202-115-isl-referee-statistics")
driver.maximize_window()
time.sleep(2)
driver.find_element_by_id("cookiebtn").click()
time.sleep(2)
nlist = driver.find_elements_by_class_name("si-fullName")

m0 = driver.find_element_by_css_selector("div[class='si-tCel si-points si-FntSize']")
mlist = driver.find_elements_by_css_selector("div[class='si-tCel si-points']")


fa0 = driver.find_elements_by_css_selector("div[class='si-tCel si-gamplyd si-FntSize']")
falist = driver.find_elements_by_css_selector("div[class='si-tCel si-gamplyd']")

data = []
data.append([nlist[0].text, m0.text, fa0[0].text, fa0[1].text, fa0[2].text, fa0[3].text])
nlist.pop(0)
faw = []
rc = []
yc = []
tc = []

for j in range(0, len(falist), 4):
    faw.append(falist[j].text)
    tc.append(falist[j+1].text)
    yc.append(falist[j+1].text)
    rc.append(falist[j+3].text)


for i in range(0,len(nlist)):
    data.append([nlist[i].text, mlist[i].text, faw[i], tc[i], yc[i], rc[i]])

final_data = pd.DataFrame(data, columns=['Name','Matches' ,'FoulsAwarded' , 'TotalCards', 'YellowCards', 'RedCards'])
final_data.to_csv('ref.csv',index=False)
driver.close()