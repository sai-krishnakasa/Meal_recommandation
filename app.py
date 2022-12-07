from flask_mail import Mail,Message
import pymysql,os
from flask_caching import Cache
from flask import Flask,render_template,url_for,redirect,request,jsonify,flash,session
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column,String,DateTime,Integer,create_engine,select
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime, timedelta
from flask_mail import Mail,Message
import myemail
import random,schedule

otp=random.randint(000000,999999)
engine=create_engine('mysql+pymysql://root:%401211292081Sai@localhost/Logins',echo=True)
Base=declarative_base()
app=Flask(__name__)
UPLOAD_FOLDER='static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
ALLOWED_EXTENSIONS=set(['jpg','png','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app.config['CACHE_TYPE']='SimpleCache'
app.config['SESSION_PERMANENT']=False
app.config['SESSION_TYPE']='filesystem'
app.secret_key='Hugescrectr'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = myemail.email
app.config['MAIL_PASSWORD'] = myemail.password
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
cache=Cache(app)
Session=sessionmaker()

class table(Base):
    __tablename__='table'
    item1=Column(String(10),primary_key=True)

class food(Base):
    __tablename__='Food_items'
    item=Column(String(50),unique=True,nullable=False,primary_key=True)
    calories=Column(Integer(),nullable=False)
    veg_or_nonveg=Column(String(10),nullable=False)
    period=Column(String(10),nullable=False)
    def __repr__(self):
        return f'<food item:{self.item},calories={self.calories}>'

class user_details(Base):
    __tablename__='user_details'
    name=Column(String(35),unique=True,nullable=False,primary_key=True)
    height=Column(String(3),nullable=False)
    weight=Column(String(3),nullable=False)
    bmi=Column(String(3),nullable=False)
    veg_or_nonveg=Column(String(10),nullable=False)
    date=Column(String(10),nullable=False,default=date.today())
    age=Column(Integer(),nullable=False)
    cal_limit=Column(Integer(),nullable=False)
    def __repr__(self):
        return f'<user_profile Name:{self.name},Height:{self.height}>'

class User(Base):
    __tablename__='users'
    fullname=Column(String(20),nullable=False)
    username=Column(String(10),nullable=False,primary_key=True)
    mobile=Column(String(10),nullable=False,unique=True)
    gender=Column(String(10),nullable=False)
    email=Column(String(30),nullable=False,unique=True)
    password=Column(String(200),nullable=False)
    def __repr__(self):
        return f'<User name:{self.username} email:{self.email} >'
        
@app.route('/meal_recommandation')
@cache.cached(timeout=30)
def meal_recommandation():
        local_session=Session(bind=engine)
        if 'username' in session:
            user=local_session.query(user_details).filter(user_details.name==session['username']).first()
        else:
            flash("Error You're Logged out/Session may be Expired,Please Login Again")
            return redirect(url_for('login'))
        count=user.cal_limit
        veg_or_nonveg=user.veg_or_nonveg
        breakfast_items=[]
        lunch_items=[]
        dinner_items=[]
        l=[]
        user_choice=local_session.execute(select(food.item,food.calories,food.period,food.veg_or_nonveg).where(food.veg_or_nonveg==veg_or_nonveg).order_by(food.period)).all()
        if veg_or_nonveg=='nonveg':
            veg_items=local_session.execute(select(food.item,food.calories,food.period,food.veg_or_nonveg).where(food.veg_or_nonveg=='veg').order_by(food.period)).all()
            for k in range(len(veg_items)//2):
                i=veg_items[k]
                if i[2].lower()=='breakfast':
                    breakfast_items.append([i[0],i[1]])
                elif i[2].lower()=='lunch':
                    lunch_items.append([i[0],i[1]])
                else:
                    dinner_items.append([i[0],i[1]])
            
            for i in user_choice:
                if i[2].lower()=='breakfast':
                    breakfast_items.append([i[0],i[1]])
                elif i[2].lower()=='lunch':
                    lunch_items.append([i[0],i[1]])
                else:
                    dinner_items.append([i[0],i[1]])
            
            random.shuffle(breakfast_items)
            random.shuffle(lunch_items)
            random.shuffle(dinner_items)
            breakfast_cal=count/3
            lunch_cal=count/3
            dinner_cal=count/3
            breakfast=[]
            lunch=[]
            dinner=[]
            for i in breakfast_items:
                    if breakfast_cal-i[1]>0:
                        breakfast.append(i[0])
                        breakfast_cal-=i[1]
            for i in lunch_items:
                    if lunch_cal-i[1]>0:
                        lunch.append(i[0])
                        lunch_cal-=i[1]
            for i in dinner_items:
                    if dinner_cal-i[1]>0:
                        dinner.append(i[0])
                        dinner_cal-=i[1]
            return render_template('meal_plan.html',breakfast=breakfast,lunch=lunch,dinner=dinner)
        else:
            for i in user_choice:
                if i[2].lower()=='breakfast':
                    breakfast_items.append([i[0],i[1]])
                elif i[2].lower()=='lunch':
                    lunch_items.append([i[0],i[1]])
                else:
                    dinner_items.append([i[0],i[1]])
            random.shuffle(breakfast_items)
            random.shuffle(lunch_items)
            random.shuffle(dinner_items)
            breakfast_cal=count/3
            lunch_cal=count/3
            dinner_cal=count/3
            breakfast=[]
            lunch=[]
            dinner=[]
            for i in breakfast_items:
                if breakfast_cal-i[1]>0:
                    breakfast.append(i[0])
                    breakfast_cal-=i[1]
            for i in lunch_items:
                    if lunch_cal-i[1]>0:
                        lunch.append(i[0])
                        lunch_cal-=i[1]
            for i in dinner_items:
                if dinner_cal-i[1]>0:
                    dinner.append(i[0])
                    dinner_cal-=i[1]
            return render_template('meal_plan.html',breakfast=breakfast,lunch=lunch,dinner=dinner,head='Meal Recommandation')
def send_mail(user):
    msg=Message('OTP:',recipients=[user.email],sender='noreply@gmail.com')
    msg.body=f'''
           OTP: {otp}
        If you don't send a password reset request.please ignore the mail
    '''
    mail.send(msg)
@app.route('/reset_password',methods=['POST','GET'])
def reset_password():
    local_session=Session(bind=engine)
    if request.method=='POST':
        email=request.form['email']
        user=local_session.query(User).filter(User.email==email).first()
        if user:
            send_mail(user)
            flash('Success : OTP  sent,Check your Mail')
            return redirect(url_for('verify_otp'))
    return render_template('reset_request.html',head='Password Reset')
@app.route('/verify_otp',methods=['POST','GET'])
def verify_otp():
    if request.method=='POST':
        if request.form['otp']==otp:
            flash('Email Verified Successfully')
            return render_template('change_password.html',head='CGange-Password')
        else:
            flash('Invalid OTP ')
            return render_template('verify_otp.html',head='VERIFY_OTP')
    else:
        return render_template('verify_otp.html',head='VERIFY_OTP')
@app.route('/')
@app.route('/register',methods=['POST','GET'])
def register():
    if 'username' in session:
        flash('Continuing with Previous session')
        return redirect(url_for('user_detail'))
    if request.method=='POST':
        local_session=Session(bind=engine)
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        gender=request.form.get('gender')
        fullname=fname+" "+lname
        username=request.form.get('username')
        mobile=request.form.get('mobile')
        email=request.form.get('email')
        file=request.files['file']
        password=request.form.get('password')
        cpassword=request.form.get('cpassword')
        special_chars=['@','$','#','%','_']
        if  not len(password) or not len(username) or not len(mobile) or not len(email)  or not len(gender):
                flash('Error Fill All The Feilds Before Submitting')
                return redirect(url_for('register'))
        if password != cpassword:
            flash(' Error, Both Password and Confirm Password Should be same')
            return redirect(url_for('register'))
        else:
            new_user=User(gender=gender,fullname=fullname,username=username,email=email,password=generate_password_hash(password),mobile=mobile)
            user=local_session.query(User).filter(User.username==username).first()
            if(user):
                if user.username==username and user.email==email:
                    flash(' Error Account Already Exists,Login Here')
                    return redirect(url_for('login'))
                if user.username==username:
                    flash('Error Username Already Exists')
                    return redirect(url_for('register'))
                if  user.email==email:
                    flash(' Error Email Already Exists,Try With Another Mail')
                    return redirect(url_for('register'))
            elif local_session.query(User).filter(User.email==email).first():
                flash(' Error Email Already Exists!')
                return redirect(url_for('register'))
            else:
                ends=['com','in']
                if email.split('.')[-1] not in ends:
                    flash(' Error INVALID EMAIL')
                    return redirect(url_for('register'))
                elif gender.lower()!='male' and gender.lower()!='female':
                    flash(' Error Only Male or Female can Register')
                    return redirect(url_for('register'))
                elif len(username)>10 or len(username)<5 :
                    flash(' Error Username should be max:10 characters or Min:5characters  ')
                    return redirect(url_for('register'))
                elif  username[0] in special_chars or username[0].isdigit():
                    flash('Error username should not start with special characters or numbers')
                    return redirect(url_for('register'))
                elif local_session.query(User).filter(User.mobile==mobile).first():
                    flash(f'Error An account with Number {mobile } already Exists')
                    return redirect(url_for('register'))
                elif mobile[0] not in ['6','7','8','9']  or len(mobile)!=10 or not mobile.isdigit():
                    flash('Error Invalid Mobile NUmber')
                    return redirect(url_for('register'))
                elif file.filename=='':
                    flash('Error No image selected')
                    return redirect(url_for('register'))
                elif  not allowed_file(file.filename):
                    flash(f'These are the Allowed extensions{ALLOWED_EXTENSIONS}')
                    return redirect(url_for('register'))
                elif len(password)<6:
                    flash('Error Password should be atleast 8 characters')
                    return redirect(url_for('register'))
                elif not any(char.isdigit() for char in password):
                    flash(' Error Password should have atleast one numeral')
                    return redirect(url_for('register'))
                elif not any(char.isupper() for char in password):
                    flash(' Error Password should have atleast  one Upper Character')
                    return redirect(url_for('register'))
                elif not any(char.islower() for char in password):
                    flash('Error Password should be  atleast one lower Character')
                elif not any(char in special_chars for char in password):
                    flash('Error Password should be atleast one Special Character')
                    return redirect(url_for('register'))
                else:
                    filename=file.filename
                    basedir = os.path.abspath(os.path.dirname(__file__))
                    file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'],username+'.png'))
                    local_session.add(new_user)
                    local_session.commit()
                    flash(f'Status: An Account with {new_user.username.upper()} is created')
                    return redirect(url_for('login',name=new_user.username))
    else:
        return render_template('register.html',head='REGISTER',title='Register')
@app.route('/edit_user',methods=['POST',"GET"])
def edit_user():
    local_session=Session(bind=engine)
    if request.method=='POST':
        file=request.files['file']
        username=session['username']
        height=float(request.form.get( 'height' ))
        weight=float(request.form.get( 'weight' ))
        age=int(request.form.get('age'))
        mobile=request.form.get('mobile')
        bmi=(weight/(height*height))
        cal_limit=request.form.get('cal_limit')
        session['cal_limit']=cal_limit
        user_det=local_session.query(user_details).filter(user_details.name==session['username']).first()
        if mobile[0] not in ['6','7','8','9']  or len(mobile)!=10 or not mobile.isdigit():
                flash('Error Invalid Mobile NUmber')
                return redirect(url_for('edit_user'))
        if file:
            if file.filename=='':
                flash('Error No image selected')
                return redirect(url_for('edit_user'))
            elif  not allowed_file(file.filename):
                flash(f'These are the Allowed extensions{ALLOWED_EXTENSIONS}')
                return redirect(url_for('edit_user'))
        users=local_session.query(User).filter(User.username==session['username']).first()
        dup_entry=local_session.query(User).filter(User.mobile==mobile).first()
        if(dup_entry):
            flash('Try with Another Mobile Number,it is Already Registered with Another user')
            return redirect(url_for('edit_user'))
        user_det.height=height
        users.mobile=mobile
        user_det.weight=weight
        user_det.age=age
        user_det.bmi=bmi
        user_det.cal_limit=cal_limit
        user_det.date=datetime.now().date()
        basedir = os.path.abspath(os.path.dirname(__file__))
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'],username+'.png'))
        local_session.commit()
        flash('Profile Successfully Updated')
        flash('A meal Has Recommanded According to your New Goal Plan,Check it out in Meal Recommmandation Section')
        return redirect(url_for('user_profile'))
    else:
        user=local_session.query(user_details).filter(user_details.name==session['username']).first()
        print(user)
        if user:
            return render_template('edit_profile.html',head='EDIT PROFILE',user=user,title='EDIT PROFILE')
        else:
            flash('Error Please Login to Edit user')
            return redirect(url_for('login'))
@app.route('/calorie_counter',methods=['POST','GET'])
def calorie_counter():
    local_session=Session(bind=engine)
    items=local_session.query(food).with_entities(food.item,food.calories).all()
    if request.method=='POST':
        data=request.form.items()
        total_cal=0
        for i in data:
            print(i)
            total_cal+=int(i[1])
            print(i[1])
        flash(f'Total calories of selected items : {total_cal}')
        return redirect(url_for('calorie_counter'))
        # list=['idli','eggrice','brownrice','whiterice','bananajuice','parathas','chapathi','dosa']
        # selected_items=" "
        # res=0
        # for i in list:
        #     val=request.form.get(i)
        #     if(val!=None):
        #         selected_items+=i.upper()+' ,'
        #         res+= int(val)
        # flash(f" Sum of calories of selected Items are:"+str(res))
    #     return render_template('calorie_counter.html',head='Calorie Counter')
    else:
         return render_template('calorie_counter.html',items=items,head='Calorie Counter',title='Calorie Counter')
@app.route('/user_profile',methods=['GET','POST'])
def user_profile():
    local_session=Session(bind=engine)
    if 'username' in session:

        user_det=local_session.query(user_details).filter(user_details.name==session['username']).first()
        user=local_session.query(User).filter(User.username==session['username']).first()
        return render_template('user_profile.html',user_det=user_det,user=user,head='Dashboard',title='user-profile')
    else:
        flash('Error Please Login to get User Profile')
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('cal_limit',None)
    session.pop('login_time',None)
    session.pop('logout_time',None)
    name=session.pop('username',None)
    if name:
        flash(f"Hello {name} ,You're Successfully Logged out")
        return redirect(url_for('login'))
    else:
        flash('Error Already Logged out')
    return redirect(url_for('login'))
@app.route('/user_detail',methods=['GET',"POST"])
def user_detail():
    if 'username' in session:
        local_session=Session(bind=engine)
        if request.method=='POST':
            name=session['username']
            height=float(request.form.get('height'))
            weight=float(request.form.get('weight'))
            bmi=(weight/(height*height))
            veg_or_nonveg=request.form.get('veg_or_nonveg')
            age=int(request.form.get('age'))
            cal_limit=request.form.get('cal_limit')
            session['cal_limit']=cal_limit
            if not height or not weight or not age or not cal_limit or not veg_or_nonveg: 
                flash('Error Please Fill All The Feilds')
                return redirect(url_for('user_detail'))
            if veg_or_nonveg.lower() not in ['veg','nonveg']:
                flash('Error Enter valid details in Veg/Nonveg Field')
                return redirect(url_for('user_detail'))
            user=user_details(bmi=bmi,veg_or_nonveg=veg_or_nonveg,name=name,height=height,weight=weight,cal_limit=cal_limit,age=age,date=date.today())
            local_session.add(user)
            local_session.commit()
            flash('A meal Has Recommanded According to your Goal,Check it out in Meal Recommmandation Section')
            return redirect(url_for('user_profile'))
        else:
            if local_session.query(user_details).filter(user_details.name==session['username']).first():
                return redirect(url_for('user_profile'))
            return render_template('user_form.html',head=f"{session['username'].upper()} Profile",name=session['username'].upper(),title='Profile')
    else:
        
        flash('Error Please Login to get User_details')
        return redirect(url_for('login'))

@app.route('/session')
def sess():
    if 'username' in session:
        return session['username']
    else:
        return 'None'

@app.route('/login',methods=['POST','GET'])
def login():
    if 'username' in session and 'cal_limit' in session:
        flash('Session Already Active')
        return redirect(url_for('user_detail'))
    elif request.method=='POST':
        if 'username' in session and 'cal_limit' in session:
            flash('Session Already Active')
            return redirect(url_for('user_detail'))
        local_session=Session(bind=engine)
        username=request.form.get('username')
        session['username']=username
        password=request.form.get('password')
        #query to fetch user with login username
        user=local_session.query(User).filter(User.username==username).first() 
        user_detai=local_session.query(user_details).filter(user_details.name==username).first()
        if(user_detai):
            session['cal_limit']=user_detai.cal_limit
        #query to fetch user_details from user_details database if exists
        # user_det=local_session.query(user_profile).filter(user_profile.name==username).first()
        if(user):
            if user.username==username and  check_password_hash(user.password,password) :
                # session['login_time']=datetime.now().strftime('%H:%M:%S')
                # session['logout_time']=(datetime.now()+timedelta(minutes=1)).strftime('%H:%M:%S')
                flash(f"Hello {user.username} ,You're SuccessFully Logged in")
                flash('A meal Has Recommanded According to your  Goal Plan,Check it out in Meal Recommmandation Section')
                return redirect(url_for('user_detail'))
            elif (user.username==username and not user.password==password):
                session.pop('username')
                flash("Error: Incorrect   Password" )
                return render_template('login.html',name=username)
            else :
                session.pop('username')
                flash("Error: Incorrect UserName " )
                return redirect(url_for('login'))
        else:
            session.pop('username')
            flash(" Error User Doesn't Exist,Create An Account")
            return redirect(url_for('register'))  
    else:
        return  render_template('login.html',head='LOGIN',title='Login')

@app.route('/about')
def about():
    return render_template('about.html',head='ABOUT',title='About')
    
if __name__=='__main__':
    app.run(debug=True)