from flask import Flask,render_template,request,redirect,url_for,jsonify
import fake_review_detection
import product_recommendation
import connect_database
import data
import uuid
import time
import hashlib
import pyautogui

unique_id = uuid.uuid4()

numeric_id = int(str(unique_id)[:8], 16)

def generate_numeric_id(data, range_limit=100):
    data_with_timestamp = f"{data}{time.time()}"
    
    hash_object = hashlib.md5(data_with_timestamp.encode())
    
    hex_digest = hash_object.hexdigest()
    numeric_id = int(hex_digest, 16)
    
    result_id = numeric_id % range_limit
    
    return result_id


app = Flask(__name__)

product_details = data.product_details

@app.route('/home')
def index():
    return render_template('index.html',user = user.upper())

@app.route('/')
def start():
    return render_template('login-register.html')

@app.route('/login', methods = ['GET' , 'POST'])
def login():
    global user,email
    error_message = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        user = connect_database.get_name(email)
        result = connect_database.login(email=email , password=password)
        if result:
            return render_template("index.html",user = user.upper())
        else:
            error_message = "Password Incorrect!"
            return render_template("login-register.html")

    return render_template('login-register.html',error = error_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global email
    error_message = None

    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['cpassword'].strip()
        unique_id = generate_numeric_id(numeric_id, range_limit=26)

        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
        else:
            print(f"Register - First Name: {first_name}, Last Name: {last_name}, Email: {email},Password: {password} , id = {unique_id}")
            connect_database.register_account(ids = unique_id, fname= first_name , lname= last_name , email= email ,password=password)
            return redirect(url_for('register'))

    return render_template('login-register.html', error=error_message)

@app.route('/get_image_value/<product_id>')
def get_image_value(product_id):
    values = {'product_id': product_id}
    if values:
        print("email for product id recommendation : ",connect_database.get_id_by_email(email))
    return jsonify(values)

click_count = 0
recommendation_position = 0  # Initialize the position in the recommendation list
next_recommendations =''
@app.route('/get_product_details/<product_id>')
def get_product_details(product_id):
    global click_count, recommendation_position, next_recommendations

    click_count += 1  # Increase the click count every time the function is called
    print(click_count)
    product = next((p for p in product_details if p['reference'] == product_id), None)

    if product:
        ids = connect_database.get_id_by_email(email)
        print("email for product recommendation: ", ids)
        predictions = product_recommendation.predict_for_user(ids)
        r = []
        products = data.products
        for i in list(predictions.ProductID):
            r.append(product_recommendation.find_product_by_id(target_id=i, products=products, ids=data.ids))

        next_recommendations = r[recommendation_position:recommendation_position + 5]
        recommendation_position += 5  

        if recommendation_position >= len(r):
            recommendation_position = 0
        print(next_recommendations)
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'})


@app.route('/aboutus')
def aboutus():
    return render_template('about-us.html',user = user.upper())
    
@app.route('/contact')
def contact():
    return render_template('contact.html',user = user.upper())

@app.route('/shop')
def shop():
    return render_template('shop-3-column.html',user = user.upper())

@app.route('/cart')
def cart():
    return render_template('shopping-cart.html',user = user.upper())

@app.route('/product',methods = ['GET','POST'])
def product():
    if request.method == 'POST':
        review = request.form['review']
        rating = request.form['rating']
        print(f"Received review: {review}, rating: {rating}")
        result = fake_review_detection.predict(user_review=review, user_score=int(rating))
        # pyautogui.hotkey('ctrl','r')
        return render_template('single-product.html', result=result,user = user.upper(),next_recommendations=next_recommendations)
    # print("email for product recommendation : ",connect_database.get_id_by_email(email))
    return render_template('single-product.html',product_details = product_details,user = user.upper(),next_recommendations=next_recommendations)

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html',user = user.upper())


@app.route('/review',methods = ['GET','POST'])
def review():
    if request.method == 'POST':
        ratings = int(request.form['rating'])
        review = request.form['comment']
        name = request.form['author'].upper()
        email = request.form['email']
        print(ratings,review,name,email)
        star = '<li><i class="fa fa-star-o"></i></li>'
        no_star = '<li class="no-star"><i class="fa fa-star-o"></i></li>'
        remaining = 5 - int(ratings)
        total = ratings*star + remaining*no_star
        print(total)
    
    return render_template('single-product.html',new_name=name,new_rating = (total), new_review = review,ratings = ratings,user = user.upper(),next_recommendations=next_recommendations)



if __name__ == '__main__':
    app.run(debug=True)