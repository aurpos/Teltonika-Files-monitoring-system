import os
from pathlib import Path
import shutil
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

open_conf = open('config.json')
data = json.load(open_conf)

source_dir_name = data["sourceDirectory"]
dst_dirs = data["destDirectories"]
default_dir = data["defaultDirectory"]

# move files to the destination directory which depends on the extension
def move_files(dir_name):
    files = Path(dir_name).glob('*')
    for file in files:
        #f.write(str(file) + "\n")
        src_path = os.path.join(source_dir_name, os.path.basename(file))
        ext = extensionType(file)
        file_name = os.path.basename(file)
        for conf_ext in dst_dirs:
            if conf_ext == ext:
                dst_path = os.path.join(dst_dirs[conf_ext], os.path.basename(file))
                f.write("Extension is " + conf_ext + "\n")
                result = checkDestinationFiles(dst_dirs[conf_ext], file_name)
                print(result)
                if if_dest_dir_exists(dst_dirs[conf_ext]) and result == False:
                    break
                elif if_dest_dir_exists(dst_dirs[conf_ext]) and result != False: 
                    print(if_dest_dir_exists(dst_dirs[conf_ext]))
                    shutil.move(src_path, dst_path)
                    f.write("File is moved in " + dst_dirs[conf_ext] + "\n")
                else:
                    f.write(dst_dirs[conf_ext] + " dir does not exist\n")
                    os.mkdir(dst_dirs[conf_ext])
                    f.write(dst_dirs[conf_ext] + " dir is created\n")
                    shutil.move(src_path, dst_path)
                    f.write("File is moved to " + dst_dirs[conf_ext] + "\n")
    f.write("All known files are moved\n")

# move files with the unknown extension to the default directory
def moveToDefaultDir():
    files = Path(source_dir_name).glob('*')
    for file in files: 
        src_path = os.path.join(source_dir_name, os.path.basename(file))
        dst_path = os.path.join(default_dir, os.path.basename(file))
        file_name = os.path.basename(file)
        result = checkDestinationFiles(default_dir, file_name)
        f.write(extensionType(file) + "\n")
        if if_dest_dir_exists(default_dir) and result == False:
            break
        elif if_dest_dir_exists(default_dir) and result != False: 
            print(if_dest_dir_exists(default_dir))
            shutil.move(src_path, dst_path)
            f.write("File is moved in " + default_dir + "\n")
        else:
            f.write(default_dir + " dir does not exist\n")
            os.mkdir(default_dir)
            f.write(default_dir + " dir is created\n")
            shutil.move(src_path, dst_path)
            f.write("File is moved to " + default_dir + "\n")


# determine what is the type of file etension 
def extensionType(file):
    ext = os.path.splitext(file)[-1].lower()   # extension is changed to lowercase string
    return str(ext)

# check if destination directory has file with the same name
def checkDestinationFiles(dst_dir, f_name):
    dst_files = Path(dst_dir).glob('*')
    for dst_file in dst_files:
        dst_file_name = os.path.basename(dst_file)
        if dst_file_name == f_name:
            f.write("File " + f_name + " already exists\n")
            return False
        else:
            return True
       
            
# def fileMovingAnswer():
#     print("File with the same name exists!\n ")
#     text = input("Do you really want to move this file?\n")
#     answer = str(text) 
#     print("Answer: ", answer)
#     yes = "y"
#     if answer == yes:
#         return True
#     else: 
#         return False

# check if source directory is empty
def if_dir_is_empty(dir_name):
    if not os.listdir(dir_name):
        f.write("Source directory is empty\n")
        return False
    else:
        f.write("Something is in source directory\n") 
        return True

# check if source directory exists
def if_dir_exists(dir_name):
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        f.write("Directory exists\n")
        return True
    else:
        f.write("Directory does not exist\n")
        return False

# check if destination directory exists
def if_dest_dir_exists(dest_dir_name):
    if os.path.exists(dest_dir_name) and os.path.isdir(dest_dir_name):
        #f.write(dest_dir_name + " exists\n")
        return True
    else:
        #f.write(dest_dir_name + " does not exist\n")
        return False

# write to logs.txt file
def writeToFile(text):
    f = open("/home/studentas/Documents/Testing/logs.txt", "a")
    f.write(text)
    f.close()

# main function
def main():
   
    result = if_dir_exists(source_dir_name)
    if result:
        not_empty = if_dir_is_empty(source_dir_name)
        if not_empty:
            move_files(source_dir_name)  
    if not_empty:
        moveToDefaultDir()  
        


f = open("/home/studentas/Documents/Testing/logs.txt", "w")
main()


class Watcher:
    DIRECTORY_TO_WATCH = source_dir_name

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            writeToFile("Received created event - %s.\n" % event.src_path)
            move_files(source_dir_name)
            moveToDefaultDir()



if __name__ == '__main__':
    w = Watcher()
    w.run()