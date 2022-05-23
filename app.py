import os
import re
from flask import Flask ,flash, render_template , request, redirect, url_for , send_file
import cv2
#from matplotlib.pyplot import text
import numpy as np
from werkzeug.utils import secure_filename
import uuid
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play  
import json
from pydub import AudioSegment
from pydub.silence import split_on_silence

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags



# random_string = uuid.uuid4().hex
random_string = uuid.uuid4().hex
UPLOAD_FOLDER = 'static/input'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','jfif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def main_page():
    return render_template('index.html')


ALLOWED_SOUND_EXTENSIONS = set(['wav'])
def allowed_sound_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_SOUND_EXTENSIONS

UPLOAD_FOLDER_M = 'static/music_input'

@app.route('/audio', methods=['GET' ,'POST'])
def upload_form_sound():
    if request.method == 'GET':
        return render_template('music.html')
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No clip selected for uploading')
            return redirect(request.url)
        if file and allowed_sound_file(file.filename):
            filename = secure_filename(file.filename)
            #file.export('static/music_input/aa1.wav', format="wav")
            save_path = os.path.join('static/music_input/', str(random_string)+'.wav')
            file.save(save_path)
            
            #print('upload_image filename: ' + filename)
            flash('Clip successfully uploaded and displayed below')
            # predict_audio()
            return redirect('/audio_download')
        else:
            
            flash('Allowed image types are -> wav mp3')
            return redirect('/audio')


@app.route('/audio_download')
def predict_audio():
    save_path = os.path.join('static/music_input/', str(random_string)+'.wav')
    sound_file = AudioSegment.from_file(save_path,format = 'wav')
    #sound_file = AudioSegment.from_mp3('D:/AI/project/app/static/test_audio(1).mp3')
    sound_out = split_on_silence(sound_file, min_silence_len=500, silence_thresh=-40 )
    out_path = 'static/music_out/'+str(random_string)+'.wav'
    #print(lst)
    #for i, audio_chunk in enumerate(lst):
    for i, out in enumerate (sound_out):
        out.export('static/music_out/out{i}.wav', format="wav")
    output = sum(sound_out)
    output.export(out_path, format="wav")  
    

    # songs = os.listdir('static/music_out')  
    return send_file(out_path, as_attachment=True)




@app.route('/image', methods=['GET','POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('image.html')
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #cv2.imwrite('static/input'+filename+'.jpg', file)
            
            file.save(os.path.join('static/input', str(random_string)+'.jpg'))
            
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
        
            return redirect('/predict_image')
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect('/predict_image')


@app.route("/predict_image", methods = ['GET','POST'])
def predict_image():
    if request.method == "POST":
        return "wAweee"
    prototxt_path = 'static/text_model_data/deploy.prototxt'
    caffemodel_path = 'static/text_model_data/weights.caffemodel'
    # Read the model
    model = cv2.dnn.readNetFromCaffe(prototxt_path,caffemodel_path)
    

    #image_path = 'static/new.png'
    #image = cv2.imread(image_path)
    # if request.method == 'GET':
    #     return render_template('index.html', href = 'static/new.jpg')
    # else:
    image = cv2.imread('static/input/'+str(random_string)+'.jpg')
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    model.setInput(blob)
    detections = model.forward()

    for i in range(0, detections.shape[2]):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        confidence = detections[0, 0, i, 2]

        # If confidence > 0.5, show box around face
        if (confidence > 0.5):
            cv2.rectangle(image, (startX, startY), (endX, endY), (255, 255, 255), 2)
            
    cv2.imwrite('static/output/'+str(random_string)+'.jpg', image)
    # predict(model,'static/input/'+str(random_string)+'.jpg',str(random_string))
    return render_template('image.html', href = 'static/output/'+str(random_string)+'.jpg')





@app.route('/text', methods=['GET','POST'])
def upload_text():
    if request.method == 'GET':
        return render_template('text.html')
    else:  
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No clip selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/text_in/', str(random_string)+'.txt'))
            
            #print('upload_image filename: ' + filename)
            flash('Clip successfully uploaded and displayed below')
        
            return redirect('/predict_text')
        else:
            flash('Allowed image types are -> wav mp3')
            return redirect('/predict_text')

@app.route("/predict_text", methods = ['GET','POST'])
def predict_text():
    text_file = open("static/text_in/"+ str(random_string)+".txt", "r")
    data = text_file.read().replace("\n", " ")
    text_file.close()
    # doc = nlp(data)
    # NER = ([(X.text, X.label_) for X in doc.ents])

    sent = nltk.word_tokenize(data)
    p_tag = nltk.pos_tag(sent)

    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    cp = nltk.RegexpParser(pattern)

    cs = cp.parse(p_tag)
    NER = tree2conlltags(cs)
    return render_template ('text.html',NER = NER)



if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')



