from typing import Iterable
import requests
import math


import re
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def getLatestFromTrud(n : int) -> Iterable:
    pages = math.ceil(n / 10)
    ans_tmp = []
    ans = []
    for i in range(pages):
        r = requests.get("https://trudvsem.ru/iblocks/_catalog/flat_filter_prr_search_vacancies/data?filter=%7B%22regionCode%22%3A%5B%225000000000000%22%5D%2C%22publishDateTime%22%3A%5B%22EXP_MAX%22%5D%7D&orderColumn=PUBLISH_DATE_DESC&page="+str(i)+"&pageSize=10")
        rjson = r.json()
        ans_tmp.extend([(x[0],x[2]) for x in rjson['result']['data']])
        

    for i in ans_tmp:
        r = requests.get('https://trudvsem.ru/iblocks/job_card?companyId='+i[-1]+'&vacancyId='+i[0])
        vacancy = r.json()['data']['vacancy']
        ans.append({
            'custom_position' : vacancy['vacancyName'],
            'description' : cleanhtml(vacancy.get('additionalRequirements','')) + cleanhtml(vacancy.get('positionResponsibilities', '')),
            'salary_from' : vacancy.get('salaryMin', 18000),
            'salary_to' : vacancy.get('salaryMax', 18000),
            'link' : 'https://trudvsem.ru/vacancy/card/'+i[-1]+'/'+i[0],
        })
    return ans

print(getLatestFromTrud(30))