import cv2

def drawsafelines(image_np,Orientation,Line_Perc1,Line_Perc2):
    
    posii=int(image_np.shape[1]-(image_np.shape[1]/3))
    cv2.putText(image_np,'Blue Line : Machine Border Line',
                        (posii,30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(image_np, 'Red Line : Safety Border Line',
                        (posii,50),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    if(Orientation=="bt"):
        
        Line_Position1=int(image_np.shape[0]*(Line_Perc1/100))
        
        Line_Position2=int(image_np.shape[0]*(Line_Perc2/100))
        
        cv2.line(img=image_np, pt1=(0, Line_Position1), pt2=(image_np.shape[1], Line_Position1), color=(0, 0, 255), thickness=2, lineType=8, shift=0)
                
        cv2.line(img=image_np, pt1=(0, Line_Position2), pt2=(image_np.shape[1], Line_Position2), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
        
        return Line_Position2;
        
    elif(Orientation=="tb"):
       
        Line_Position1=int(image_np.shape[0]-(image_np.shape[0]*(Line_Perc1/100)))
        
        Line_Position2=int(image_np.shape[0]-(image_np.shape[0]*(Line_Perc2/100)))
        
        cv2.line(img=image_np, pt1=(0, Line_Position1), pt2=(image_np.shape[1], Line_Position1), color=(0, 0, 255), thickness=2, lineType=8, shift=0)
                 
        cv2.line(img=image_np, pt1=(0, Line_Position2), pt2=(image_np.shape[1], Line_Position2), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
        
        return Line_Position2;
    
    elif(Orientation=="lr"):
        
        
        Line_Position1=int(image_np.shape[1]-(image_np.shape[1]*(Line_Perc1/100)))
        
        Line_Position2=int(image_np.shape[1]-(image_np.shape[1]*(Line_Perc2/100)))
        
        cv2.line(img=image_np, pt1=(Line_Position1, 0), pt2=(Line_Position1,image_np.shape[0]), color=(0, 0, 255), thickness=2, lineType=8, shift=0)
                
        cv2.line(img=image_np, pt1=(Line_Position2, 0), pt2=(Line_Position2,image_np.shape[0]), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
           
        return Line_Position2;
        
        
    elif(Orientation=="rl"):
        
        Line_Position1=int(image_np.shape[1]*(Line_Perc1/100))
        
        Line_Position2=int(image_np.shape[1]*(Line_Perc2/100))
        
        cv2.line(img=image_np, pt1=(Line_Position1, 0), pt2=(Line_Position1,image_np.shape[0]), color=(0, 0, 255), thickness=2, lineType=8, shift=0)
                
        cv2.line(img=image_np, pt1=(Line_Position2, 0), pt2=(Line_Position2,image_np.shape[0]), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
        
        return Line_Position2;
