import json
import requests
import csv

from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = {}


with open('exchangerates.csv', 'w', newline='') as csvfile:
       fieldnames = ['currency', 'code', 'bid', 'ask']
       writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
       writer.writeheader()
       for r in rates:          
         writer.writerow({'currency': r["currency"], 'code': r["code"],'bid': r["bid"], 'ask': r["ask"]})



def convert(amount, ask):
    return "%.2f" % (float(amount) * float(ask))

@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        data = request.form
        amount = data.get('amount')
        code = data.get('codes') 
        for r in rates:
            if rates[r][0] == code:
                name_currency = r
                ask = float(rates[r][2])
        costs = convert(amount, ask)
        result =  f" {costs} PLN"
        return render_template("currency_calculator.html", result=result)
    return render_template("currency_calculator.html")

if __name__ == "__main__":
    app.run()


