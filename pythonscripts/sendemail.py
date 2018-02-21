#!/usr/bin/python

import smtplib
import getpass

def send_email(user, pwd, recipient, subject, body):

   gmail_user = user
   gmail_pwd = pwd
   FROM = user
   TO = recipient if type(recipient) is list else [recipient]


   SUBJECT = subject
   TEXT = body

   # Prepare actual message
   message = """From: %s\nTo: %s\nSubject: %s\n\n%s
   """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
   try:
       server = smtplib.SMTP("smtp.gmail.com", 587)
       server.ehlo()
       server.starttls()
       server.login(gmail_user, gmail_pwd)
       server.sendmail(FROM, TO, message)
       server.close()
       print 'successfully sent the mail'
   except Exception as e:
       print e 

def main():
   user = raw_input("Enter your mail ID: ")
   pwd = getpass.getpass(prompt='Password: ')
   recipient = raw_input("Enter recipient list: ")
   subject = raw_input("Enter Email subject: ")
   body = raw_input("Enter Email body: ")
   send_email(user, pwd, recipient, subject, body)

if __name__ == "__main__":
   main()
