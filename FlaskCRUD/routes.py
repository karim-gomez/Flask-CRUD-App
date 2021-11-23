#myenv\Scripts\activate
from flask import render_template, redirect,url_for, flash, abort,request
from flask_wtf import form
from FlaskCRUD.forms import AddUserForm,RegistrationForm,LoginForm,ProductForm
from FlaskCRUD.models import User,Product
from flask_login import login_required,current_user,login_user,logout_user
from FlaskCRUD import app, db



@app.route('/')
def home():
    #return 'Hello, user'
    return render_template("home.html")


# admin_dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    check_admin()
    return render_template("admin_dashboard.html")



# user_dashboard route
@app.route('/user_dashboard')
def user_dashboard():
    return render_template("user_dashboard.html")


# getting users route
@app.route('/users')
@login_required
def get_users():
    check_admin()
    users = User.query.all()
    user=User.query.filter_by(id=current_user.id).first_or_404()
    # user.product is the relationship bet two tbls
    products = Product.query.filter_by(owned_user=user)
    form=AddUserForm()
    return render_template('users.html', users=users,products=products,
                          form=form)

def check_admin():
    if not current_user.is_admin:
        abort(403)


# handling the gets
@app.route('/users')
@login_required
def new_user():
    return render_template('users.html')

# handling the posts
@app.route('/users', methods=['POST'])
@login_required
def new_user_acount():
    check_admin()
    form =AddUserForm()
    if form.validate_on_submit():
        employee = User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data,is_admin=True)

        db.session.add(employee)
        db.session.commit()
        flash('User has been registered successfully!','success')
        return redirect(url_for('get_users'))

    return render_template('users.html', form=form)


#edit route
@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    check_admin()
    
    user = User.query.get_or_404(id)
    form = AddUserForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        db.session.commit()
        flash('The user has been successfully updated.','info')
        return redirect(url_for('get_users'))

        
    elif request.method == 'GET':
        form.email.data = user.email
        form.username.data = user.username
    return render_template('users.html', 
                            form=form,
                           user=user)

# del route
@app.route('/users/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_user(id):
    check_admin()
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('The user has been successfully deleted .','info')
    return redirect(url_for('get_users'))



######################################################################## products

#getting products route
@app.route('/products')
@login_required
def get_products():
    check_admin()
    user=User.query.filter_by(id=current_user.id).first_or_404()
    # user.product is the relationship bet two tbls
    #products = user.product
    products=Product.query.all()
    form=ProductForm()
    return render_template('products.html', products=products,
                          user=user, form=form)

# handling the gets
@app.route('/products')
@login_required
def new_product():
    return render_template('products.html')

# handling the posts
@app.route('/products', methods=['POST'])
@login_required
def new_product_post():
    check_admin()
    form = ProductForm()
    if form.validate_on_submit():
        products = Product(name=form.name.data,
                            price=form.price.data,
                            description=form.description.data,
                            owned_user=current_user)
        db.session.add(products)
        db.session.commit()
        flash('The product has been inserted successfully!','success')
        return redirect(url_for('get_products'))
    return render_template('products.html', form=form)


# edit route
@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    check_admin()
    pro = Product.query.get_or_404(id)
    form = ProductForm(obj=pro)
    if form.validate_on_submit():
        pro.name = form.name.data
        pro.price = form.price.data
        pro.description = form.description.data
        db.session.commit()
        flash('The Product has been successfully updated.','info')

        return redirect(url_for('get_products'))
        
    elif request.method == 'GET':
        form.name.data = pro.name
        form.price.data = pro.price
        form.description.data = pro.description

    return render_template('products.html', 
                            form=form,
                           pro=pro)



# del route
@app.route('/products/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_product(id):
    check_admin()
    pro = Product.query.get_or_404(id)
    db.session.delete(pro)
    db.session.commit()
    flash('The product has been successfully deleted .','info')
    return redirect(url_for('get_products'))





##################################################################### registration, Login & logout
#registration 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = User(email=form.email.data,
                            username=form.username.data,
                            password=form. password.data)

        db.session.add(employee)
        db.session.commit()
        flash('you have been registered successfully!','success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')



#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the appropriate dashboard page
            if user.is_admin:
                flash('You Logged in successful ', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('You Logged in successful ', 'success')
                return redirect(url_for('user_dashboard'))

        else:
            flash('Inncorect email or password, try again.','danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been successfully logged out.','info')
    return redirect(url_for('login'))
