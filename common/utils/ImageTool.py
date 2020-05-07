import os, requests
from datetime import datetime
from PIL import Image
from common.utils.StrUtils import StrUtils

class ImageTool:
    def __init__(self):
        super().__init__()

    
    def download(self, scode, userId, url, savePath):
        if url is None:
            return None, None
        filename = (str(int(datetime.now().microsecond / 1000)))+'-'+ url.split('/')[-1]
        path = os.path.join(savePath, scode, userId)
        if os.path.exists(path) == False:
            os.makedirs(path)
        savePath = os.path.join(path, filename)

        r = requests.get(url, allow_redirects=True)
        open(savePath, 'wb').write(r.content)

        return savePath, os.stat(savePath).st_size

    IMAGE_CROP_SIZE = 360
    def cropImageByFullPath(self, scode, userId, srcPath, destPath):
        if StrUtils.isImageFile(srcPath) == False:
            return False
        path = os.path.join(destPath, scode, userId)
        if os.path.exists(path) == False:
            os.makedirs(path)
        filename = srcPath.split('/')[-1]
        destPath = os.path(path, filename)

        im = Image.open(srcPath)
        w, h = im.size

        left = (w - self.IMAGE_CROP_SIZE)/2 if w > self.IMAGE_CROP_SIZE else 0
        right = left + self.IMAGE_CROP_SIZE
        top = (h - self.IMAGE_CROP_SIZE)/2 if h > self.IMAGE_CROP_SIZE else 0
        bottom = top + self.IMAGE_CROP_SIZE

        im1 = im.crop((left, top, right, bottom))
        im1.save(destPath)
        return True

    def cropImageByFilename(self, scode, userId, srcRoot, fileName, destPath):
        srcPath = os.path.join(srcRoot, scode, userId, fileName)
        return self.cropImageByFullPath(scode, userId, srcPath, destPath)