from flask import Flask, request 
from langchain import OpenAI
import os
import configparser
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain 
import ai
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}




@app.route('/question', methods=['POST'])
@cross_origin()
def answer():
    if app.config.get('answer') is None:
        app.config['answer'] = ai.AI("modules/anthro.pdf")
        # get the question from json
    data = request.get_json()
    question = data['question']

    # return the answer
    return app.config['answer'].answer(question)



@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    # if the uploaded file is pdf
    if request.files['file'].filename.endswith('.pdf'):
        # save the file
        file = request.files['file']
        file.save('file.pdf')
        app.config['answer'] = ai.AI("file.pdf")
        return {"message": "File uploaded successfully"}
    elif request.files['file'].filename.endswith('.docx'):
        # save the file
        file = request.files['file']
        file.save('file.docx')
        app.config['answer'] = ai.AI("file.docx", "docx")
        return {"message": "File uploaded successfully"}
    elif request.files['file'].filename.endswith('.pptx'):
        # save the file
        file = request.files['file']
        file.save('file.pptx')
        app.config['answer'] = ai.AI("file.pptx", "pptx")
        return {"message": "File uploaded successfully"}
    else:
        return {"message": "Invalid file type"}


# @app.route('/answer', methods=['POST', 'GET'])
# def answer():
#     if request == 'GET':
#         question = request.args.get('question')
#         if index == None:
#             return '<h1> No context to answer from!</h1>'
#         return index.query(question)
#     else:
#         file = request.files['file']
#         question = request.form['question']
#         file.save('file.pdf')
#         loader = PyPDFLoader('file.pdf')
#         index = VectorstoreIndexCreator().from_loaders([loader])
#         return {'question': question, 'answer': index.query(question)}
    


# @app.route('/yt', methods=['POST'])
# def yt():
#     try:
#         link = request.form['url']
#         question = request.form['question']
#         loader = YoutubeLoader.from_youtube_channel(link, add_video_info=True)
#         loader.load()
#         index = VectorstoreIndexCreator().from_loaders([loader])
#         return index.query(question)  
#     except Exception as e:
#         return f'<h1> Error: {e} </h1>'      
    
    


if __name__ == '__main__':
    app.run(debug=True)
