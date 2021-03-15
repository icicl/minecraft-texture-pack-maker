path = '../1.8.9_source/assets/minecraft/textures/'
mcmeta='{"pack":{"pack_format":1,"description":"I don\'t like sand."}}'
import os
from PIL import Image

def downscale_function(q):
    r,g,b,a,ac=0,0,0,0,0
    for i in q:
        r+=i[0]
        g+=i[1]
        b+=i[2]
        a+=i[3]
        ac+=i[3]>0
    if ac*2<len(q):return (0,0,0,0)
    return (round(r/len(q)),round(g/len(q)),round(b/len(q)),round(a/len(q)))

def gray(p):
    return round((3*p[0]+6*p[1]+p[2])/10)

def cbits(p,bits,gs):
    if gs:
        g=gray(p)
        g=round(255*(g>>(8-bits))/((1<<(bits))-1))
        a=round(255*(p[3]>>(8-bits))/((1<<(bits))-1))
        return (g,g,g,a)
    r=round(255*(p[0]>>(8-bits))/((1<<(bits))-1))
    g=round(255*(p[1]>>(8-bits))/((1<<(bits))-1))
    b=round(255*(p[2]>>(8-bits))/((1<<(bits))-1))
    a=round(255*(p[3]>>(8-bits))/((1<<(bits))-1))
    return (r,g,b,a)


def none(a):return a
def rescale(im,size,factor,bits,gs):#reduces by 2^factor
    f=2**factor
    io = Image.new('RGBA',size)
    il = io.load()
    for x in range(0,size[0],f):
        for y in range(0,size[1],f):
            q=[]
            for dx in range(f):
                for dy in range(f):
                    q+=[im[x+dx,y+dy]]
            px=cbits(downscale_function(q),bits,gs)
            for dx in range(f):
                for dy in range(f):
                    il[x+dx,y+dy]=px
    return io


folders = ['blocks/','items/']
def pack(scale=0,bits=8,grayscale=False):
    if not grayscale:
        name = str(16//(2**scale))+'x'+str(16//(2**scale))+' - '+str(bits)+'-bit color channels'
    else:
        name = str(16//(2**scale))+'x'+str(16//(2**scale))+' - '+str(bits)+'-bit grayscale'
    print('generating: '+name)
    cd = name+'/'
    try:
        os.mkdir(cd)
        with open(cd+'pack.mcmeta','w+') as f:f.write(mcmeta)
        cd += 'assets/'
        os.mkdir(cd)
        cd += 'minecraft/'
        os.mkdir(cd)
        cd += 'textures/'
        os.mkdir(cd)
    except:
        cd = name+'/assets/minecraft/textures/'
    for f in folders:
        try:
            os.mkdir(cd+f)
        except:
            pass
        for i in os.listdir(path+f):
            if i[-4:]=='.png':### ELSE COPY
#                print(i)
                im=Image.open(path+f+i)
                rescale(im.convert('RGBA').load(),im.size,scale if (f!='items/') else 0,bits,grayscale).save(cd+f+i)
            else:
                with open(path+f+i) as file:dat=file.read()
                with open(cd+f+i,'w+') as file:file.write(dat)

def solid(color,name):
    print('generating: '+name)
    cd = name+'/'
    try:
        os.mkdir(cd)
        with open(cd+'pack.mcmeta','w+') as f:f.write(mcmeta)
        cd += 'assets/'
        os.mkdir(cd)
        cd += 'minecraft/'
        os.mkdir(cd)
        cd += 'textures/'
        os.mkdir(cd)
    except:
        cd = name+'/assets/minecraft/textures/'
    for ff in os.listdir(path):
        f=ff+'/'
        try:
            os.mkdir(cd+f)
        except:
            pass
        for i in os.listdir(path+f):
            if i[-4:]=='.png':
                im=Image.open(path+f+i)
                Image.new('RGBA',im.size,color).save(cd+f+i)
            elif '.' in i:
                with open(path+f+i) as file:dat=file.read()
                with open(cd+f+i,'w+') as file:file.write(dat)
    

solid((255,255,255,255),'blinding_light')
solid((0,0,0,255),'eternal_dark')

for scale in range(5):
    for bits in range(1,9):
        for gs in (True,False):
            pack(scale,bits,gs)

