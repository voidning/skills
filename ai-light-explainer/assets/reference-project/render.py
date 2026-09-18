"""Jev 是啥？ Editable 47-second Chinese motion graphic and 3:4 cover.
All visuals and sounds are generated locally. All model outputs are illustrative.
"""
from pathlib import Path
from functools import lru_cache
import argparse, math, os, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

W,H,FPS,DURATION = 1080,1920,30,47
BG,INK,MUTED,LINE = '#F7F5EF','#302F2B','#75736C','#B6B2A9'
ORANGE,PALE,WHITE = '#C66B4E','#EEDDD2','#FCFBF7'
CN=os.environ.get('AI_EXPLAINER_CN_FONT','/System/Library/Fonts/PingFang.ttc')
CN_BOLD=os.environ.get('AI_EXPLAINER_CN_BOLD_FONT',CN)
MONO=os.environ.get('AI_EXPLAINER_MONO_FONT','/System/Library/Fonts/SFNSMono.ttf')
REPLY=['想吃点北京味儿，','可以考虑炸酱面。','烤鸭、涮肉也不错，','不过得看看预算和时间。']
TYPE_START,CHAR_INTERVAL=4.4,.135
PROBS=[.10,.78,.12]
CUTS=[3,14,25,39,43]

@lru_cache(None)
def font(size,mono=False,bold=False):
    path=MONO if mono else (CN_BOLD if bold else CN)
    if not Path(path).is_file():
        raise FileNotFoundError('Font unavailable. Set AI_EXPLAINER_CN_FONT, AI_EXPLAINER_CN_BOLD_FONT and AI_EXPLAINER_MONO_FONT to installed fonts. Missing: '+path)
    pingfang=not mono and Path(path).name=='PingFang.ttc'
    return ImageFont.truetype(path,size,index=(8 if bold else 2) if pingfang else 0)

def tx(d,x,y,s,size=40,color=INK,mono=False,bold=False):
    d.text((x,y),s,font=font(size,mono,bold),fill=color,anchor='lt')

def center(d,x,y,s,size=40,color=INK,mono=False,bold=False):
    tw=d.textlength(s,font=font(size,mono,bold))
    tx(d,x-tw/2,y,s,size,color,mono,bold)

def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)

def mix(a,b,v): return a+(b-a)*ease(v)

def arrow(d,x,y,length=60):
    d.line((x,y,x,y+length),fill=ORANGE,width=3)
    d.line((x-10,y+length-11,x,y+length,x+10,y+length-11),fill=ORANGE,width=3)

def window(d,box,label,tag='',small=False):
    x,y,r,b=box; hh=52 if small else 62
    d.rounded_rectangle(box,radius=5,fill=WHITE,outline=INK,width=2)
    d.line((x,y+hh,r,y+hh),fill=LINE,width=2)
    for i in range(3):
        d.ellipse((x+20+i*18,y+hh/2-3,x+26+i*18,y+hh/2+3),fill=ORANGE if i==0 else LINE)
    tx(d,x+95,y+17,label,22 if small else 24,mono=True)
    if tag:
        tw=d.textlength(tag,font=font(22,True))
        tx(d,r-tw-20,y+18,tag,22,MUTED,True)

def base(chapter):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    tx(d,84,173,'AI 工作原理',29)
    tx(d,785,175,f'{chapter:02d} / 04',24,MUTED,True)
    d.line((84,234,934,234),fill=LINE,width=2)
    for i,label in enumerate(['生成','决策','行动','用途']):
        x=84+i*215
        d.line((x,1615,x+176,1615),fill=ORANGE if i==chapter-1 else LINE,width=5 if i==chapter-1 else 2)
        tx(d,x,1640,f'0{i+1}',23,ORANGE if i==chapter-1 else MUTED,True)
        tx(d,x+48,1637,label,26,INK if i==chapter-1 else MUTED)
    tx(d,84,1710,'LLM / JEV',23,MUTED,True)
    tx(d,485,1708,'概念演示 · 非实际模型输出',26,MUTED)
    return im,d

def heading(d,n,en,line1,line2=None):
    tx(d,84,307,f'0{n} / {en}',25,ORANGE,True)
    tx(d,80,394,line1,70,bold=True)
    if line2:tx(d,80,493,line2,70,bold=True)

def request(d,y=662):
    window(d,(84,y,934,y+246),'YOUR APP','INPUT')
    tx(d,119,y+98,'北京有啥好吃的？',50,bold=True)
    tx(d,119,y+176,'预算 50，想快点吃完。',33,MUTED)

