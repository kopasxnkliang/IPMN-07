from flask import Flask,jsonify,request,json
# from transformers import MvpTokenizer, MvpForConditionalGeneration
import run_tuned_model


app = Flask(__name__)

@app.route('/example', methods=['POST'])
def handle_json():
    data = request.json
    sid = data.get('ID')      
    relation = data.get('Relation') 
    relation = ' [SEP] '.join(relation)
    # generate sentence
    generated_sentence = run_tuned_model.get_sentence(relation, sid)
    return {
        "status": "200 OK",
        "ID": sid,
        "Text": generated_sentence
    }
   

if __name__ == "__main__":
    app.run()
