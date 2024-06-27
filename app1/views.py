from django.shortcuts import render,HttpResponse,redirect
import mysql.connector as sql 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import phonenumbers
from phonenumbers import carrier,geocoder
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')


un=''
ph=''
em=''
pwd=''

def SignupPage(request):
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="2621",database='django_user')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            global un,ph,em,pwd
            if key=="Name":
                un=value
            if key=="phonenumber":
                ph=value
            if key=="email":
                em=value
            if key=="password":
                pwd=value

        c="insert into users Values('{}','{}','{}','{}')".format(un,ph,em,pwd)
        cursor.execute(c)
        m.commit()       
        
    return render (request,'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        # Connect to MySQL database
        db = sql.connect(host="localhost", user="root", passwd="2621", database='django_user')
        cursor = db.cursor()
        
        # Get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password1')

        # Query database for user with matching username and password
        cursor.execute("SELECT * FROM users WHERE username = %s AND password1 = %s", (username, password))
        result = cursor.fetchone()

        # Close database connection
        cursor.close()
        db.close()

        # Check if user exists in database
        if result:
           return render (request,'home.html')
        else:
            return render(request,'warning.html')

    return render(request, 'login.html')

import mysql.connector

def OutputPage(request):
    if request.method == 'POST':
        num = request.POST.get('phone')
        phone_number = phonenumbers.parse(num)
        carrier_name = phonenumbers.carrier.name_for_number(phone_number, "en")
        region_name = phonenumbers.geocoder.description_for_number(phone_number, "en")
        
        # Establish database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2621",
            database="django_user"
        )
        
        # Retrieve user name from database based on phone number
        mycursor = mydb.cursor()
        sql = "SELECT username FROM users WHERE phone = %s"
        val = (num,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        
        # Check if user is registered
        if result:
            user_name = result[0]
        else:
            user_name = "USER NOT REGISTERED ON OUR SITE"
            
        output = {"carrier": carrier_name, "region": region_name, "user": user_name}

        return render(request, 'output_template.html', {'output': output})
    
    return render(request,'Output.html')




def LogoutPage(request):
    logout(request)
    return redirect('login')