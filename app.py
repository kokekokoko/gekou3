from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta,time 
import jpholiday 
import pytz 
from zikokuhyou import kasugaeki, keiosinjukustation 

app = Flask(__name__)
def isBizDay(Date):
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return 1 #holiday
    else:
        return 0 #weekday
    
def nexttrain(time1,eki,isweekday):
    ans = []
    for zikan, hun in eki[isweekday].items():
        if time1.hour > zikan:
            continue
        elif time1.hour == zikan:
            for i in range(len(hun)):
                if len(ans) == 3:
                    return ans 
                if time1.minute <= hun[i]:
                    ans.append(datetime.combine(datetime.today(),time(zikan,hun[i])))
        elif time1.hour < zikan:
            for i in range(len(hun)):
                if len(ans) == 3:
                    return ans 
                if zikan == 24:
                    zikan = 0 
                    
                ans.append(datetime.combine(datetime.today(),time(zikan,hun[i])))
    return ans 

@app.route("/")
def gekou():
    return render_template('index.html')

@app.route("/gekou")
def gekoukaisi():
    
    school_DP = datetime.now()
    isweekday = isBizDay(school_DP)
    day = "平日" if isweekday == 0 else "休日"
    kasuga_AR = school_DP + timedelta(minutes=10)
    kasuga_DP = nexttrain(kasuga_AR.time(), kasugaeki, isweekday)[0]
    shinjukunishiguchi_AR = kasuga_DP + timedelta(minutes=14)
    keioshinjuku_AR = shinjukunishiguchi_AR + timedelta(minutes=6)
    keioshinjuku_DP = nexttrain(shinjukunishiguchi_AR,keiosinjukustation, isweekday)
    
    return render_template("kekka.html",school_DP = school_DP,kasuga_AR=kasuga_AR,
                           kasuga_DP=kasuga_DP,shinjukunishiguchi_AR=shinjukunishiguchi_AR,keioshinjuku_AR=keioshinjuku_AR,keioshinjuku_DP=keioshinjuku_DP,day=day)