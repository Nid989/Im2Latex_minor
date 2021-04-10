# import os 
# import pprint

# # password = os.environ.get('PASSWORD')

# env_var = os.environ.get('Pass_key')

# # pprint.pprint(dict(env_var), width=1)
# print(env_var)

# # def send_mail(req):
# #     # name and email address retrieved form json data.
# #     name = req['Name_'] 
# #     email = req['Email_']
# #     # message to be sent!
# #     message = "Hey {0} here's your message!".format(name)
# #     server = smtplib.SMTP("smtp.gmail.com", 587) # google accepts mail through port-sno.: 587.
# #     server.starttls()
# #     server.login(my_address, my_pass) # using environment variable for safe transit.
# #     server.sendmail(my_address, email, message)

from tex_2_pdf_converter import tex_2_pdf

file = "temp_tex_file"

obj = tex_2_pdf(file_name=file)

# import numpy as np
# from numpy import random

# with open('train.formulas.norm.txt') as file:
#     formulas = [line for line in file.read().split('\n')]

# rand_n = np.random.randint(0, len(formulas))
# t = formulas[rand_n]
# print(t)

# with open('abc.txt', 'w') as f:
#     f.write(t)


