import streamlit as st
import pandas as pd
import requests

GA_SCRIPT = """
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LP0EX3CCDH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-LP0EX3CCDH');
</script>
"""

def get_stats_valuation(ticker, headers = {'User-agent': 'Mozilla/5.0'}):
    '''Scrapes Valuation Measures table from the statistics tab on Yahoo Finance 
       for an input ticker 
    
       @param: ticker
    '''

    stats_site = "https://finance.yahoo.com/quote/" + ticker + \
                 "/key-statistics?p=" + ticker
    
    tables = pd.read_html(requests.get(stats_site, headers=headers).text)
    
    tables = [table for table in tables if "Trailing P/E" in table.iloc[:,0].tolist()]
    
    table = tables[0].reset_index(drop = True)
    
    return table

def main():
    st.title('Yahoo Finance Valuation Measures Scraper')
    ticker = st.text_input('Enter Ticker Symbol (e.g., AAPL):')

    if st.button('Get Valuation Measures'):
        if ticker:
            try:
                valuation_table = get_stats_valuation(ticker)
                st.write(valuation_table)  # 데이터를 화면에 출력
            except Exception as e:
                st.error(f"Error occurred: {e}")
        else:
            st.warning('Please enter a valid ticker symbol.')

    # Google Analytics 스크립트 삽입
    st.write(GA_SCRIPT, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
