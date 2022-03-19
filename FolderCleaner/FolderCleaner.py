import json
import os.path
import shutil
import time


def Cleanup():
    print("Cleanup Started",flush=True);
    config=None
    with open('Cleaner.json') as jsonfile:
        config = json.load(jsonfile)
    print('Config loaded',flush=True)
    now = time.time()
    timeunits= {'Day':1,'Week':7,'Month':30,'Year':365}
    for folderPath in config['FolderPaths']:
        print('Processing '+folderPath['FolderPath']+' for Cleanup',flush=True)
        if not os.path.exists(folderPath['FolderPath']):
            print(folderPath['FolderPath'] + 'doesnt exist, skipping to next entry', flush=True)
            continue
        for fileFolder in os.listdir(folderPath['FolderPath']):

            fullpath = os.path.join(folderPath['FolderPath'],fileFolder)
            createdTime = os.path.getmtime(fullpath)
            allowedTime = now - folderPath['TimePeriod'] * timeunits[folderPath['TimeUnit']] * 86400

            if createdTime < allowedTime :
                try:
                    if os.path.isfile(fullpath):
                        os.remove(fullpath)
                        print('File ' + fileFolder + ' deleted', flush=True);
                    else:
                        shutil.rmtree(fullpath,ignore_errors=False)
                        print('Folder ' + fileFolder + ' deleted', flush=True);
                except:
                    print(fullpath + ' Deletion not succeeded due to errors')
            else:
                print(fileFolder + ' not deleted', flush=True);