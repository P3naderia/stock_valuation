import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pathlib
import shutil

GA_ID = "google_analytics"
GA_SCRIPT = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LP0EX3CCDH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-LP0EX3CCDH');
</script>
"""

def inject_ga(): 
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID): 
        bck_index = index_path.with_suffix('.bck')
        try:
            if bck_index.exists():
                shutil.copy(bck_index, index_path)  
            else:
                shutil.copy(index_path, bck_index)  
        except Exception as e:
            st.error(f"Error occurred while copying file: {e}")
            return
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_SCRIPT)
        try:
            index_path.write_text(new_html)
        except Exception as e:
            st.error(f"Error occurred while writing HTML: {e}")
            shutil.copy(bck_index, index_path)

def get_stats_valuation(ticker, headers={'User-agent': 'Mozilla/5.0'}):
    '''Scrapes Valuation Measures table from the statistics tab on Yahoo Finance 
       for an input ticker 
    
       @param: ticker
    '''

    stats_site = "https://finance.yahoo.com/quote/" + ticker + "/key-statistics?p=" + ticker
    
    try:
        tables = pd.read_html(requests.get(stats_site, headers=headers).text)
        tables = [table for table in tables if "Trailing P/E" in table.iloc[:, 0].tolist()]
        if tables:
            table = tables[0].reset_index(drop=True)
            return table
        else:
            return None
    except Exception as e:
        st.error(f"Error occurred while scraping data: {e}")
        return None

def main():
    inject_ga()  # Google Analytics 코드 삽입
    st.title('Yahoo Finance Valuation Measures Scraper')
    ticker = st.text_input('Enter Ticker Symbol (e.g., AAPL):')

    if st.button('Get Valuation Measures'):
        if ticker:
            valuation_table = get_stats_valuation(ticker)
            if valuation_table is not None:
                st.write(valuation_table)  # 데이터를 화면에 출력
            else:
                st.warning(f"No valuation measures found for ticker {ticker}.")
        else:
            st.warning('Please enter a valid ticker symbol.')

if __name__ == "__main__":
    main()

