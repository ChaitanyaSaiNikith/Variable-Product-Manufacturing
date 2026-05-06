from calendar import TUESDAY

from vision_utils import saveImage, loadImage, RESULT_CODES
import vision

# Defines specific image path for
def bulkImagePath(type, num):
    testImage = type + str(num) + ".png"
    testImagePath = "BulkTest/" + testImage
    return testImagePath

# All tests produce the same message
def testMessageHandler(lidType, testNumber, testResult):
    if(not testResult):
        print("Test Number: " + str(testNumber) + " Test In : " + testResult + " None")
    elif(testResult != lidType):
        print("Test Number: " + str(testNumber) + " Test In : " + lidType + " Type mismatch")
        
# Run a test on a single image
# Allows troubleshooting of any failed tests
def individualTest(type, testNumber):
    testImagePath = bulkImagePath(type, testNumber)
    image = loadImage(testImagePath)
    testResult = vision.lidTypeIndicator(image)
    testMessageHandler(type, testNumber, testResult)

# Captures r range of images for known lidType
# Name of file designates number and type for batchtest
def bulkSave(lidType, r):
    for i in range(*r):
        img = vision.scan()
        testImagePath = bulkImagePath(lidType, i)
        saveImage(img, testImagePath)

# Run test in range r for lidType
def bulkTest(lidType, r):
    for i in range(*r):
        testImagePath = bulkImagePath(lidType, i)
        image = loadImage(testImagePath)
        testResult = vision.lidTypeIndicator(image)
        testMessageHandler(lidType, i, testResult)

def main():
    # Used to save bulk images from webcam
    # bulkSave(RESULT_CODES[1], (300,400))

    # bulkTest(RESULT_CODES[1], (1,400))
    # bulkTest(RESULT_CODES[2], (1,400))
    
    # Early testing or trouble shooting individual images
    # Trouble shoot individual
    individualTest(RESULT_CODES[1],13)


if __name__ == "__main__":
    main()