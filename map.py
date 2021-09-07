from PIL import Image,ImageDraw
import matplotlib.pyplot as plt
if __name__=='__main__':

    img=Image.open('Images/campusCapture.png')
    image=img.resize((2200,900),Image.HAMMING)
    step_count=100
    draw=ImageDraw.Draw(image)
    y_start=0
    y_end=image.height
    step_size=int(image.width/step_count)
    for x in range(0, image.width, step_size):
        line=((x,y_start),(x,y_end))
        draw.line(line,fill=128)

    x_start=0
    x_end=image.width
    
    for y in range(0, image.height,step_size):
        line=((x_start,y),(x_end,y))
        draw.line(line,fill=128)

    del draw
    
    
    image.save('campusCapturefixed.png')