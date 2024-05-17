import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#Parent directory where item sorting will be applied. 
src_dir = "C:/Users/harve/Downloads"


audio_ext = [".m4a",".flac",".mp3",".wav", ".wma",".aac"]
video_ext = [".mp4"]
image_ext = [".jpg", ".png",".jpeg"]

#Gets all available file extensions in src_dir
def get_file_extensions(dir):
    file_ext = []
    for i in os.listdir(dir):
        if not os.path.splitext(i)[1] in file_ext:
            file_ext.append(os.path.splitext(i)[1])        
    return file_ext
    
#Cleaning function that sorts files into respective folders based on file type
def clean(src_dir):
    ext_list= get_file_extensions(src_dir)
    for i in os.listdir(src_dir):
        if os.path.splitext(i)[1] in image_ext:
            dest_folder = os.path.join(src_dir, "Images Folder")
            if not os.path.exists(os.path.join(src_dir, "Images Folder")):
                os.mkdir(dest_folder)
            shutil.move(os.path.join(src_dir,i),dest_folder)

        elif os.path.splitext(i)[1] in video_ext:
            dest_folder = os.path.join(src_dir, "Video Folder")
            if not os.path.exists(os.path.join(src_dir, dest_folder)):
                os.mkdir(dest_folder)
            shutil.move(os.path.join(src_dir,i),dest_folder)

        elif os.path.splitext(i)[1] in audio_ext:
            dest_folder = os.path.join(src_dir, "Audio Folder")
            if not os.path.exists(os.path.join(src_dir, dest_folder)):
                os.mkdir(dest_folder)
            shutil.move(os.path.join(src_dir,i),dest_folder)       
            
        elif os.path.splitext(i)[1] in ext_list and not os.path.isdir(os.path.join(src_dir,i)):
            dest_folder = os.path.join(src_dir, "Others")
            if not os.path.exists(os.path.join(src_dir, dest_folder)):
                os.mkdir(dest_folder)
            shutil.move(os.path.join(src_dir,i),dest_folder)

#Declaring event to be passed when any modifications are detected inside parent directory.
class TheCleansing(LoggingEventHandler):
    def on_modified(self,event):
        clean(src_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = src_dir
    event_handler = TheCleansing()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
