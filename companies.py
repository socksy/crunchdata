import entities

def get_companies():
    raw_companies = entities.get_endpoint('organizations', 1, organization_types="company")
    #TODO change this so we can sanely deal with pagination
    companies = []
    for company in raw_companies[:10]:
        companies.append(entities.Entity(company))
        print('c')
    return companies

