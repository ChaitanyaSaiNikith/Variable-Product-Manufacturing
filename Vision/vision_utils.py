import cv2
from pathlib import Path

# index maps to type
RESULT_CODES = [
    "unknown",
    "tall",
    "short",
]

# Save CV Image in specific file
# Typically for later testing
def saveImage(image, filename):
    current_script_path = Path(__file__).resolve()
    current_dir = current_script_path.parent
    image_path = current_dir / filename
    cv2.imwrite(image_path, image)

# Load specific image
# Great for early testing, debugging, batchtest
def loadImage(imgPath):
    current_script_path = Path(__file__).resolve()
    current_dir = current_script_path.parent
    image_path = current_dir / imgPath
    return cv2.imread(image_path)

# Crop CV to specific dimensions
def crop(image, stat):
    x, y, w, h, area = stat
    return image[y:y+h, x:x+w].copy()

# Draws rectangles and circles on top of image
# Displays 
def drawStuffShowStuff(originalImage, circles, lines):
    colorImage = cv2.cvtColor(originalImage, cv2.COLOR_GRAY2BGR)
    
    #Draw Lines
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv2.line(colorImage, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv2.LINE_AA)
        
    #Draw Circles
    for circle in circles:
        center = (int(circle.pt[0]), int(circle.pt[1]))
        radius = int(circle.size/2)
        cv2.circle(colorImage, center, radius, (0,0,255), 2)
    displayWindow(colorImage, "We Did Drawn")
    saveImage(colorImage, "Holes.png")

# Handles the display of images such that window is resizable
def displayWindow(image, windowName):
    resized_image = cv2.resize(image, image.shape[:2], interpolation=cv2.INTER_AREA)
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.imshow(windowName, resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()