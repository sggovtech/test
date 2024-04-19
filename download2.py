import asyncio
import httpx
import pandas as pd
import sys
import os
from bs4 import BeautifulSoup
import re
import random
import urllib
import json


async def get_random_user_agent() -> str:
    """
    Returns a random user agent string.
    
    Returns:
        str : Random user agent string.
    """
    agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Geck",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.6",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.7",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.5",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.6",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4450.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.5",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.3",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Whale/3.21.192.18 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.4",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.5",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.11",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.",
                "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.6",
                "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Geck",
                "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.3",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
                "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.72",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
                "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.115",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/255.0.515161012 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-N960F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/113.0.5672.121 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (Linux; Android 11; SM-A217F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 11; 22011119UY) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 10; JNY-LX1; HMSCore 6.11.0.302) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/14.0.0.323 Mobile Safari/537.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.124 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (Linux; Android 12; SM-A217F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 10; SM-A750FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A326B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A226B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.3",
                "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.",
                "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A336B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20.0 Chrome/106.0.5249.126 Mobile Safari/537.3",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.0.0; SM-G570F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36 OPR/76.2.4027.73374",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.124 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"
                ]
    return random.choice(agents)
    

async def B_get_hidden_input(content):
    """ Return the dict contain the hidden input 
    """
    tags = dict()
    soup = BeautifulSoup(content, 'html.parser')
    hidden_tags = soup.find_all('input', type='hidden')
    for tag in hidden_tags:
        try:
            name = tag.get('name')
            value = tag.get('value')
            if value is not None or value != '':
                tags[name] = value
            else:
                tags[name] = ''
        except Exception as e:
            continue
    return tags