def intro(t):
    im,d=base(1)
    tx(d,84,315,'先从一个日常问题说起',30,MUTED)
    off=round(14*(1-ease(t/.5)))
    tx(d,80,412+off,'北京有啥',90,bold=True)
    tx(d,80,532+off,'好吃的？',106,ORANGE,bold=True)
    # Expand a real window rather than fade the whole page.
    p=ease((t-.3)/.55)
    if p>0:
        layer=Image.new('RGB',(W,H),BG);ld=ImageDraw.Draw(layer)
        request(ld,859)
        region=(74,849,944,1115)
        im.paste(Image.blend(im.crop(region),layer.crop(region),p),(74,849))
        d=ImageDraw.Draw(im)
    if t>.95:
        arrow(d,510,1140,70)
        center(d,510,1260,'同一个问题',42)
        center(d,510,1327,'看看两种处理方式',42,ORANGE,bold=True)
    return im

def llm(t):
    im,d=base(1)
    heading(d,1,'TEXT GENERATION','问 LLM，','它可以展开聊。')
    request(d)
    arrow(d,510,930,60)
    window(d,(84,1011,934,1410),'LLM','OUTPUT')
    count=max(0,int((t-TYPE_START)/CHAR_INTERVAL))
    left=count;cx,cy=119,1114
    for i,line in enumerate(REPLY):
        shown=line[:max(0,left)]
        tx(d,119,1114+i*64,shown,42)
        cx=119+d.textlength(shown,font=font(42));cy=1114+i*64
        if left<=len(line):break
        left-=len(line)
    total=sum(map(len,REPLY))
    if count<total or int(t*2)%2==0:
        d.rectangle((cx+7,cy,cx+23,cy+42),fill=ORANGE)
    tx(d,84,1472,'它会生成一段回答。',38)
    tx(d,84,1530,'画面按字展示；模型通常逐个生成 token。',26,MUTED)
    return im

def jev(t):
    im,d=base(2)
    heading(d,2,'TYPED DECISIONS','Jev 这边，','要先把选项给它。')
    request(d)
    arrow(d,510,930,60)
    window(d,(84,1011,934,1420),'JEV','OPTIONS')
    tx(d,119,1097,'我们预先提供的选项',27,MUTED)
    p=ease((t-16.7)/.95)
    for i,(label,value) in enumerate(zip(['烤鸭','炸酱面','涮肉'],PROBS)):
        y=1160+i*76
        chosen=i==1 and t>18.0
        d.rounded_rectangle((115,y-9,304,y+50),radius=3,fill=PALE if chosen else WHITE,outline=ORANGE if chosen else LINE,width=2)
        tx(d,134,y+3,label,34,ORANGE if chosen else INK,bold=chosen)
        d.rectangle((340,y+11,769,y+30),fill='#E8E5DD')
        if p>0:d.rectangle((340,y+11,340+429*value*p,y+30),fill=ORANGE if i==1 else INK)
        tx(d,804,y,f'{round(value*p*100):02d}%' if p>0 else '—',30,ORANGE if chosen else MUTED,True)
    if t<20.4:
        tx(d,84,1472,'各个选项的概率，一起返回。',38)
    else:
        tx(d,84,1472,'程序可以拿这些结果，接着往下做。',36)
    tx(d,84,1530,'LLM 也能做选择；这里对比输出机制。',28,MUTED)
    return im

def pixel(d,cx,cy,color=ORANGE,enemy=False):
    x,y=round(cx),round(cy)
    d.rectangle((x-23,y-24,x+23,y+22),fill=color,outline=INK,width=2)
    d.rectangle((x-15,y-5,x-8,y+2),fill=INK)
    d.rectangle((x+7,y-5,x+14,y+2),fill=INK)
    if enemy:d.line((x-9,y+12,x+9,y+12),fill=INK,width=2)
    else:
        d.rectangle((x-21,y+22,x-10,y+30),fill=INK)
        d.rectangle((x+10,y+22,x+21,y+30),fill=INK)

def game_state(t):
    # A pre-authored concept animation, not a model-controlled game.
    if t<26.5:return 510,995,-1
    if t<28.7:return mix(510,380,(t-26.7)/1.1),995,0
    if t<30.9:return mix(380,620,(t-28.9)/1.25),995,1
    if t<33.2:return 620,mix(995,905,(t-31.1)/1.3),2
    if t<35.6:return 620,905,3
    return 620,mix(905,753,(t-35.8)/2.0),2

