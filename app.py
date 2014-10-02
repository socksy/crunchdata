import companies as cl #company logic
import entities as en
import products as pd
from flask import Flask, render_template, request
import json
app = Flask(__name__)
#ugly hack to get something in global scope for the time being
companies = []

@app.route('/')
def root():
    return render_template('base.html')

@app.route('/company', methods=["POST"])
def company():
    raw_company = en.get_endpoint('organization/'+request.form["company"])[0]
    company = en.Entity(raw_company)
    return render_template('entity.html', entity=company)

@app.route('/companies')
def companies():
    return render_template('companies.html', entities=companies[:10])

@app.route('/products')
def products():
    return render_template('companies.html', entities=products[:10])

@app.route('/entity/<what>/<organization>')
def entity(what, organization):
    return json.dumps(en.get_individual_entity(what+'/'+organization))

if __name__ == "__main__":
    #companies = get_endpoint('organizations', 1, organization_types="company")
    #print(companies)
    companies = cl.get_companies()
    products = pd.get_products()
    app.run(debug=True)
