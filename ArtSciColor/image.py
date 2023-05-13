
import cv2

def resizeCV2Image(
        img, resizeToFraction, 
        interpolation=cv2.INTER_AREA
    ):
    # Rescale image -----------------------------------------------------------
    (width, height) = (
        int(img.shape[1]*resizeToFraction), 
        int(img.shape[0]*resizeToFraction)
    )
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=interpolation)
    return resized


def readCV2Image(
        imgPath, scaleFactor=1, interpolation=cv2.INTER_AREA
    ):
    bgr = cv2.imread(imgPath)
    img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return img