# Writer : Dongyoon Kim
# Date : 210401
# Description : Collecting the best five company which satisfy several conditions
#               from Naver in each industrial fields

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import pandas as pd
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe') #크롬을 사용할거다
url = 'https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=202' #이 url을
driver.get(url) #열어라

#gu_list = gu_list_raw.find_elements_by_tag_name('option')
#gu_name = [option.get_attribute('value') for option in gu_list]
#gu_name
buy_btn_xpath = '//*[@id="option2"]'
sell_btn_xpath = '//*[@id="option8"]'
marketcap_btn_xpath = '//*[@id="option4"]'
per_btn_xpath = '//*[@id="option6"]'
apply_btn_xpath = '//*[@id="contentarea"]/div[3]/form/div/div/div/a[1]/img'
driver.find_element_by_xpath(buy_btn_xpath).click() # buy버튼 클릭
driver.find_element_by_xpath(sell_btn_xpath).click() # sell버튼 클릭
driver.find_element_by_xpath(marketcap_btn_xpath).click() # 시가총액 버튼 클릭
driver.find_element_by_xpath(per_btn_xpath).click() # per버튼 클릭
driver.find_element_by_xpath(apply_btn_xpath).click() # per버튼 클릭

driver.implicitly_wait(3)

# PER 을 표시해주는 버튼을 클릭한다.

company_table_xpath = '//*[@id="contentarea"]/div[4]/table'
company_table = driver.find_element_by_xpath(company_table_xpath)
# 테이블을 찾고

#
# trs = company_table.find_elements_by_tag_name('tr')
# comp_names = [tr.text.split() for tr in trs]
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', attrs={'summary':'업종별 시세 리스트'})

# url 가져오기
base_url = 'https://finance.naver.com'
name_lists = table.find_all('div', attrs={'class':'name_area'})
links = [base_url+name.find('a')['href'] for name in name_lists]
name = [name.find('a').get_text() for name in name_lists]
# 회사명과 회사로 통하는 링크를 받아온다.

# 시가총액, PER 가져오기
trs = table.find_all('tr')
marketcap = [tr.find_all('td',class_='number')[6].text.strip() for tr in trs if len(tr.find_all('td',class_='number'))>1]
per = [tr.find_all('td',class_='number')[7].text.strip() for tr in trs if len(tr.find_all('td',class_='number'))>1]
# tr을 모두 가져와 6 - 시가총액 7 - PER 두 데이터를 뽑아 리스트에 담아준다.
# tr 중에서 td를 가져오되, class 이름이 number 인 것만 가져온다.
# 길이가 0 이상인 것만 더해준다.

#market_cap = []
columns = trs[0].text.split()
#per = []
code = []
reg_date = [] # 상장일
class__ = []
# 이제 해당 링크를 타고 가서 종목코드와 상장일을 가져온다.
count=0
for link in links:
    driver.get(link)
#    html = driver.page_source
#   여기선 셀레늄으로 데이터 추출해보자.
    kospi_xpath = '//*[@id="middle"]/div[1]/div[1]/div/img'
    kospi_or_kosdaq = driver.find_element_by_xpath(kospi_xpath).get_attribute('class')
    class__.append(kospi_or_kosdaq)
    code_num = driver.find_element_by_xpath('//*[@id="middle"]/div[1]/div[1]/div/span[1]').text
    code.append("A"+code_num)

    # 코스피 코스닥 정보 가져오기

    code_analysis_btn_xpath = '//*[@id="content"]/ul/li[6]/a/span' # 종목분석 버튼
    driver.find_element_by_xpath(code_analysis_btn_xpath).click()  # 종목분석 버튼 클릭
    # 기업개요는 안찾아짐. 어떻게 들어가지?
    driver.implicitly_wait(3)
    reg_site = 'https://navercomp.wisereport.co.kr/v2/company/c1020001.aspx?cn=&cmp_cd={code}&menuType=block'.format(code=code_num)
    driver.get(reg_site)

    driver.implicitly_wait(3)
    reg_day = driver.find_element_by_xpath('//*[@id="cTB201"]/tbody/tr[3]/td[1]').text # 상장일 찾아서
    reg_date.append(reg_day[-11:-1])
    count += 1

    # 일부 테스트를 위한 코드
    if count > 5:
        break

# print('ppppeeeerrrr')
# print(per[:10])
# print('marketttttcpa')
# print(marketcap[:10])
# print('name')
# print(name[:10])
# print('regggdateee')
# print(reg_date[:5])
# print('code')
# print(code[:5])
# 불러오는거 성공

# pd.DataFrame(data, columns=[comp_names[0],comp_names[]])
cols = ['name','code','class','market_cap','reg_day','per']
data = pd.DataFrame(
    {
        'name':name
        , 'code':code
        , 'class':class__
        , 'market_cap':marketcap
        , 'reg_day':reg_date
        , 'per':per
    }
)

# 이제 조건처리 등등 해야 함.