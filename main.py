from flask import Flask, request
from patent_client import Inpadoc
from datetime import datetime
from titlecase import titlecase

app = Flask(__name__)

@app.route("/")
def index():
    patNumber = request.args.get("patNumber", "")
    if patNumber:
        patentSelect = get_patent_info(patNumber)
    else:
        patentSelect = ""
        
    return (
        """<form action="" method="get">
                <p><label for="number">Input individual numbers here:</label>
                <input type="text" name="patNumber">
                </p>
                <p><input type="submit" value="Submit"></p>   
            </form>""" 
        + patentSelect
    )

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
        image = pub.images.first_page.link
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

        if image:
            response += "<h2>Image:</h2>"
            response += f"<a href={image}>Link</a>"
            # link not working getting 403'd due to link string not being authenticated

        return response
    
    except ValueError as e:
        return str(e), ""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
