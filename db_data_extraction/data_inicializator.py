from db_connect import cursor
from utils import *
import re
import pycountry

def prepare_articles():
    query = "SELECT * FROM paper_references"
    cursor.execute(query)

    result = cursor.fetchall()
    for i in range(len(result)):
        row = result[i]
        row['Title'] = cleanText(row['Title'])
        row['Abstract'] = cleanText(row['Abstract'])
        row['Authors'] = cleanText(row['Authors'])
        row['Country'] = cleanText(row['Country'])
        row['Country_name'] = cleanText(row['Country_name'])
        result[i] = row

    return result

def prepare_authors(articles):
    name_regex = '\*\s*'
    result = []
    for article in articles:
        article_id = article['ID']
        author_names = re.split(",\s*", article['Authors'])
        countries = re.split(",\s*", article['Country'])
        for i in range(len(author_names)):
            author_id = len(result)+1
            aname = author_names[i]
            c = None 
            cname = None
            email = None
            corresponding = False

            if aname != '':
                if re.search(name_regex, aname):
                    corresponding = True
                    aname = re.sub(name_regex, '', aname)

                if corresponding:
                    # NOTE: esto no es correcto, habria que preguntar cual es la 
                    #       mejor forma de relacionar el mail con el author
                    email = article['Corresponding_author']

                if len(countries) > i:
                    country = pycountry.countries.get(alpha_2=countries[i])
                    if country:
                        c = country.alpha_2
                        cname = country.name
                
                author = {'ID': author_id,
                    'paperID': article_id,
                    'name': aname,
                    'email': email,
                    'country': c,
                    'country_name': cname
                    }
                
                result.append(author)

    return result