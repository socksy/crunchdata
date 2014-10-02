import companies as cl #company logic
import entities as en
from flask import Flask, render_template
import json
app = Flask(__name__)
#ugly hack to get something in global scope for the time being
companies = []

@app.route('/')
def root():
    return render_template('base.html')

@app.route('/companies')
def companies():
    return render_template('companies.html', entities=companies[:10])

@app.route('/entity/<what>/<organization>')
def entity(what, organization):
    return json.dumps(en.get_individual_entity(what+'/'+organization))

if __name__ == "__main__":
    #companies = get_endpoint('organizations', 1, organization_types="company")
    #print(companies)
    companies = cl.get_companies()
    app.run(debug=True)
