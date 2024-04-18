import requests
import pandas as pd
import io
import os
import numpy as np


def download_instruments(url) -> pd.DataFrame:
    session = requests.session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.bseindia.com/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-site", "Sec-Fetch-User": "?1", "Te": "trailers"}
    response = session.get(os.environ["URL1"], headers=headers)
    data = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(data))
    return df

url1 = os.environ["URL1"]
url2 = os.environ["URL2"]
df1 = download_instruments(url1)
df2 = download_instruments(url2)
combined_df = pd.concat([df1, df2])
dfs = np.array_split(combined_df, 19)
for i, df in enumerate(dfs, 1):
    df.to_csv(f"B_instruments_{i}.csv", index=False)