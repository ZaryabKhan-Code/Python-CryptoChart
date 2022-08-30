from api import Crypto
import imghdr
from email.message import EmailMessage
from flask import Flask, render_template,request, make_response,redirect,url_for
import math,smtplib,os
from flask_sqlalchemy import SQLAlchemy

IMG_FOLDER = os.path.join('static', 'bugs')
UPLOAD_FOLDER = IMG_FOLDER
app = Flask(__name__)
crypto  = Crypto()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:zaryab@localhost/cryptobug"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    namez = db.Column(db.String(200))
    message = db.Column(db.String(1000))
    image = db.Column(db.String(2000))
    filename = db.Column(db.String(200)) 

@app.route("/")
def hello():
    results = crypto.get_top_5()
    last = math.ceil(len(results)/int(100))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page= int(page)
    results = results[(page-1)*int(100): (page-1)*int(100)+ int(100)]
    if (page==1):
        prev = "#"
        next = "/?page="+ str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    return render_template('index.html',page=page,prev=prev,next=next, results=results)

@app.route("/coin/<id>/<name>/<symbol>/<cmc_rank>/<num_market_pairs>/<circulating_supply>/<total_supply>/<max_supply>/<last_updated>/<date_added>/<price>/<volume_24h>/<volume_change_24h>/<percent_change_1h>/<percent_change_24h>/<percent_change_7d>/<market_cap>/<market_cap_dominance>/<fully_diluted_market_cap>")
def coin(id,name,symbol,cmc_rank,num_market_pairs,circulating_supply,total_supply,max_supply,last_updated,date_added,price,volume_24h,volume_change_24h,percent_change_1h,percent_change_24h,percent_change_7d,market_cap,market_cap_dominance,fully_diluted_market_cap):
    return render_template('details.html', id=id,name=name,symbol=symbol,cmc_rank=cmc_rank,num_market_pairs=num_market_pairs,circulating_supply=float(circulating_supply),total_supply=float(total_supply),max_supply=max_supply,last_updated=last_updated,date_added=date_added,price=float(price),volume_24h=volume_24h,volume_change_24h=float(volume_change_24h),percent_change_1h=float(percent_change_1h),percent_change_24h=float(percent_change_24h),percent_change_7d=float(percent_change_7d),market_cap=float(market_cap),market_cap_dominance=float(market_cap_dominance),fully_diluted_market_cap=float(fully_diluted_market_cap))

@app.route("/report/", methods=["GET", "POST"])
def contact():
    email = request.form.get('email')
    name = request.form.get('name')
    message = request.form.get('message') 
    if request.method=='POST':
        msg = EmailMessage()                         
        msg['Subject'] = "Bug Reported CryptoChart"
        msg['From'] = email
        msg['To'] = 'zk126128@gmail.com'
        if "image" not in request.files:
                    return "there is no file1 in form!"
        file1= request.files["image"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
        file1.save(path)
        entry = users(email=email,namez=name,message=message,image=file1,filename=file1.filename)
        db.session.add(entry)
        db.session.commit()
        user = users.query.filter_by(email=email).first()
        msg.set_content('Dear, Zaryab Message from Real Time CryptoChart \n'+name+ 'Report a bug \nHis email is' +email+ '\nMessage '+message) 
        with open('static/bugs/'+user.filename, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename='static/bugs/'+user.filename)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('zk126128@gmail.com', 'gcfwjbdlhkpevjvl')              
            smtp.send_message(msg)
            return redirect(url_for('hello'))  
    return render_template('contact.html', **locals())

@app.route("/set/")
@app.route("/set/<theme>/")
def set_theme(theme="light"):
  res = make_response(redirect(url_for("hello")))
  res.set_cookie("theme", theme)
  return res


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)


