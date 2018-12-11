from flask import Flask, render_template, request, url_for, redirect, session, flash
from sqlalchemy import or_, and_
from flaskshop import app
from flaskshop.forms import RegistrationForm, LoginForm, FavouriteForm, FavClickForm
from flask_login import login_user, current_user, logout_user, login_required
from flaskshop import bcrypt, db
from flaskshop.models import Clothing, User, Favourites_board, Favourites_relationship

############# get categories ############

products= Clothing.query.all()
brands = []
for product in products:
    if product.brand in brands:
        pass;
    else:
        brands.append(product.brand)
categories = []
for p in products:
    if p.clothing_category in categories:
        pass;
    else:
        categories.append(p.clothing_category)

################# search function ##########################
def search_bar():
    search_items=[]
    for i in products:
        temp_list=[]
        search = str(request.form['search']).lower()
        name = str(i.name).lower()
        name = name.split("-")
        colour = (i.colour).lower()
        brand = (i.brand).lower()
        search = search.split(" ")

        for s in search:
            if s in name:
                temp_list.append(s)
            elif s == colour:
                temp_list.append(s)
            elif s == brand:
                temp_list.append(s)
            else:
                pass;
        if len(temp_list) >= 1:
            search_items.append(i)
    if len(search_items) == 0:
        flash('Sorry, we could not find anything matching your search! :( Check out some of our new stuff below!'.format(), 'danger')
        return redirect(url_for('index'))

    return render_template('home.html', items = search_items, brands = brands, categories = categories)


def check_auth(email, password):
    if(email == valid_email and valid_pwhash == bcrypt.hashpw(password.encode('utf-8'), valid_pwhash)):
        return True
    return False

def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.login'))
        return decorated


#################### app routes #############################

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return search_bar()
    return render_template('home.html', items=products, brands = brands, categories = categories)

############## product display page ##############

@app.route('/<brand>/<name>', methods=['GET', 'POST'])
def product_details(brand=None, name=None):
    boards=[]
    if not current_user.is_authenticated:
        flash('Login or Register to add to favourites!','danger')
    else:
        boards = Favourites_board.query.filter_by(creator = current_user)
        if not boards:
            flash('Create a board in favourites to add a favourite!','info')
        else:
            if request.method =="POST":
                f_b_titles = request.form.getlist("board_titles")
                titles = request.form.get("board_titles")
                search_bar_submit = request.form.get("search_button")
                if search_bar_submit:### return search bar if search
                    return search_bar()
                if not titles or not f_b_titles and not search_bar_submit:### error handling for favourites button
                    flash('Select board to add to, or create a board in favourites!', 'danger')
                    return search_bar()
                elif titles:
                    clothing = Clothing.query.filter_by(name = name).first()
                    userid = int(current_user.id)
                    clothingid = int(clothing.id)
                    for b in boards:
                        for board in f_b_titles:
                            if b.title == board:
                                fav_relationship = Favourites_relationship(user_id = userid, clothing_id = clothingid, favs_board = b)
                                db.session.add(fav_relationship)
                                db.session.commit()
                                flash('Added favourite to mood board!', 'success')

    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories, boards = boards)

############## sort by female ################

@app.route('/female', methods=['GET', 'POST'])
def female():
    if request.method=='POST':
        return search_bar()
    females_products = Clothing.query.filter(or_(Clothing.gender=='Female', Clothing.gender=='Mixed'))
    return render_template('home.html', items = females_products, brands = brands, categories = categories)

############# sort by male ###############

@app.route('/male', methods=['GET', 'POST'])
def male():
    if request.method=='POST':
        return search_bar()
    males_products = Clothing.query.filter(or_(Clothing.gender=='Male', Clothing.gender=='Mixed'))
    return render_template('home.html', items = males_products, brands = brands, categories = categories)

############# sort by mixed ###############

@app.route('/mixed', methods=['GET', 'POST'])
def mixed():
    if request.method=='POST':
        return search_bar()
    mixed_products = Clothing.query.filter_by(gender='Mixed')
    return render_template('home.html', items = mixed_products, brands = brands, categories = categories)

