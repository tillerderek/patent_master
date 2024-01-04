from flask import Flask, request, abort, render_template
from flask_httpauth import HTTPBasicAuth
from patent_client import Inpadoc
from datetime import datetime
from titlecase import titlecase

app = Flask(__name__)
auth = HTTPBasicAuth()

USERNAME = 'patent'
PASSWORD = 'bigMoneybig$how'

@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD

@app.route("/")
@auth.login_required
def index():
    patNumber = request.args.get("patNumber", "")
    if patNumber:
        patentSelect = get_patent_info(patNumber)
    else:
        patentSelect = ""
        
    return render_template("index.html", patentSelect=patentSelect)

def format_date(date):
    formatted_date = date.strftime('%B %d, %Y')
    return formatted_date

def get_patent_info(patNumber):
    try:
        pub = Inpadoc.objects.get(f"US{patNumber}")
        inventors = pub.biblio.inventors_original
        title = pub.biblio.title
        abstract = pub.biblio.abstract
        formNum = "{:,}".format(int(patNumber))
        date = pub.biblio.publication_reference_docdb.date
        google = f"https://patents.google.com/patent/US{patNumber}"
        response = ""

        if formNum:
            response += "<h2>Patent Number:</h2>"
            response += f"<p>{formNum}</p>"
        else:
            response += "<p>Patent Number: Not Found</p>"

        if date:
            formatted_date = format_date(date)
            response += "<h2>Publication Date:</h2>"
            response += f"<p>{formatted_date}</p>"
        else:
            response += "<p>Publication Date: Not Found</p>"

        if inventors:
            response += f"<h2>Inventors:</h2>"
            for inventor in inventors:
                response += f"<p>{inventor.title()}</p>"
        else:
            response += "<p>Inventors: Not Found</p>"

        if title:
            response += f"<h2>Title:</h2>"
            response += f"<p>{titlecase(title)}</p>"
        else:
            response += "<p>Title: Not Found</p>"

        if abstract:
            response += f"<h2>Abstract:</h2>"
            response += f"<p>{abstract}</p>"
        else:
            response += "<p>Abstract: Not Found</p>"
            
        response += f"<h2>Google Patents:</h2>"
        response += f"<a href='{google}' target='blank'>Google Patents Link</a>"

        return response
    
    except ValueError as e:
        return str(e), ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
