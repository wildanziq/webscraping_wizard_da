from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class': 'history-rates-data'})
print(table.prettify()[1:500])

table.find_all('a', attrs={'class': 'w'})
table.find_all('a', attrs={'class': 'w'})[1].text

table.find_all('span', attrs={'class': 'w'})
table.find_all('span', attrs={'class': 'w'})[1].text

row = table.find_all('a', attrs={'class': 'w'})
row_length = len(row)
row_length

temp = [] #initiating a list 

for i in range(0, row_length):
    # insert the scrapping process here
    
    date = table.find_all('a', attrs={'class': 'w'})[i].text
    date = date.strip()
        
    rate = table.find_all('span', attrs={'class': 'w'})[i].text
    rate = rate.strip()
    
    temp.append((date, rate))

    
temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','rate'))


#insert data wrangling here
df['date'] = pd.to_datetime(df['date'])
df['rate'] = df['rate'].str.replace('$1 = Rp', '').str.replace(',', '')
df['rate'] = df['rate'].astype('float64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	plt.figure(figsize=(20, 6))
	plt.plot(df['date'], df['rate'], marker='o', linestyle='-')
	plt.xlabel('Date')
	plt.ylabel('Exchange Rate (USD to IDR)')
	plt.grid(True)
	plt.tight_layout()
	plt.show() 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)