import asyncio
import httpx
import pandas as pd
import sys
import os
from bs4 import BeautifulSoup
import re

async def get_random_user_agent(client) -> str:
    """
    Returns a random user agent string.
    
    Returns:
        str : Random user agent string.
    """
    url = "https://randua.somespecial.one/"
    try:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    except Exception as e:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    

async def get_hidden_input(content):
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

async def shareholding_requester(client:httpx.Client,instrument:dict) -> dict:
    code = instrument['Security Code']
    print(code)
    rand_user_agent = await get_random_user_agent(client)
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

    hidden = await get_hidden_input(response.content)
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
    hidden = await get_hidden_input(response.content)
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

async def shareholding_pattern(file_name) -> pd.DataFrame:
    data = pd.read_csv(file_name)
    data["market_cap"] = ""
    data = data.to_dict(orient='records')

    async with httpx.AsyncClient() as client:
        chunks = [data[i:i+20] for i in range(0, len(data), 20)]
        results = []
        for chunk in chunks:
            tasks = [shareholding_requester(client, instrument) for instrument in chunk]
            chunk_results = await asyncio.gather(*tasks)
            results.extend(chunk_results)
    return results

async def main(arg:str):
    data = await shareholding_pattern(arg)
    df = pd.DataFrame(data)
    df.to_csv(arg, index=False)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))