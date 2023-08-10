from flask import Flask
from flask import request
import patent_client
from patent_client import Inpadoc
import urllib.request
from titlecase import titlecase

#need patent function to return all the info from the patent, css styling, and html fixed up###

#activate with venv\Scripts\activate and start app with python main.py###

app = Flask(__name__)



@app.route("/")
def index():
    patNumber = request.args.get("patNumber", "")
    if patNumber:
        patentSelect = patent(patNumber)
        # formPatNumber = patNumber
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

def patent(patNumber):
    try:
      pub = Inpadoc.objects.get(f"US{patNumber}")
      inventors = pub.biblio.inventors_original
      title = pub.biblio.title
      abstract = pub.biblio.abstract
      # Imagesimages = pub.
      formNum = "{:,}".format(int(patNumber))
  
      response = ""
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
 
        
      if formNum:
        response += "<h2>Patent Number:</h2>"
        response += f"<p>{formNum}</p>"
      else:
        response += "<p>Patent Number: Not Found</p>"

      # if images:
      #   response += "<h2>Images:</h2>"
      #   response += f"<p>{Images.get_images}</p>"
      #   # response += f"<p>{images.get(435)}</p>"
      #   # urllib.request.urlretrieve(
      #   #    'http://ops.epo.org/3.2/rest-services/published-data/images/{images.link}', "application.pdf")
      #   # img = Image.open("application.pdf")
      #   # response += img.show()
      # else:
      #   response += "<p>Images: Not Found</p>"
      
      return response
      
    
    except ValueError as e:
      return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