############### sort by brand #################

@app.route('/<brand>', methods=['GET', 'POST'])
def brand(brand=None):
    if request.method=='POST':
        return search_bar()
    branded_products = Clothing.query.filter_by(brand=brand)
    return render_template('home.html', items = branded_products, brands = brands, categories = categories)

############### sort by categorised products ################

@app.route('/Bottoms', methods=['GET', 'POST'])
def bottoms():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(clothing_category='Bottoms')
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/Tops', methods=['GET', 'POST'])
def category():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(clothing_category='Tops')
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/Accessories', methods=['GET', 'POST'])
def accessories():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(clothing_category='Accessories')
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/Shoes', methods=['GET', 'POST'])
def shoes():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(clothing_category='Shoes')
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/Outerwear', methods=['GET', 'POST'])
def outerwear():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(clothing_category='Outerwear')
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)


############### sort by sub category ##############

@app.route('/Bottoms/<sub_category>', methods=['GET', 'POST'])
def bottoms_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(sub_category=sub_category)
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/Bottoms/<brand>/<name>', methods=['GET', 'POST'])
def bottoms_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/Tops/<sub_category>', methods=['GET', 'POST'])
def tops_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(sub_category=sub_category)
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/Tops/<brand>/<name>', methods=['GET', 'POST'])
def tops_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/Accessories/<sub_category>', methods=['GET', 'POST'])
def accessories_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(sub_category=sub_category)
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/Accessories/<brand>/<name>', methods=['GET', 'POST'])
def acc_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/Shoes/<sub_category>', methods=['GET', 'POST'])
def shoes_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(sub_category=sub_category)
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/Shoes/<brand>/<name>', methods=['GET', 'POST'])
def shoes_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/Outerwear/<sub_category>', methods=['GET', 'POST'])
def outerwear_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter_by(sub_category=sub_category)
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/Outerwear/<brand>/<name>', methods=['GET', 'POST'])
def outerwear_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, categories = categories)

########## sort by gender AND category ############

@app.route('/female/Bottoms', methods=['GET', 'POST'])
def w_bottoms():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Bottoms', Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/female/Tops', methods=['GET', 'POST'])
def w_tops():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Tops', Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/female/Accessories', methods=['GET', 'POST'])
def w_accessories():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Accessories', Clothing.gender=='Mixed'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/female/Shoes', methods=['GET', 'POST'])
def w_shoes():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Shoes', Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/female/Outerwear', methods=['GET', 'POST'])
def w_outerwear():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Outerwear', Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)


############### sort by sub category ##############

@app.route('/female/Bottoms/<sub_category>', methods=['GET', 'POST'])
def w_bottoms_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/female/Bottoms/<brand>/<name>', methods=['GET', 'POST'])
def w_bottoms_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/female/Tops/<sub_category>', methods=['GET', 'POST'])
def w_tops_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/female/Tops/<brand>/<name>', methods=['GET', 'POST'])
def w_top_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/female/Accessories/<sub_category>', methods=['GET', 'POST'])
def w_accessories_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Mixed'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/female/Accessories/<brand>/<name>', methods=['GET', 'POST'])
def w_acc_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/female/Shoes/<sub_category>', methods=['GET', 'POST'])
def w_shoes_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/female/Shoes/<brand>/<name>', methods=['GET', 'POST'])
def w_shoe_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/female/Outerwear/<sub_category>', methods=['GET', 'POST'])
def w_outerwear_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Female'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/female/Outerwear/<brand>/<name>', methods=['GET', 'POST'])
def w_out_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

#################### males categories ###############


@app.route('/male/Bottoms', methods=['GET', 'POST'])
def m_bottoms():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Bottoms', Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/male/Tops', methods=['GET', 'POST'])
def m_category():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Tops', Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/male/Accessories', methods=['GET', 'POST'])
def m_accessories():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Accessories', Clothing.gender=='Mixed'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/male/Shoes', methods=['GET', 'POST'])
def m_shoes():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Shoes', Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)

