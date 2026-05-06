import math
import cv2
import modbus_server
from vision_utils import crop, RESULT_CODES, drawStuffShowStuff

# Safely Opens camera and captures camera 
def scan():
    camera = None
    image = None

    try:
        camera = cv2.VideoCapture(cv2.CAP_DSHOW)
        if not camera.isOpened():
            print(f"[scan] ERROR: Camera failed to open")
            return None

    except Exception as e:
        print(f"[scan] ERROR: Exception opening camera: {e}")
        if camera is not None:
            camera.release()
        return None

    # Attempts to capture image 3 times
    # Skipping first 30 frames
    for i in range(0,3):
        for i in range(30):
            ret, image = camera.read()
        if(ret): break
    camera.release()

    if image is None:
        print("[scan] ERROR: Failed to capture frame.")
        return None
    return image

# Sets all values less than threshold to black
# https://docs.opencv.org/4.x/d7/dd0/tutorial_js_thresholding.html
def clipBlacks(image):
    clipLevel = 200
    dst = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, dst = cv2.threshold(dst, clipLevel, 255, cv2.THRESH_TOZERO)
    return dst


# Initialize Blob (circle) Detector and returns key data (radius, location, etc)
# https://docs.opencv.org/4.x/d0/d7a/classcv_1_1SimpleBlobDetector.html
def findHoles(image):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 25
    params.maxArea = 1000

    params.filterByCircularity = True
    params.minCircularity = 0.5  # 1.0 = perfect circle, low threshold because of crop

    params.filterByConvexity = False
    params.filterByInertia = False
        
    detector = cv2.SimpleBlobDetector_create(params)
    circles = detector.detect(image)

    return circles 

# Finds largest all white area
#https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga107a78bf7cd25dec05fb4dfc5c9e765f
def findLargestConnected(image):
    # Otsu Binarization (Split into blacks and whites)
    _, mask = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    largestIndex, largestArea = 0, 0
    # skip first index, it's background
    for i in range(1, numLabels):
        x, y, w, h, area = stats[i]
        if(area > largestArea):
            largestIndex, largestArea = i, area

    return stats[largestIndex]

# Find distance between every set of pairs of circle's centerpoints
def calcHoleSpacing(holes):
    l = len(holes)
    distances = []
    for i in range(l):
        for j in range(i+1, l):
            distances.append(math.dist(holes[i].pt , holes[j].pt))
    return distances

# Determines lid type
# Algorithm takes the shortest hole distance  and splits over threshold
def lidTypeByHoles(holeSpacing, indicatorThreshold):
    lidType = RESULT_CODES[0]
    holeSpacing.sort()
    if(len(holeSpacing) == 0): 
        return lidType
    if(holeSpacing[0] < indicatorThreshold):
        lidType = RESULT_CODES[1]
    elif(holeSpacing[0] > indicatorThreshold):
        lidType = RESULT_CODES[2]

    print(holeSpacing[0])
    print(lidType)

    return lidType

# Wrapper for all image processing and indication
def lidTypeIndicator(image):

    #Crop image to just tray (this is clever :)
    clippedImage = clipBlacks(image)

    imageStats = findLargestConnected(clippedImage)
    lidCrop = crop(clippedImage, imageStats)

    # Find Features
    holes = findHoles(lidCrop)
    drawStuffShowStuff(lidCrop, holes, [])

    holeSpacing = calcHoleSpacing(holes)
    lidType = lidTypeByHoles(holeSpacing, 85)

    return lidType

# Captures image, indicates type, calls to send result
def main():
    image = scan()
    
    # Pauses algorithm for human verification
    # Uncomment DrawStuffShowStuff in lidTypeIndicator for algorithm validation
    # displayWindow(image, "Test Camera")

    lidType = lidTypeIndicator(image)
    modbus_server.set_result(lidType)

if __name__ == "__main__":
    main()