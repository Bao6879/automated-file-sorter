import os
import shutil
import logging
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
with open('D:/CV/Sorter/config.json', 'r') as f:
    config=json.load(f)
cwd=config['watchFolder']
os.chdir(cwd)
logging.basicConfig(filename="work.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileTypes = config['fileTypes']
class OnMyWatch:
    watchDirectory=cwd
    def __init__(self):
        self.observer=Observer()
    def run(self):
        eventHandler=Handler()
        self.observer.schedule(eventHandler, self.watchDirectory, recursive=False)
        self.observer.start()
        print("Started observer")
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def processFile(self, filePath):
        x=os.path.basename(filePath)
        if (x==os.path.basename(__file__)):
            logger.info("Skipping the file itself...")
            return
        if x.startswith('~') or x.endswith('.tmp') or x.endswith('.crdownload') or x.endswith('.part'):
            logger.info(f"Ignoring temporary file: {x}")
            return
        for folders in fileTypes:
            for fileExtension in fileTypes[folders]:
                if (x.endswith(fileExtension)):
                    num=0
                    currentFile=x
                    while (os.path.exists(folders+'/'+currentFile)):
                        newFile='('+str(num)+') '+x
                        currentFile=newFile
                        num+=1
                    shutil.move(x, folders+'/'+currentFile)
                    logger.info('Moved '+x+' to '+folders)
                    break
    def on_moved(self, event):
        destDir = os.path.dirname(event.dest_path)+'/'
        if (destDir.startswith(cwd)):
            relativePath=os.path.relpath(destDir, cwd)
            if (relativePath in fileTypes.keys()):
                logger.info("Ignoring internal move to category folder...")
                return
        if not event.is_directory:
            self.processFile(event.dest_path)
        return super().on_moved(event)
    def on_created(self, event):
        if not event.is_directory:
            self.processFile(event.dest_path)
        return super().on_created(event)

if __name__ == '__main__':
    for folders in fileTypes:
        if (os.path.exists(folders)):
            logger.info('The folder '+folders+' exists, skipping...')
        else:
            os.makedirs(folders, exist_ok=True)
            logger.info('The folder '+folders+' does not exist, created successfully...')
    watch = OnMyWatch()
    watch.run()