import cv2
import datetime
import os
import pysftp
import uuid

mac = '-'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8*6, 8)][::-1])

# FTP details
config = {
    "host": "207.244.74.204",
    "username": "fryscrypto",
    "password": "Wtf.7001",
}

last_upload_hour = datetime.datetime.now().hour

# Initialize the current_file variable
now = datetime.datetime.now()
current_file = f"FRYimage_{mac}_{now.strftime('%m%d%Y_%H%M%S')}.jpg"

cap = cv2.VideoCapture(0)

def save_image():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        return
    cv2.imwrite(current_file, frame)

def upload_to_sftp(current_file, config):
    local_filename = current_file
    remote_filename = f"/home/fryscrypto/traffic_camera/FRYimage_{mac}_{now.strftime('%m%d%Y_%H%M%S')}.jpg"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    with pysftp.Connection(config['host'], username=config['username'], password=config['password'], cnopts=cnopts) as sftp:
        sftp.put(local_filename, remote_filename)
    os.remove(local_filename)  # removes local file after upload

while True:
    now = datetime.datetime.now()

    # Capture image every 10 seconds
    if now.second % 10 == 0:
        save_image()
        print(f"Saved image at {now.strftime('%H:%M:%S')}")  # printing for visibility
    
    # Upload the file one minute before the top of the hour
    if now.minute == 59 and now.second == 0:
        upload_to_sftp(current_file, config)

    # Update the filename at the top of the hour
    if now.minute == 0 and now.second == 0 and now.hour != last_upload_hour:
        current_file = f"FRYimage_{mac}_{now.strftime('%m%d%Y_%H%M%S')}.jpg"
        last_upload_hour = now.hour

cap.release()
cv2.destroyAllWindows()
