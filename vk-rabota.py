from typing import Iterable
import requests
import math


def getLatestFromVk(n : int) -> Iterable:
    pages = math.ceil(n / 20)
    ans_tmp = []
    ans = []
    for i in range(pages):
        r = requests.get("https://api.iconjob.co/api/web/v1/jobs?sort=fresh&page="+str(i)+"&per_page=20")
        ans_tmp.extend(r.json()['jobs'])
    for i in ans_tmp:
        if len(i['professions'])>0:
            ans.append({
                'custom_position' :i['professions'][0]['title'] ,
                'description' : i['description'],
                'salary_from' : i['salary_from'],
                'salary_to' : i['salary_to'],
                'link' : "https://vkrabota.ru/vacancy/"+i['hashid'],
            })
        else:
            ans.append({
                'custom_position' :  i['title'],
                'description' : i['description'],
                'salary_from' : i['salary_from'],
                'salary_to' : i['salary_to'],
                'link' : "https://vkrabota.ru/vacancy/"+i['hashid'],
            })
    return ans

print(getLatestFromVk(60))