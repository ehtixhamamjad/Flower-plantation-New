from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify,flash,session
from werkzeug.utils import secure_filename
import os
# from tensorflow.keras.models import load_model
# import numpy as np
from myFunctions.nurserysignupform import nurserysignupform
from myFunctions.usersignupform import usersignupform
from myFunctions.loginfun import addlogin
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# database

from myFunctions.userAddPlanFun import userAddPlanFun
from myFunctions.addFlowerfun import addFlowerfun
# from myFunctions.editplan import editplan
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

from flask_sqlalchemy import SQLAlchemy
# database
# alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/flowerplantation"
# app.config['SQLALCHEMY_MOUDIFICATIONS']
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
   

class Flower(db.Model):
    __tablename__ = 'flower'
    flower_id = db.Column(db.Integer, primary_key=True)  # Added Flower id
    flower_image_name = db.Column(db.String(225), unique=False, nullable=True)
    flower_name = db.Column(db.String(225), unique=False, nullable=True)
    flower_information = db.Column(db.String(225), unique=False, nullable=True)  # Changed to flower_information
    color = db.Column(db.String(225), unique=False, nullable=True)  # Added Color
    season = db.Column(db.String(225), unique=False, nullable=True)
    category = db.Column(db.String(225), unique=False, nullable=True)  # Added Category
    altitude = db.Column(db.Integer, nullable=True)  # Changed to Integer
    height = db.Column(db.Integer, nullable=True)  # Changed to Integer
    area = db.Column(db.String(225), unique=False, nullable=True)
    grow_time = db.Column(db.String(225), unique=False, nullable=True)  # Added Grow time
    pesticide = db.Column(db.String(225), unique=False, nullable=True)
    fertilizer = db.Column(db.String(225), unique=False, nullable=True)
    disease = db.Column(db.String(225), unique=False, nullable=True)
    fragrance = db.Column(db.String(225), unique=False, nullable=True)
    shape = db.Column(db.String(225), unique=False, nullable=True)
    sunlight = db.Column(db.String(225), unique=False, nullable=True)
    watering = db.Column(db.String(225), unique=False, nullable=True)

class Plan(db.Model):
    __tablename__ = 'flower_plan'
    plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    flower_name = db.Column(db.String(225), unique=False, nullable=True)
    season = db.Column(db.String(225), unique=False, nullable=True)
    flower_varieties = db.Column(db.String(225), unique=False, nullable=True)
    start_date = db.Column(db.Date, unique=False, nullable=True)
    end_date = db.Column(db.Date, unique=False, nullable=True)
    location = db.Column(db.String(225), unique=False, nullable=True)
    notes = db.Column(db.String(225), unique=False, nullable=True)
    budget_allocation = db.Column(db.Integer, unique=False, nullable=True)
    
# @app.route("/usealchemy")
# def usealchemy():
#     Firstname="ali"
#     Lastname='rahman'
#     new_user = TEST(name=Firstname, fname=Lastname)
#     db.session.add(new_user)
#     db.session.commit()
#     return "Succes"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flowerplantation'
mysql = MySQL(app)

# # Define predict_class function
# def predict_class(model, image_path):
#     # Load the image
#     img = load_img(image_path, target_size=(64, 64))
#     # Convert the image to a numpy array
#     img_array = img_to_array(img)
#     # Rescale the image
#     img_array = img_array / 255.0
#     # Expand dimensions to match the model's expected input shape
#     img_array = np.expand_dims(img_array, axis=0)
#     # Make a prediction
#     prediction = model.predict(img_array)
#     # Get the index of the highest probability
#     predicted_class_index = np.argmax(prediction)
#     return predicted_class_index

# # Load the model
# model_file_path = 'model.h5'
# model = load_model(model_file_path)