async def B_shareholding_requester(client:httpx.Client,instrument:dict) -> dict:
    code = instrument['Security Code']
    print(code)
    rand_user_agent = await get_random_user_agent()
    headers = {"User-Agent": rand_user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://www.bseindia.com", "Referer": "https://www.bseindia.com/markets/equity/eqreports/bulknblockdeals.aspx", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
    url = os.environ["URL3"]
    while True:
        try:
            response = await client.get(url, headers=headers)
            break
        except httpx.ReadTimeout:
            pass
        except httpx.ConnectTimeout:
            pass
        except httpx.HTTPError:
            pass
        except Exception as e:
            break

    hidden = await B_get_hidden_input(response.content)
    values = {
        'ctl00$ContentPlaceHolder1$hdnCode':'',
        'ctl00$ContentPlaceHolder1$industry':'ALL',
        'ctl00$ContentPlaceHolder1$brodcast':'1',
        'ctl00$ContentPlaceHolder1$scrip':code,
        'ctl00$ContentPlaceHolder1$Hidden1':'',
        'ctl00$ContentPlaceHolder1$SmartSearch$hdnCode':code,
        'ctl00$ContentPlaceHolder1$SmartSearch$smartSearch':'',
        'ctl00$ContentPlaceHolder1$hf_scripcode':code,
        'ctl00$ContentPlaceHolder1$ddlbrodcast':7,
        'ctl00$ContentPlaceHolder1$ddlindustry':'ALL',
        'ctl00$ContentPlaceHolder1$btnSubmit':'Submit'
    }
    join_hidden = {**hidden, **values}
    while True:
        try:
            response = await client.post(url, headers=headers, data=join_hidden)
            break
        except httpx.ReadTimeout:
            pass
        except httpx.ConnectTimeout:
            pass
        except httpx.HTTPError:
            pass
        except Exception as e:
            break
    hidden = await B_get_hidden_input(response.content)
    values = {
                "__EVENTTARGET": "ctl00$ContentPlaceHolder1$gvData$ctl02$lnkXML",
                "__EVENTARGUMENT": '', 
                "ctl00$ContentPlaceHolder1$hdnCode": '',
                "ctl00$ContentPlaceHolder1$industry": "ALL",
                "ctl00$ContentPlaceHolder1$brodcast": "7",
                "ctl00$ContentPlaceHolder1$scrip": code,
                "ctl00$ContentPlaceHolder1$Hidden1": '',
                "ctl00$ContentPlaceHolder1$SmartSearch$hdnCode": code,
                "ctl00$ContentPlaceHolder1$SmartSearch$smartSearch": '',
                "ctl00$ContentPlaceHolder1$hf_scripcode": code,
                "ctl00$ContentPlaceHolder1$ddlbrodcast": 7,
                "ctl00$ContentPlaceHolder1$ddlindustry": "ALL"
            }
    join_hidden = {**hidden, **values}
    while True:
        try:
            response = await client.post(url, headers=headers, data=join_hidden,follow_redirects=True)
            break
        except httpx.ReadTimeout:
            pass
        except httpx.ConnectTimeout:
            pass
        except httpx.HTTPError:
            pass
        except Exception as e:
            break
    # print(response.text)
    if "<xbrli" in response.text:
        num_shares = re.findall(r'<in-bse-shp:NumberOfFullyPaidUpEquityShares contextRef="ShareholdingPattern_ContextI" unitRef="shares" decimals="INF">(\d+)</in-bse-shp:NumberOfFullyPaidUpEquityShares>', response.text)
        if len(num_shares) > 0:
            num_shares = int(num_shares[0])
            instrument["market_cap"] = num_shares
            return instrument
        else:   
            return instrument
    else:
        return instrument

async def N_shareholding_requester(client,instrument:dict) -> dict:
    N_code = instrument['SYMBOL']
    print(N_code)
    N_name = instrument['NAME OF COMPANY']
    user_agent = await get_random_user_agent()
    url1 = os.environ["URL6"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers"}
    while True:
        try:
            resp1 = await client.get(url1, headers=headers,follow_redirects=True)
            break
        except httpx.ReadTimeout:
            print(1)
            pass
        except httpx.ConnectTimeout:
            print(2)
            pass
        except httpx.HTTPError:
            print(3)
            pass
        except Exception as e:
            break
    cookies_dict = {k: v for k, v in resp1.cookies.items()}
    url2 = os.environ["URL7"]+f"symbol={N_code}&issuer={urllib.parse.quote(N_name, safe='')}"
    while True:
        try:
            resp2 = await client.get(url2, headers=headers, cookies=cookies_dict)
            break
        except httpx.ReadTimeout:
            print(4)
            pass
        except httpx.ConnectTimeout:
            print(5)
            pass
        except httpx.HTTPError:
            print(6)
            pass
        except Exception as e:
            break
    data = json.loads(resp2.text) 
    if len(data) > 0:
        xrbl_url = data[0]['xbrl']
        while True:
            try:
                resp3 = await client.get(xrbl_url, headers=headers)
                break
            except httpx.ReadTimeout:
                print(7)
                pass
            except httpx.ConnectTimeout:
                print(8)
                pass
            except httpx.HTTPError:
                print(9)
                pass
            except Exception as e:
                break
        if "<xbrli" in resp3.text:
            num_shares = re.findall(r'<in-bse-shp:NumberOfFullyPaidUpEquityShares contextRef="ShareholdingPatternI" unitRef="shares" decimals="INF">(\d+)</in-bse-shp:NumberOfFullyPaidUpEquityShares>', resp3.text)
            if len(num_shares) > 0:
                num_shares = int(num_shares[0])
                instrument["market_cap"] = num_shares
                return instrument
            else:
                return instrument
        else:
            return instrument




async def shareholding_pattern(file_pattern) -> tuple[pd.DataFrame,pd.DataFrame]:
    B_file_name = f"B_instruments_{file_pattern}.csv"
    N_file_name = f"N_instruments_{file_pattern}.csv"
    B_data = pd.read_csv(B_file_name)
    N_data = pd.read_csv(N_file_name)
    B_data["market_cap"] = ""
    N_data["market_cap"] = ""
    B_data = B_data.to_dict(orient='records')
    N_data = N_data.to_dict(orient='records')

    async with httpx.AsyncClient() as client:
        B_chunks = [B_data[i:i+20] for i in range(0, len(B_data), 20)]
        N_chunks = [N_data[i:i+20] for i in range(0, len(N_data), 20)]
        B_results = []
        N_results = []
        for chunk in B_chunks :
            client.cookies.clear()
            tasks = [B_shareholding_requester(client, instrument) for instrument in chunk]
            chunk_results = await asyncio.gather(*tasks)
            B_results.extend(chunk_results)
        for chunk in N_chunks :
            client.cookies.clear()
            tasks = [N_shareholding_requester(client,instrument) for instrument in chunk]
            chunk_results = await asyncio.gather(*tasks)
            N_results.extend(chunk_results)
    return B_results, N_results

async def main(arg:str):
    B_data,N_data = await shareholding_pattern(arg)
    B_df = pd.DataFrame(B_data)
    B_df.to_csv(f"B_instruments_{arg}.csv", index=False)
    N_df = pd.DataFrame(N_data)
    N_df.to_csv(f"N_instruments_{arg}.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))