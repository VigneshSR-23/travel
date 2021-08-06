from django.shortcuts import redirect, render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from travello.models import Details
from travello.models import Destination
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')
def login(request):
    if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
            auth.login(request,user)
            return redirect("/")
         else:
            messages.info(request,'INVALID CREDENTIALS')
            return redirect('login')
    else:
        return render(request,'login.html')

def register(request):
    if request.method=='POST':

        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['user_name']
        password1=request.POST['password1']
        password2=request.POST['password2']
        emails=request.POST['email']
        Wallet=request.POST['wallet']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'USERNAME TAKEN') 
                return redirect('register')
            elif User.objects.filter(email=emails).exists():
                messages.info(request,'EMAIL TAKEN')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=emails,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                print(user)
                print(user.email)
                
        else:
            messages.info(request,'PASSWORD NOT MATCHING')
            return redirect('register')
        return redirect('index')
    else:
        return render(request,'register.html')
    
   
def book(request):
    amt=0;
    flag=False
    temp1=0
    temp2=""
    s=""
    h=""
    flag2=False
    check=False
    if(request.method=='POST'):
        s=request.POST['city']
        h=request.POST['mail']
        use=request.POST['uses']
        passw=request.POST['pas']
        #username=request.POST['username']
        #password=request.POST['password']
        #user=auth.authenticate(username=username,password=password)
        desti=Destination.objects.all()
        # print(s)
        k=Details.objects.all()
        for k1 in k:
            if k1.email==h:
                check=True
                break
        users=auth.authenticate(username=use,password=passw)
        if users is not None and check==False:
            detail1=Details.objects.create(names=use,email=h,places="",wallet=5000)
            detail1.save()
        for p in desti:
            if s==p.name:
                print(p.name)
                amt=p.price
                flag2=True
                break
        if flag2==False:
            messages.info(request,"  CHOOSE AVAILABLE LOCATION   ")
            return render(request,'book.html')
        d=Details.objects.all()

        for f in d:
            if h==f.email:
                flag=True
                user=auth.authenticate(username=use,password=passw)
                if user is not None:
                    temp1=f.wallet
                    temp2=f.places
                    break
                else:
                    messages.info(request," ** INVALID CREDENTIALS ** ")
                    return render(request,'book.html')
        if flag:
            if s in temp2:
                messages.info(request,'**  LOCATION BOOKED ALREADY **')
                return render(request,'book.html')
            elif(temp1<amt):
                messages.info(request,'**YOUR CURRENT BALANCE IS LESS THAN THE PRICE OF THE SELECTED LOCATION **')
                messages.info(request,'CURRENT BALANCE :'+str(temp1))
                messages.info(request,'COST OF SELECTED LOCATION :'+str(amt))
                return render(request,'book.html')
            else:
                Details.objects.filter(email=h).update(wallet=temp1-amt)
                Details.objects.filter(email=h).update(places=s+" , "+temp2)
            des=Details.objects.all()
            
            for p in des:
                if p.email==h:
                    break
            return render(request, "book.html", {'des': p})
        else:
           messages.info(request,'** CREATE ACCOUNT FIRST AND THEN TRY TO BOOK LOCATIONS **')
           return redirect('book')
    subject = "Travel"
    body = "This is an email with attachment sent from Python"
    sender_email = "travellowebsitedjango@gmail.com"
    receiver_email = h
    password = "vigneshsubu@"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    filename = "abc.txt"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",)
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text) 
    return render(request,'book.html')


    

      