def game(t):
    im,d=base(3)
    heading(d,3,'DECISION LOOP','放进游戏里，','就好理解了。')
    window(d,(84,651,934,1127),'GAME STATE','DEMO')
    # Top-down room. Forward points up, left/right use screen coordinates.
    for x in range(126,924,44):d.line((x,730,x,1104),fill='#ECE9E2',width=1)
    for y in range(730,1120,44):d.line((106,y,911,y),fill='#ECE9E2',width=1)
    d.rectangle((126,744,239,792),fill=PALE,outline=LINE,width=2)
    d.rectangle((755,913,890,961),fill=PALE,outline=LINE,width=2)
    d.rectangle((577,730,663,770),fill=INK)
    tx(d,581,736,'EXIT',24,WHITE,True)
    for x,y in [(310,876),(835,805)]:
        d.polygon([(x,y-7),(x+7,y),(x,y+7),(x-7,y)],fill=ORANGE)
    x,y,action=game_state(t)
    # Enemy and projectile have one continuous, visible collision.
    shot=ease((t-33.65)/.65)
    if t<34.3:pixel(d,620,824,PALE,True)
    if 33.65<=t<34.3:
        sy=879+(844-879)*shot
        d.rectangle((616,sy-10,624,sy+5),fill=ORANGE)
    if 34.3<=t<34.65:
        r=10+40*((t-34.3)/.35)
        for a in [0,math.pi/2,math.pi,math.pi*1.5]:
            xx,yy=620+math.cos(a)*r,824+math.sin(a)*r
            d.rectangle((xx-4,yy-4,xx+4,yy+4),fill=ORANGE)
    if t<38.0:pixel(d,x,y)
    else:center(d,510,909,'这一轮，完成。',43,ORANGE,bold=True)
    tx(d,84,1171,'预先给定的动作',28,MUTED)
    labels=['向左','向右','前进','射击']
    for i,label in enumerate(labels):
        xx=84+i*215;active=i==action and t<38
        d.rounded_rectangle((xx,1220,xx+176,1303),radius=4,fill=PALE if active else WHITE,outline=ORANGE if active else LINE,width=3 if active else 2)
        center(d,xx+88,1242,label,34,ORANGE if active else INK,bold=active)
    tx(d,84,1384,'这一刻，该往哪走？' if t<31 else '它给出判断，程序执行动作。',40)
    tx(d,84,1472,'当前状态',30,MUTED)
    tx(d,288,1472,'→',30,ORANGE)
    tx(d,355,1472,'Jev 决策',30,MUTED)
    tx(d,565,1472,'→',30,ORANGE)
    tx(d,632,1472,'程序执行',30,MUTED)
    tx(d,84,1530,'状态以数据传入；不是让模型直接看画面。',27,MUTED)
    return im

def summary(t):
    im,d=base(4)
    heading(d,4,'WHERE IT FITS','这类具体决策，','就是它的用武之地。')
    labels=[('分类','归到哪一类'),('评分','按标准打分'),('路由','交给谁处理'),('选动作','下一步做什么')]
    for i,(label,desc) in enumerate(labels):
        x=84+i%2*439;y=726+i//2*246
        off=round(10*(1-ease((t-39-i*.1)/.35)))
        d.rounded_rectangle((x,y+off,x+411,y+208+off),radius=5,fill=WHITE,outline=LINE,width=2)
        tx(d,x+28,y+30+off,label,50,ORANGE,bold=True)
        tx(d,x+28,y+121+off,desc,32)
    tx(d,84,1333,'不提供自由文本生成。',36)
    tx(d,84,1401,'判断也可能出错，结果仍要验证。',32,MUTED)
    return im

def end(t):
    im,d=base(4)
    tx(d,84,316,'把问题留给你',29,MUTED)
    tx(d,78,538,'你觉得 Jev',86,bold=True)
    tx(d,78,661,'能用来干啥？',86,ORANGE,bold=True)
    d.line((84,826,256,826),fill=ORANGE,width=5)
    # A quiet open comment field reinforces the question without an extra CTA.
    window(d,(84,1024,934,1238),'YOUR IDEA','?')
    tx(d,122,1137,'一个你想到的用途',37,MUTED)
    if int(t*2)%2==0:d.rectangle((478,1134,493,1176),fill=ORANGE)
    tx(d,84,1436,'资料：TypeSafe 官方文档',27,MUTED)
    tx(d,84,1485,'docs.typesafe.ai',26,MUTED,True)
    return im

SCENES=[intro,llm,jev,game,summary,end]
def frame(t):
    ix=sum(t>=cut for cut in CUTS)
    for i,cut in enumerate(CUTS):
        if cut<=t<cut+.24:
            return Image.blend(SCENES[i](cut-.001),SCENES[i+1](t),ease((t-cut)/.24))
    return SCENES[ix](t)

