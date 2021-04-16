from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask.helpers import make_response
# lib for handling mail transfer protocol
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders, message
import os
import re
import json
from io import BytesIO
import base64
from PIL import Image
# Import tex_2_pdf class
from tex_2_pdf_converter import tex_2_pdf
# to be removed later 
import numpy as np
# import first section of main pipeline
from Pipeline_sec_a import form_or_nonform

app = Flask(__name__)

# The mail address and password
my_address = "nidbhavsar989@gmail.com"
my_pass = os.environ.get('Pass_key')

# texworks filename
tex_file_name = "temp_tex_file"
tex_file_name_2 = "temp_tex_file_2"
directory = "sake/"

# universal string to carry tex output from model.
tex_string = ''

# to be removed!
with open('train.formulas.norm.txt') as file:
    formulas = [line for line in file.read().split('\n')]

# creating object of predict class.
model_dir = 'form_vs_non_form'
yes_predict_model = form_or_nonform(model_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # remove dependent variables before starting execution.
    clean('temp.pdf', tex_file_name)

    req = request.get_json()
    # req = { image_base64: base64_dataURL, Name_: name, Email_: email }
    rec_bytes = bytes(req['image_base64'], 'utf-8')

    im = Image.open(BytesIO(base64.b64decode(rec_bytes)))
    # save image to directory. 
    save_loc = 'temp.png'
    Image.open(save_loc)
    im.save(save_loc, 'PNG')
    
    # placeholder for model (to be added later)
    
    # model pipeline 1) detect whether given image contains formula or not 2) predict Latex formula || date: 4/9/2021 time: 12:04 PM
    yes_predict_model.predict_class(save_loc)
    seek_pred = yes_predict_model.pred_class
    if seek_pred == 1:
        pass
    elif seek_pred == 0:
        res = make_response(jsonify({"message" : "JSON received", "tex" : 'None'}), 202)
        return res

    # output of model will be a tex format string
    # Since model is not working so randomly generate the tex output from  train.formulas.norm.txt
    rand_n = np.random.randint(1, len(formulas))
    tex_string = formulas[rand_n]
    with open('{}.txt'.format(tex_file_name), "w") as f:
        f.write(tex_string)

    # create tex_2_pdf object
    tex_to_pdf = tex_2_pdf(file_name=tex_file_name)
    name = tex_to_pdf.get_pdf_name()

    # send output response via mail.
    send_email(req, name)

    # send appropriate response.
    res = make_response(jsonify({"message" : "JSON received", "tex" : tex_string}), 200)
    return res

def send_email(req, pdf_file_name):
    # name and email address retrieved form json data.
    name = req['Name_'] 
    email = req['Email_']
    
    # Main mail format
    mail_content = "Hey {0}, here's your message!".format(name)

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = my_address
    message['To'] = email
    message['Subject'] = 'Demo message.'

    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = directory + pdf_file_name
    attach_file = open(attach_file_name, 'rb') # open the file in binary mode.
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment

    # add paayload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)

    # Create SMTP session for sending the mail
    server = smtplib.SMTP("smtp.gmail.com", 587) # google accepts mail through port-sno.: 587.
    server.starttls()
    server.login(my_address, my_pass) # using environment variable for safe transit.
    text = message.as_string()
    server.sendmail(my_address, email, text)
    server.quit()
    print("Mail Sent!")

def delete_file(filename):
    try :
        os.remove(filename)
    except Exception:
        pass

def clean(pdf_name, txt_name):
    delete_file(directory+pdf_name)
    delete_file(txt_name)

@app.route('/process', methods=['POST', 'GET'])
def open_image():
    
    if request.method == 'POST':
        print('using post block')
        req = request.get_json()
        # storing request json data 
        Latex_string = req['Latex_string']
        with open('{}.txt'.format(tex_file_name_2), "w") as f:
            f.write(Latex_string)

        # create tex_2_pdf object
        tex_to_pdf = tex_2_pdf(file_name=tex_file_name_2)
        name = tex_to_pdf.get_pdf_name()
        print(name)

        res = make_response(jsonify({"message" : "JSON received"}), 200)
        # return redirect(url_for('next_page'))
        return res
    else:
        print('using get block')
        return redirect(url_for('next_page'))

@app.route('/next_page')
def next_page():
    print("Lumos")
    return render_template('Image_show.html')

if __name__ == "__main__":
    app.run(debug = True)


    
