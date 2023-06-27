from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from lxml import etree
from time import sleep 
import smtplib
import imghdr
from email.message import EmailMessage

while(True):
    driver = webdriver.Chrome()
    driver.get('https://sis.eelu.edu.eg/static/index.html')  
    sleep(5)

    #login
    driver.find_element(By.XPATH, "//input[@id='name']").send_keys("UserName")
    driver.find_element(By.ID , 'password').send_keys("Password")
    driver.find_element(By.ID , 'usertype_1').click()
    driver.find_element(By.ID,'login_btn').click()
    print("loged in https://sis.eelu.edu.eg ")
    sleep(5)
    #Check degree
    driver.find_element(By.ID ,'crsGrd').click() 
    print("now in course degrees")

    sleep(5)
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    body = soup.find("body")
    dom = etree.HTML(str(body))

    degree = dom.xpath('//*[@id="divContents"]/table[4]/tbody/tr[1]/td[4]')[0].text
    degree=ord(degree.replace(" ", "")[0])

    if(degree>=65 and degree<=90):
        driver.get_screenshot_as_file("screenshot_for_degrees.png")
        # send on email 
        Sender_Email = "yousefmyiu@gmail.com"
        Reciever_Email = "yousefmyou@gmail.com"
        Password = "passwordForSesnder"

        newMessage = EmailMessage()                         
        newMessage['Subject'] = "crouses grade ^_^ " 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content('The degree of the courses appeared, I hope you succeeded ') 

        with open("screenshot_for_grades.png", 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
        print("i'm finished ")
        break
    else:
        driver.quit()
        print("The degree of the courses did not appeare \n I will take 1 hour break")
        sleep(3600)







