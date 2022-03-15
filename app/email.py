import os
from flask_mail import Message
from flask import render_template
from . import mail
import smtplib


subject_pref = 'bloGg'


def mail_message(subject,template,to,**kwargs):
   
    sender_email = 'antony.akono@student.moringaschool.com'
    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)