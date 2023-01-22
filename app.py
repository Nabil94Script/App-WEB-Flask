from flask import Flask
from API_REST import view


app = Flask(__name__)


app.register_blueprint(view,name="Page")
app.register_blueprint(view,name="Result")
app.register_blueprint(view,name="Predict")


#################################################################################

# configure this first

broker_adress='localhost'
my_port=9090
user=''
password=''

#run APP

if __name__ == '__main__':
   
   app.run(host=broker_adress,port=my_port, debug=True)

            



