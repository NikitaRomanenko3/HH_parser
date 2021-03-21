import requests
from bs4 import BeautifulSoup


headers = {
    'Host': 'rabota.by',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}


def extract_last_page(url):
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, 'html.parser')
    last_page = html.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].a.text
    return int(last_page)


def get_job_attributes(job):
    vacancy = job.a.text
    company = job.find_all('div', {'class': 'vacancy-serp-item__meta-info'})[0].a.text
    location = job.find_all('div', {'class': 'vacancy-serp-item__meta-info'})[1].span.text.split(',')[0]
    link = job.a['href']
    temp_dict = {'vacancy': vacancy, 'company': company, 'location': location, 'link': link}
    return temp_dict


def get_jobs_list(url, last_page):
    jobs = []
    for page in range(last_page):
        r = requests.get(f'{url}&page={page}', headers=headers)
        html = BeautifulSoup(r.text, 'html.parser')
        temp_list = html.find_all('div', {'class': 'vacancy-serp-item'})
        for job in temp_list:
            jobs.append(get_job_attributes(job))

    return jobs


def hh_extract_jobs(keyword):
    url = f'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&st=searchVacancy&text={keyword}'
    max_page = extract_last_page(url)
    jobs = get_jobs_list(url, max_page)
    return jobs


