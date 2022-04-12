import requests
import bs4

def get_now_grade(name):
    url = "http://codeforces.com/profile/"+name+"#"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    ls = soup.select('#pageContent > div:nth-child(3) > div.userbox > div.info > ul > li:nth-child(1)')
    tmp = ls[0].text.strip()
    str_tmp=tmp.replace(' ','').split('\n')[2]
    grade = str_tmp[0:str_tmp.find('(')]
    max_specialist = str_tmp[str_tmp.find(',')+1:len(str_tmp)-1]
    return grade,max_specialist


if __name__ == "__main__":
    name = 'tourist'
    res = get_now_grade(name)
    now = res[0]
    max = res[1]
    print(name)
    print('now : %s\nmax : %s'%(now,max))