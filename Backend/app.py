"""
This script handles POST request, generates sentence using data from frontend, and returns the 
generated sentence we want to display in the user's browser.

This script requires that `flask` be installed within the Python
environment you are running this script in.
"""

from flask import Flask,jsonify,request,json
# from transformers import MvpTokenizer, MvpForConditionalGeneration
import run_tuned_model


app = Flask(__name__)
mvp = run_tuned_model.MVP()

@app.route('/example', methods=['POST'])
def handle_json():
    data = request.json
    sid = data.get('ID')      
    relation = data.get('Relation') 
    # relation = ' [SEP] '.join(relation)
    # generate sentence
    generated_sentence = mvp.generate(relation)
    return {
        "status": "200 OK",
        "ID": sid,
        "Text": generated_sentence
    }
   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
