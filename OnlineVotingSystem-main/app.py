from flask import Flask,render_template,request
from admin import *
from voter import *
import win32api
from faceunlock import *
from livepro import *
from threading import Thread
import multiprocessing

app=Flask(__name__)
vid=0

# home page
@app.route("/")
def homepage_get():
    return render_template("homepage.html")

# admin login
@app.route("/admin",methods=['GET','POST'])
def admin_get():
    return render_template("adminLogin.html")  

# admin menu
@app.route("/admin/adminMenu",methods=['GET','POST'])
def adminMenu_get():
    name = request.form.get('uname')
    passw = request.form.get('pass')

    if log_admin(name,passw)==True:
        win32api.MessageBox(0, 'Logged In successfully!!!', 'Valid credentials', 0x00001000)
        return render_template("adminMenu.html")
    
    win32api.MessageBox(0, 'Invalid username/password', 'Invalid credentials', 0x00001000)
    return render_template("adminLogin.html")

# register candidate
@app.route("/admin/adminMenu/regCand")
def regCand_get():
    pnames=get_partyNames()
    cnames=get_candNames()
    cities=get_city()
    zones=get_zone()
    return render_template("regCandPage.html",pnames=pnames,cnames=cnames,cities=cities,zones=zones)

# success page
@app.route("/admin/adminMenu/regCand/success",methods=['GET','POST'])
def regCandSuccess():
    pname = request.form.get('pname')
    cname = request.form.get('cname')
    gender = request.form.get('gender')
    cvid = request.form.get('voterId')
    city = request.form.get('city')
    zone = request.form.get('zone')
    age = request.form.get('age')
    if int(age)<25:
        win32api.MessageBox(0, 'Age Criteria failed!! Your age is below the minimum age', 'Failure message', 0x00001000)
    if verify(int(cvid))==False:
        win32api.MessageBox(0, "Candidate registeration failed!! You don't have a registered voter id", 'Failure message', 0x00001000)
    elif taking_data_candidate(pname,cname,gender,city,zone)==True:
        win32api.MessageBox(0, 'Candidate registered successfully!!!', 'Success message', 0x00001000)
        return render_template('adminMenu.html')
    return regCand_get()

# results page
@app.route("/admin/adminMenu/showResults",methods=['GET','POST'])
def showResults_get():
    table_data=show_result()
    return render_template("finalResultPage.html",table_data=table_data)

# reset 
@app.route("/admin/adminMenu/resetAll",methods=['GET','POST'])
def resetAll():
    if count_reset()==True:
        win32api.MessageBox(0, 'Reset process completed!!!', 'Resetting', 0x00001000)
        return render_template("adminMenu.html")
    return homepage_get()

# voter id verification page
@app.route("/voter",methods=['GET','POST'])
def voterId_get():
    return render_template('voterIdVeri.html')

# voter id verified and redirected to otp verification
@app.route("/voter/otp",methods=['GET','POST'])
def vidVerify():
    global vid
    vid= request.form.get('vid')
    print(type(vid))
    msg=log_server(vid)
    if msg=='valid voter':
        win32api.MessageBox(0, 'Valid voter!!!', 'Voter ID Verification', 0x00001000)
        return render_template('otpVeri.html') 
    win32api.MessageBox(0, msg , 'Voter ID Verification', 0x00001000)
    return voterId_get()

genOtp=0

@app.route("/voter/otp/send",methods=['GET','POST'])
def sendOtp():
    global genOtp
    genOtp=otpGen(vid)
    print(genOtp)
    win32api.MessageBox(0, 'OTP sent to registered mobile number!!!', 'OTP Verification', 0x00001000)
    return render_template('otpVeri.html')

# otp verified
@app.route("/voter/otp/success",methods=['GET','POST'])
def otpVerify():
    otpget=request.form.get('otp')
    print(otpget)
    print(genOtp)
    if checkOTP(otpget,genOtp)=="Verification Successful":
        win32api.MessageBox(0, 'Verified Successfully!!!', 'OTP Verification', 0x00001000)

        global t
        t = multiprocessing.Process(target=liveProct, args=[True])
        t.start()

        return render_template('faceRec.html')
    win32api.MessageBox(0, 'Invalid OTP!!!', 'OTP Verification', 0x00001000)
    return render_template('otpVeri.html')

# face unlock
@app.route("/voter/faceUnlock",methods=['GET','POST'])
def faceRec():
    if unlockFace(vid)=="Face unlocked!":
        win32api.MessageBox(0, 'Verified Successfully!!!', 'Face Authentication', 0x00001000)
        return render_template("votingPage.html")
    t.terminate()
    win32api.MessageBox(0, 'Invalid Face!!!', 'Face Authentication', 0x00001000)
    return render_template('voterIdVeri.html')

# vote casted
@app.route("/voter/voteCast",methods=['GET','POST'])
def votcastPage():
    parName=request.form.get('candidate')
    print(parName)
    print(vid)
    
    if vote_update(parName,vid) and liveProct(False)=='Success':
        win32api.MessageBox(0, 'Vote Casted Successfully!!!', 'Success', 0x00001000)
    else:
        win32api.MessageBox(0, 'Failure!!!', 'Failure', 0x00001000)
    t.terminate()
    return render_template("homepage.html")


if __name__=="__main__": 
    app.run(debug=True)