# # Define class_indices
# class_indices = {
#     0: 'Daisy',
#     1: 'Dandelion',
#     2: 'Rose',
#     3: 'SunFlower',
#     4: 'Tulip'
# }

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return redirect(request.url)
#         file = request.files['image']
#         if file.filename == '':
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             predicted_class_index = predict_class(model, os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # Check if predicted_class_index is in class_indices
#             if predicted_class_index in class_indices:
#                 class_name = class_indices[predicted_class_index]
#             else:
#                 # Handle the case where predicted_class_index is not found in class_indices
#                 class_name = "Unknown"
#             return render_template('result.html', class_name=class_name)
#     return redirect(url_for('home_page'))
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# all routes
# main
@app.route('/index')
def index():
    # Your index route logic here
    return render_template('index.html')

@app.route('/', methods=['GET'])
def getFlowerdataindex():
    # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_id, flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area, grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("/index.html", flowers=flower_data)

@app.route('/login' , methods=['POST', 'GET'])
def login():
    return addlogin()
    # email=request.form.get('email')
    # password=request.form.get('password')
    # cur = mysql.connection.cursor()
    # query = "SELECT email FROM user WHERE email = %s and WHERE password"
    # cur.execute(query, (email,))

    # # flower_data = cur.fetchall()
    # cur.close()
    # if(email):
    #  return render_template("/index.html") 
    # else:  
    #  return render_template("/login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return usersignupform()
    return render_template("signup.html")   

@app.route('/upload-img')
def uploadimage():
    return render_template("upload-img.html")    

@app.route('/flowerdetails/<int:id>', methods=['GET'])
def flowerdetail(id):
# @app.route('/user/flowersdetailsbyid/<int:id>', methods=['GET'])
    try:
        # Fetch flower details from the database based on the provided ID
        flower_data = Flower.query.filter_by(flower_id=id).first()
        if flower_data:
            # Pass the fetched data to the template
            return render_template("/flower-details.html", flower=flower_data)
        else:
            return "Flower not found."
    except ValueError:
        return "Invalid ID provided."
   
@app.route('/nursery/flowers',methods=['GET'])
def getFlowerdata():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT  flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("nursery/flowers.html", flowers=flower_data)

@app.route('/user/cityflower',methods=['GET'])
def getFlowerdataincityflower():
     # Fetch all flower plans from the database
    userid = session.get('id') 
    if userid is not None:
        cur = mysql.connection.cursor()
        cur.execute("SELECT area FROM user WHERE id = %s", (userid,))
        flower_area = cur.fetchone()[0]  # Fetch a single row and first column value

        cur.execute("SELECT flower_id, flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area, grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower WHERE area = %s", (flower_area,))

        flower_data = cur.fetchall()
        cur.close()
        
        # Pass the fetched data to the template
        return render_template("/user/cityflower.html", flowers=flower_data)
    else:
        # Handle case where 'id' is not found in session
        return "User ID not found in session"

@app.route('/user/flower',methods=['GET'])
def getFlowerdatainuserflower():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT  flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("user/flower.html", flowers=flower_data)
@app.route('/user',methods=['GET'])
def getFlowerdatainuserindex():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT  flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("index.html", flowers=flower_data)
# @app.route('/user/flowersdetailsbyid/<int:id>', methods=['GET'])
# def getFlowerdstails(id):
#     try:
#         # Fetch flower details from the database based on the provided ID
#         flower_data = Flower.query.filter_by(flower_id=id).first()
#         if flower_data:
#             # Pass the fetched data to the template
#             return render_template("user/flowersdetailsbyid.html", flower=flower_data)
#         else:
#             return "Flower not found."
#     except ValueError:
#         return "Invalid ID provided."

@app.route('/user/index',methods=['GET'])
def getFlowerdatainuser():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT  flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("user/index.html", flowers=flower_data)
@app.route('/nursery/flowers')
def flowers_nursery():
    return render_template("nursery/flowers.html")

@app.route('/editflower/<int:id>', methods=['GET', 'POST'])
def editflower(id):
    flower_data = Flower.query.filter_by(flower_id=id).first()
    # return redirect(url_for('editflower', id=flower_data.flower_id))
    return render_template("nursery/editflower.html", flowers=flower_data)
    # return render_template("user/editplan.html", flower_plans=plan_data)
  

@app.route('/nursery/flowers',methods=['GET'])
def flowersdata():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("nursery/flowers.html", flowers=flower_data)


@app.route('/updateflower/<int:id>', methods=['POST'])
def updateflower(id):
    flower_data = Flower.query.get_or_404(id)  # Retrieve the flower by its ID or return a 404 error if not found
    
    if request.method == 'POST':
        # Update the flower with the data from the form
        flower_data.flower_image_name = request.form.get('flower_image_name')
        flower_data.flower_name = request.form.get('flower_name')
        flower_data.flower_information = request.form.get('flower_information')
        flower_data.color = request.form.get('color')
        flower_data.season = request.form.get('season')
        flower_data.category = request.form.get('category')
        flower_data.altitude = request.form.get('altitude')
        flower_data.area = request.form.get('area')
        flower_data.grow_time = request.form.get('grow_time')
        flower_data.pesticide = request.form.get('pesticide')
        flower_data.fertilizer = request.form.get('fertilizer')
        flower_data.shape = request.form.get('shape')
        flower_data.sunlight = request.form.get('sunlight')
        flower_data.watering = request.form.get('watering')
        
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the flowers page or any other desired page
        return redirect(url_for('flowers'))
    
    # Render the edit flower form with the existing flower data
    return render_template("nursery/editflower.html", flower=flower_data)

@app.route('/deleteflower/<int:id>', methods=['GET', 'POST','DELETE'])
def deleteflower(id):
    delflower = Flower.query.filter_by(flower_id=id).first()
    db.session.delete(delflower)
    db.session.commit()
    return render_template("nursery/flowers.html")

@app.route('/nursery',methods=['GET'])
def getFlowerdatainurseryindex():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT  flower_id ,flower_image_name, flower_name, flower_information, color, season, category, altitude, height, area,  grow_time, pesticide, fertilizer, disease, fragrance, shape, sunlight, watering FROM flower")
    flower_data = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("/nursery/index.html", flowers=flower_data)


# user///////////////////////////
@app.route('/user')
def user():
    return render_template("user/index.html")

@app.route('/user/flower')
def userflower():
    return render_template("user/flower.html")
@app.route('/user/cityflower')
def cityflower():
    return render_template("user/cityflower.html")

@app.route('/user/user-flower-plan',methods=['GET'])
def userplan():
     # Fetch all flower plans from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT plan_id, flower_name, season, flower_varieties,  start_date, end_date,location,notes, budget_allocation  FROM flower_plan")
    flower_plan = cur.fetchall()
    cur.close()
    # Pass the fetched data to the template
    return render_template("user/plan.html", flower_plans=flower_plan)

@app.route('/user/add-plan', methods=['GET', 'POST'])
def addflowerplan():
    return userAddPlanFun()
    

@app.route('/nursery/add-flower', methods=['GET', 'POST'])
def addflowerdata():
    return addFlowerfun()

# @app.route('/editplan/<int:id>', methods=['GET', 'POST'])
# def editplan(id):
#     plan=Plan.query.filter_by(plan_id=id).first()
#     # name=Plan.query.filter_by(plan_id=id).first
#     return render_template("user/editplan.html",flower_plans=plan)

@app.route('/editplan/<int:id>', methods=['GET', 'POST'])
def editflowerplan(id):
    plan_data = Plan.query.filter_by(plan_id=id).first()
    return render_template("user/editplan.html", flower_plans=plan_data)

@app.route('/deleteplan/<int:id>', methods=['GET', 'POST','DELETE'])
def deleteflowerplan(id):
    delplan = Plan.query.filter_by(plan_id=id).first()
    db.session.delete(delplan)
    db.session.commit()
    return render_template("user/plan.html")
   
@app.route('/user/favourite')
def userfavourite():
    return render_template("user/favourite.html")


@app.route('/user/notification')
def usernotification():
    return render_template("user/notification.html")

# nursery////////////////////////////
@app.route('/nursery')
def nursery():
    return render_template("nursery/index.html")

@app.route('/nursery/signup', methods=['GET', 'POST'])
def nurserysignup():
    if request.method == 'POST':
        return nurserysignupform()
    return render_template("nursery/signup.html")

@app.route('/nursery/login')
def nurserylogin():
    return render_template("nursery/login.html")

@app.route('/nursery/add-flower')
def addflower():
    return render_template("nursery/add-flower.html")

@app.route('/nursery/flowers')
def flowers():
    return render_template("nursery/flowers.html")

@app.route('/nursery/location')
def location():
    return render_template("nursery/location.html")

@app.route('/nursery/add-location')
def addlocation():
    return render_template("nursery/add-location.html")    

# admin ///////////////////////////////////
@app.route('/admin')
def admin():
    return render_template("admin/index.html")

@app.route('/admin/signup')
def adminsignup():
    return render_template("admin/signup.html")

@app.route('/admin/login')
def adminlogin():
    return render_template("admin/login.html")    

@app.route('/admin/user' ,methods=['GET'])
def adminuserinfo():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, phone, city, email FROM user")
        all_user = cur.fetchall()
        cur.close()
        return render_template("admin/user.html", all_users=all_user)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return render_template("admin/user.html", all_users=[])
app.secret_key = 'your_secret_key_here'

@app.route('/admin/nursery',methods=['GET'])
def adminnurseryinfo():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, address, city, zip, Country, phone, email FROM nursery_owner")
        all_nursery = cur.fetchall()
        cur.close()
        return render_template("admin/nursery.html", all_nurserys=all_nursery)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return render_template("admin/nursery.html", all_nurserys=[])
    # return render_template("admin/nursery.html")  

@app.route('/updateplan/<int:id>', methods=['POST'])
def updateplan(id):
    plan_data = Plan.query.get_or_404(id)  # Retrieve the plan by its ID or return a 404 error if not found
    
    if request.method == 'POST':
        # Update the plan with the data from the form
        plan_data.flower_name = request.form['flowerName']
        plan_data.season = request.form['season']
        plan_data.flower_varieties = request.form['flowerVarieties']
        plan_data.start_date = request.form['startDate']
        plan_data.end_date = request.form['endDate']
        plan_data.location = request.form['location']
        plan_data.notes = request.form['notes']
        plan_data.budget_allocation = request.form['budgetAllocation']
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the plan detail page or any other desired page
        return redirect(url_for('userplan'))
    
    # Render the edit plan form with the existing plan data
    return render_template("user/editplan.html", flower_plans=plan_data)


app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)