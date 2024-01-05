from requests import get
from bs4 import *
from convertpersianhelp import *
import openpyxl

document = get("https://www.findatour.co/fa/travel-agency/page/21").content

bs = BeautifulSoup(document,'html.parser')
agents = bs.findAll('a',class_='view more-btn')

links = [ f"https:{i.attrs['href'].strip()}" for i in agents]

num = 2000
for li in links:
    num += 1
    agdoc = BeautifulSoup(get(li).content,'html.parser')
    headdiv = agdoc.find('div',class_='agnacy-header')
    divtel = agdoc.findAll('div', class_='col-md-6')
    for i,b in zip(divtel,range(3)):
        if b == 0:
            try:
                telephon = i.find('p')
                telephon = telephon.text[6:].strip() 
            except:
                telephon = ''
        elif b == 1:
            try:
                phone = i.find('p')
                phone = phone.text[11:].strip()
            except:
                phone = ''
        elif b == 2:
            try:
                what = i.find('p')
                what = what.text[11:].strip()
            except:
                what = ''
        try:
            addres = agdoc.findAll("div",class_='row form-group')
            addres = addres[1].text[8:].strip()
        except:
            addres = ''
        try:
            website = agdoc.find('p',class_='website')
            website = website.text[9:].strip()
            weblink = website
            if len(weblink) > 3:
                website = 'دارد'
            else:
                website = 'ندارد'

        except:
            website = 'ندارد'
    try:
        if get(weblink,timeout=5).status_code == 200:
            website_status = 'فعال'
        else:
            website_status = 'غیره فعال'
    except:
        try:
            if get('http:'+weblink,timeout=5).status_code == 200:
                website_status = 'فعال'
            else:
                website_status = 'غیره فعال'
        except:
            try:
                if get('https:'+weblink,timeout=5).status_code == 200:
                    website_status = 'فعال'
                else:
                    website_status = 'غیره فعال'
            except:
                try:
                    if get('http://'+weblink,timeout=5).status_code == 200:
                        website_status = 'فعال'
                    else:
                        website_status = 'غیره فعال'
                except:
                    try:
                        if get('https://'+weblink,timeout=5).status_code == 200:
                            website_status = 'فعال'
                        else:
                            website_status = 'غیره فعال'
                    except:
                        website_status = 'غیره فعال'
    newitem = [headdiv.text.strip(),telephon,phone,what,addres,website,website_status,weblink]
    book = openpyxl.load_workbook('safar-agent.xlsx')
    sheet = book.active
    sheet.append(newitem)
    book.save('safar-agent.xlsx')
    print(num)
print('collecting done.')
