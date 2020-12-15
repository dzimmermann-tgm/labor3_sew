import langdetect                    
from iso639 import languages                
from flask import Flask, request, jsonify  

app = Flask(__name__)

@app.route("/lg", methods=['GET'])
def detect():
    text = request.args.get("text")
    result = langdetect.detect_langs(text)        
    best = result[0]                   
    prob = round(best.prob, 2) * 100              
    iso_lang = best.lang               
    is_reliable = best.prob > 0.5       
    lang = languages.get(part1=iso_lang)
    
    response = {
        "reliable": is_reliable,
        "language": lang.name,
        "short": iso_lang,
        "prob": prob,
    }

    return jsonify(response)

@app.route("/", methods=['GET'])
def hello_user():
    return "Hello there"

if __name__ == "__main__":
    app.run()
