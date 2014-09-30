import companies as cl #company logic
from flask import Flask, render_template
app = Flask(__name__)
#ugly hack to get something in global scope for the time being
companies = []
@app.route('/')
def companies():
    for company in companies[:10]:
        company.get_additional_info()
    return render_template('companies.html', companies=companies)

if __name__ == "__main__":
#    companies = get_endpoint('organizations', 1, organization_types="company")
#    print(companies)
    companies = cl.get_companies()
    app.run(debug=True)
