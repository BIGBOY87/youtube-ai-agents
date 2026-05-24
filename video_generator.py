
import os, math, time, tempfile
import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

def _font(size):
    try: return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except Exception: return ImageFont.load_default()

def _center(draw, text, y, font, fill):
    box=draw.textbbox((0,0), text, font=font); w=box[2]-box[0]
    draw.text(((1280-w)//2,y), text, font=font, fill=fill)

def generate_visualizer_video(title, genre="Tech House", seconds=20, output_path=None):
    seconds=max(5,min(int(seconds),60))
    if output_path is None:
        safe="".join(c for c in title if c.isalnum() or c in (" ","_","-")).strip().replace(" ","_")[:40]
        output_path=os.path.join(tempfile.gettempdir(),f"bangitup_{safe}_{int(time.time())}.mp4")
    fps=24
    writer=imageio.get_writer(output_path,fps=fps,codec="libx264",quality=8,macro_block_size=16)
    ft=_font(52); fs=_font(28); fsmall=_font(22)
    for i in range(seconds*fps):
        t=i/fps
        img=Image.new("RGB",(1280,720),(5,5,14)); d=ImageDraw.Draw(img)
        for x in range(0,1280,80): d.line((x,0,x,720),fill=(30,int(45+25*math.sin(t*2+x/100)),80),width=1)
        for y in range(0,720,80): d.line((0,y,1280,y),fill=(20,int(45+25*math.sin(t*2+y/80)),90),width=1)
        for b in range(48):
            x=120+b*22; h=int(40+180*abs(math.sin(t*3.2+b*.55)))
            d.rounded_rectangle((x,560-h,x+12,560),radius=6,fill=(140,40,240))
        r=int(160+40*math.sin(t*1.5))
        d.ellipse((640-r,280-r,640+r,280+r),outline=(100,20,220),width=5)
        d.ellipse((640-r//2,280-r//2,640+r//2,280+r//2),outline=(0,210,255),width=3)
        _center(d,"BANG IT UP MUSIC",90,fsmall,(0,220,255))
        _center(d,title[:58],155,ft,(245,245,255))
        _center(d,f"Dark {genre} Visualizer",230,fs,(190,170,255))
        _center(d,"AI GENERATED PROMO VIDEO",620,fsmall,(180,180,210))
        writer.append_data(np.array(img))
    writer.close()
    return output_path
