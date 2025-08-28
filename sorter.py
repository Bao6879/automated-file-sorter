import os
import shutil
import logging
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
with open('config.json', 'r') as f:
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
    def on_created(self, event):
        if not event.is_directory:
            x=os.path.basename(event.src_path)
            if (x==os.path.basename(__file__)):
                logger.info("Skipping the file itself...")
                return
            for folders in fileTypes:
                for fileExtension in fileTypes[folders]:
                    if (x.endswith(fileExtension)):
                        num=0
                        currentFile=x
                        while (os.path.exists(folders+'/'+currentFile)):
                            newFile='('+str(num)+') '+x
                            renameSuccessful=False
                            retries=5
                            waitTime=1

                            while (not renameSuccessful and retries>0):
                                try:
                                    os.rename(currentFile, newFile)
                                    renameSuccessful=True
                                except PermissionError:
                                    logger.warning(currentFile+' is locked, retrying in '+str(waitTime)+'s...')
                                    retries-=1
                                    time.sleep(waitTime)
                            if (not renameSuccessful):
                                logger.error('Failed to rename '+currentFile+' after multiple attempts, skipping file...')
                                break
                            logger.info('Found a duplicate in the '+folders+', renaming '+currentFile+' to '+newFile+'...')
                            currentFile=newFile
                            num+=1
                        moveSuccessful=False
                        retries=5
                        waitTime=1
                        while (not moveSuccessful and retries>0):
                            try:
                                shutil.move(currentFile, folders)
                                moveSuccessful=True
                            except PermissionError:
                                logger.warning(currentFile+' is locked for moving, retrying in '+str(waitTime)+'s...')
                                retries-=1
                                time.sleep(waitTime)
                        if (not moveSuccessful):
                            logger.error('Failed to move '+currentFile+' after multiple attempts, skipping file...')
                            break
                        logger.info('Moved '+currentFile+' to '+folders)
                        break
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