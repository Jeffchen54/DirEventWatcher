"""
Extremely simple script written in half an hour for automating 
Google SMTP request for file changes.

Script is intended for sending email alerts regarding file creations to 
FTP server from an intentionally misconfigured security camera to prevent
Internet access but allow LAN access.

Automated response sends attachments matching ATTACHMENT_TYPE and 
ATTACHMENT_SIZE for files created in WATCHDIRECTORY
"""

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



# SMTP variables
SENDER = ""                 # Sender gmail
RECIPIENTS = [""]           # List of recepiants
PASSWORD = ""               # app password for sender gmail

# Watchdog
WATCHDIRECTORY = r""        # r"M:\...\testdir"
ATTACHMENT_TYPE = ['']      # .jpg, .mp4, ...
ATTACHMENT_SIZE = 1024      # bytes
TIME_BETWEEN_EVENT = 1      # Seconds between change scans


def send_email(subject:str, body:str, sender:str, recipients:list[str], password:str, files:list[str]=[])->None:
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body))
    
    
    for path in files:
        part = MIMEBase('application', "octet-stream")
        
        # wait for file to download fully
        file_sz = -1
        while file_sz != Path(path).stat().st_size:
            file_sz = Path(path).stat().st_size
            sleep(1)
        
        try:            
            with open(path, 'rb') as file:
                    part.set_payload(file.read())
                    
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)
        except Exception as err:
            print(f"Unexpected error opening {path} is",repr(err))
    
    try:    
        with SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            
    except Exception as err:
        print(f"Unexpected error {sender} cannot email {', '.join(recipients)} is",repr(err))

class OnMyWatch:
    # Set the directory on watch
 
    def __init__(self, watchDirectory):
        self.observer = Observer()
        self.watchDirectory = Path(watchDirectory)
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        print("Watchdog is now running")
        try:
            while True:
                sleep(TIME_BETWEEN_EVENT)
        except:
            self.observer.stop()
            print("Observer Stopped")
 
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
        
    @staticmethod
    def on_created(event):
        if event.is_directory or \
            not len(set(Path(event.src_path).suffixes).intersection(set(ATTACHMENT_TYPE))) > 0 or \
                not Path(event.src_path).stat().st_size <= ATTACHMENT_SIZE:
            return None
        
        # Event is created, you can process it now
        print(f"Watchdog received created event - {event.src_path}.")
        send_email(f"Watchdog CREATED {event.src_path}",\
            f"{event.src_path}.",\
                SENDER,\
                    RECIPIENTS,\
                        PASSWORD,\
                            [event.src_path])
 
if __name__ == '__main__':
    watch = OnMyWatch(WATCHDIRECTORY)
    watch.run()
    