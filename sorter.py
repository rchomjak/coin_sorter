import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture("http://192.168.0.52:4747/mjpegfeed?960x720")

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
    print("Fail")

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()


#main loop
while True:

    # get coin - move belt until coin ni picture

    # scan coin

    # move to right container
    # |0.10|0.20|0.50|1|2|5|


    # drop coin

    pass