def cover():
    im=Image.new('RGB',(1080,1440),BG);d=ImageDraw.Draw(im)
    tx(d,84,85,'AI 工作原理',28)
    tx(d,829,88,'01',24,MUTED,True)
    d.line((84,144,996,144),fill=LINE,width=2)
    tx(d,79,211,'外网爆火的',66,bold=True)
    tx(d,72,316,'Jev 是啥？',130,ORANGE,bold=True)
    tx(d,84,498,'一个动画，看懂它和 LLM 的区别',39)
    window(d,(84,615,996,799),'YOUR APP','INPUT')
    center(d,540,717,'北京有啥好吃的？',47,bold=True)
    d.line((540,799,540,846,307,846,307,890),fill=ORANGE,width=3)
    d.line((540,846,773,846,773,890),fill=ORANGE,width=3)
    window(d,(84,891,531,1239),'LLM',small=True)
    window(d,(561,891,996,1239),'JEV',small=True)
    tx(d,113,982,'想吃点北京味儿，',30)
    tx(d,113,1039,'可以考虑炸酱面。',30)
    tx(d,113,1096,'烤鸭、涮肉也不错…',29)
    d.rectangle((114,1161,383,1174),fill='#D6D2C8')
    d.rectangle((394,1155,406,1180),fill=ORANGE)
    for i,(s,p) in enumerate(zip(['烤鸭','炸酱面','涮肉'],PROBS)):
        y=983+i*72
        tx(d,584,y,s,28,ORANGE if i==1 else INK,bold=i==1)
        d.rectangle((701,y+7,917,y+21),fill='#E8E5DD')
        d.rectangle((701,y+7,701+216*p,y+21),fill=ORANGE if i==1 else INK)
    tx(d,584,1190,'预设选项 · 概率示意',23,MUTED)
    tx(d,84,1295,'生成文本',30,MUTED)
    tx(d,562,1295,'返回结构化结果',30,MUTED)
    tx(d,84,1370,'概念演示，非实际模型输出',23,MUTED)
    return im

def sound(path):
    sr=48000;audio=np.zeros((sr*DURATION,2),dtype=np.float64);rng=np.random.default_rng(41)
    def event(at,kind='select'):
        duration=.026 if kind=='key' else .12
        n=round(sr*duration);tt=np.arange(n)/sr
        if kind=='key':
            env=np.exp(-tt*155)*np.minimum(tt/.0015,1)
            v=(rng.normal(0,1,n)*.22+np.sin(tt*2*np.pi*1350)*.3)*env*.12
        elif kind=='shot':
            env=np.exp(-tt*45)*np.minimum(tt/.002,1)
            v=(rng.normal(0,1,n)*.1+np.sin(2*np.pi*(500*tt-1400*tt*tt))*.12)*env
        else:
            env=np.sin(np.pi*tt/duration)**2
            v=np.sin(2*np.pi*(660*tt-850*tt*tt))*.06*env
        a=round(at*sr);b=min(len(audio),a+n)
        audio[a:b,0]+=v[:b-a]*.95;audio[a:b,1]+=v[:b-a]
    for at in [.36,3.08,14.08,16.72,18.02,25.08,26.5,28.7,30.9,33.2,35.6,39.08,43.08]:event(at)
    event(33.65,'shot');event(34.3)
    for i in range(sum(map(len,REPLY))):event(TYPE_START+(i+1)*CHAR_INTERVAL,'key')
    with wave.open(str(path),'wb') as wf:
        wf.setnchannels(2);wf.setsampwidth(2);wf.setframerate(sr)
        wf.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path,default=Path.cwd()/'rendered')
    ap.add_argument('--stills',type=Path)
    ap.add_argument('--stills-only',action='store_true')
    args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    cover().save(args.output_dir/'jev-cover.png')
    if args.stills:
        args.stills.mkdir(parents=True,exist_ok=True)
        for t in [1.8,11.5,19.5,24,27.7,29.9,32.6,33.9,34.45,37,40.5,45]:
            frame(t).save(args.stills/f'{t:05.1f}s.png')
    if args.stills_only:return
    output=args.output_dir/'jev-explained-v1.mp4'
    with tempfile.TemporaryDirectory() as tmp:
        wav=Path(tmp)/'sfx.wav';sound(wav)
        cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y',
             '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
             '-i',str(wav),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
             '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',str(DURATION),str(output)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        for n in range(FPS*DURATION):
            proc.stdin.write(frame(n/FPS).tobytes())
            if n%(FPS*10)==0:print(f'rendered {n//FPS}s / {DURATION}s',flush=True)
        proc.stdin.close();err=proc.stderr.read().decode()
        if proc.wait()!=0:raise RuntimeError(err)
    print(output.resolve())

if __name__=='__main__':main()