@app.route('/male/Outerwear', methods=['GET', 'POST'])
def m_outerwear():
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.clothing_category=='Outerwear', Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)


############### sort by sub category ##############

@app.route('/male/Bottoms/<sub_category>', methods=['GET', 'POST'])
def m_bottoms_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products)
@app.route('/male/Bottoms/<brand>/<name>', methods=['GET', 'POST'])
def m_bottoms_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/male/Tops/<sub_category>', methods=['GET', 'POST'])
def m_tops_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/male/Tops/<brand>/<name>', methods=['GET', 'POST'])
def m_top_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/male/Accessories/<sub_category>', methods=['GET', 'POST'])
def m_accessories_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Mixed'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/male/Accessories/<brand>/<name>', methods=['GET', 'POST'])
def m_acc_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/male/Shoes/<sub_category>', methods=['GET', 'POST'])
def m_shoes_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/male/Shoes/<brand>/<name>', methods=['GET', 'POST'])
def m_shoe_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

@app.route('/male/Outerwear/<sub_category>', methods=['GET', 'POST'])
def m_outerwear_sub(sub_category=None):
    if request.method=='POST':
        return search_bar()
    categorised_products = Clothing.query.filter(and_(Clothing.sub_category==sub_category, Clothing.gender=='Male'))
    return render_template('home.html', items = categorised_products, brands = brands, categories = categories)
@app.route('/male/Outerwear/<brand>/<name>', methods=['GET', 'POST'])
def m_out_product_details(brand=None, name=None):
    if request.method=='POST':
        return search_bar()
    return render_template('item_display.html', products = products, name=name, brands = brands, categories = categories)

################################## login ########################################


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created, you can now login!'.format(), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, products = products, brands = brands, categories = categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_param = request.args.get('next')
            return redirect(next_param) if next_param else redirect(url_for('index'))
            flash('Login Success!', 'success')
        else:
            flash('Login Unsuccessful. Please check email and password or register for an account.', 'danger')
    return render_template('login.html', title='Login', form=form, products = products, brands = brands, categories = categories)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

############### routes for logged in #############

@app.route('/favourites', methods=['GET', 'POST'])
@login_required
def favourites():
    form = FavouriteForm()
    if form.validate_on_submit():
        board = Favourites_board(title = form.title.data, creator=current_user)
        db.session.add(board)
        db.session.commit()
        flash('Mood Board has been created!', 'success')
        return redirect(url_for('favourites'))
    boards = Favourites_board.query.filter_by(user_id = current_user.id)
    return render_template('favourites.html', title='Account', form=form, boards=boards)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    flash('Oops! Page still under construction', 'danger')
    return render_template('cart.html', title='Cart', form=form, products = products, brands = brands, categories = categories)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    flash('Oops! Page still under construction', 'danger')
    return render_template('checkout.html', title='Cart', form=form, products = products, brands = brands, categories = categories)

@app.route('/favourites/<board>', methods=['GET', 'POST'])
@login_required
def favourites_sub(board=None):
    if request.method=='POST':
        return search_bar()
    board_rel = Favourites_relationship.query.all()
    clothes_int=[]
    clothes_list=[]
    boards = Favourites_board.query.filter_by(creator = current_user)
    for b in boards:
        for rel in board_rel:
            if b.title == rel.board_title and rel.board_title == board:
                clothes_int.append(rel.clothing_id)
        for i in clothes_int:
                for p in products:
                    if i == p.id:
                        print(p.id)
                        print(i)
                        clothes_list.append(p)
    return render_template('fav_boards.html', products = clothes_list, clothing = clothes_list, brands = brands, categories = categories)

## basic error handling
@app.errorhandler(404)
def page_not_found(e):
    flash('Oops! This page does not exist, check spelling and try again', 'danger')
    return render_template('home.html', items=products, brands = brands, categories = categories), 404
