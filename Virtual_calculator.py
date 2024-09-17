import cv2
import hand_tracking as ht

class Button():
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
        cv2.putText(img,self.value,(self.pos[0]+40,self.pos[1]+60),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)

    def checkClick(self,x,y):
        if self.pos[0] < x < self.pos[0]+self.width and self.pos[1] < y < self.pos[1]+self.height:
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(250,250,250),cv2.FILLED)
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
            cv2.putText(img,self.value,(self.pos[0]+20,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),2)

            return self.value
        

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = ht.HandDetector(detectionCon=0.8,maxHands=1)

buttonsValues = [["1","2","3","+"],
                 ["4","5","6","-"],
                 ["7","8","9","*"],
                 ["C","0","=","/"]]
buttons = []

for i in range(4):
    for y in range(4):
        xpos = 800 + i*100
        ypos = 150 + y*100
        buttons.append(Button((xpos,ypos),100,100,buttonsValues[y][i]))

equation = ""
delaycounter = 0


while True:
    success,img = cap.read()
    img = cv2.flip(img,1)

    # detecting the hand
    img,hand = detector.findHands(img)

    # draw all the buttons 
    cv2.rectangle(img,(800,50),(800+400,70+100),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(800,50),(800+400,70+100),(50,50,50),3) #border

    for button in buttons:
        button.draw(img)
    
    # check if the hand is detected
    if hand:
        lmList = detector.findPosition(img,draw=False)
        length = detector.findDistance(lmList[8],lmList[12],img)
        print(length)
        _,x,y = lmList[8]
        if length < 30:

            # check witch button is clicked
            for button in buttons:
                value = button.checkClick(x,y)
                if value and delaycounter == 0:
                    if value == '=':
                        equation = equation + "=" + str(eval(equation))
                    if value == "C":
                        equation = ""
                    else:
                        equation += value
                    delaycounter += 1
            
        
        # solve the duplicated value 
        if delaycounter > 10:
            delaycounter = 0
        else:
            delaycounter += 1

    # display the result
    cv2.putText(img,equation,(810,120),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)

    # display the image 
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

