import gmail

def send_credentials(email,name,acn,pwd):
     con=gmail.GMail("rishabhvermarishabhverma034@gmail.com","##########")   #app password
     body=f'''
     Hello {name},
     Welcome to ABC Bank,here is your credentials
     account No={acn}
     password={pwd}
     
     Kindly change your password when you login frist time
     ABC Bank
     Sector-16,Noida
     '''
     msg=gmail.Message(to=email,subject='Your Creantials for operating account',text=body)
     con.send(msg)
     

def send_otp(email,name,otp):
     con=gmail.GMail("rishabhvermarishabhverma034@gmail.com","uotq odck yrhi sncc")
     body=f'''
     Hello {name},
     Welcome to ABC Bank,here is your otp to recover password
     OTP={otp}
     ABC Bank
     Sector-16,Noida
     '''
     msg=gmail.Message(to=email,subject='OTP for password recovery',text=body)
     con.send(msg)
     
def send_otp_withdraw(email,name,otp,amt):
     con=gmail.GMail("rishabhvermarishabhverma034@gmail.com","uotq odck yrhi sncc")
     body=f'''
     Hello {name},
     Welcome to ABC Bank,here is your otp to withdraw {amt} 
     OTP={otp}
     ABC Bank
     Sector-16,Noida
     '''
     msg=gmail.Message(to=email,subject='OTP for withdrawl',text=body)
     con.send(msg)
     
def send_otp_transfer(email,name,otp,amt,to_acn):
     con=gmail.GMail("rishabhvermarishabhverma034@gmail.com","uotq odck yrhi sncc")
     body=f'''
     Hello {name},
     Welcome to ABC Bank,here is your otp to transfer amount: {amt} to ACN:{to_acn}
     OTP={otp}
     ABC Bank
     Sector-16,Noida
     '''
     msg=gmail.Message(to=email,subject='OTP for transfer',text=body)

     con.send(msg)
