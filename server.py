from flask import Flask, jsonify, request,redirect,url_for
from pymongo import MongoClient
app = Flask(__name__)
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager,set_access_cookies,unset_jwt_cookies
from datetime import timedelta
import os


mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
folder = client["DataBase"]
db=folder["Datas"]
pdb=folder["P_Datas"]


app.config['UPLOAD_FOLDER'] = 'Products_Uploads'




# JWT AUthentication

app.secret_key = 'jaypateltopsecret789654123'
app.config["JWT_SECRET_KEY"] = "jaypateltopsecret789654123" 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60) 
jwt = JWTManager(app)

# expire token 
@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({'Page': 'Login Page','Message':"Token is Expired.. Try to Login Again!",'Status':200})


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return jsonify({'Page': 'Login Page','Message':"You Are not Authorized NOw... Login Again !!",'Status':200})












@app.route('/',methods=['GET'])
def HomeAPI():
    return jsonify({'Page': 'Home Page','Message':"Test Page",'Status':200})



@app.route('/Registration',methods=['POST','GET'])
def Registration():
    if request.method == "POST":
        data= request.json
        name = data.get("Name")
        user = data.get("User")
        email= data.get("Email")
        password1 = data.get("Password1")
        password2 = data.get("Password2")


        if db.find_one({"User":user}) == None and db.find_one({"Email":email}) == None:
            if password1==password2:
                userinfo = {
                    "Name" :name,
                    "User" :user,
                    "Email" :email,
                    "Password"  : password1 
                }
                db.insert_one(userinfo)  
                print("____________________________")   
                Message = "Registration Sucessfull"
                Code = 200
            else:
                Message = "Password Not Metch"
                Code = 200
        else:
            Message="User Alredy Exist"
            Code =200
        
    else:
        Message = "'Data Not Post !"
        Code = 404
    return jsonify({'Page': 'Registration Page','Message':Message,'Status':Code})




@app.route('/Login',methods=['POST'])
def Login():
    if request.method == "POST":
        data= request.json
        user = data.get("User")
        password = data.get("Password")
        userdata = db.find_one({"User":user})
        if userdata['Password'] == password:
            Message = "Login Sucessfully"
            Code = 200 
            access_token = create_access_token(identity=(
                {"Name" :userdata['Name'],
                "User" :userdata['User'],
                "Email" :userdata['Email']}
            )) 
            res = jsonify({'Page': 'Login Page','Response':'User Login Now','Token':access_token,'Status':200}) 
            print("Login Done") 
            set_access_cookies(res, access_token) 
            return res  
        else:
            Message = "User and Password not Match !!"
            Code = 200
    else:
        Message = "Something Wrong !!!"
        Code = 404

    return jsonify({'Page': 'Login Page','Response':Message,'Status':Code})

@app.route('/Logout',methods=['GET'])
@jwt_required()
def Logout():
    res = jsonify({'Page': 'Logout Page','Response':'User Logout Now','Status':200})
    unset_jwt_cookies(res)
    print("Logout Done")
    return res



@app.route('/Private',methods=['GET'])
@jwt_required()
def Private():
    data =get_jwt_identity()
    print(data)
    return jsonify({'Page': 'Private Page','Message':"Private Page",'Status':200})



if __name__ == '__main__':
    app.run(debug=True)
