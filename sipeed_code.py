'''
Python code running on Sipeed Maix Bit camera
Performs the inference, measures runtime and fps
Software License Agreement (MIT License)
Copyright (c) 2020, Amirhossein Pakdaman.
'''
import sensor, image, lcd, time
import KPU as kpu
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
lcd.clear()
lcd.draw_string(100,96,"MobileNet Demo")
lcd.draw_string(100,112,"Loading labels...")
f=open('labels.txt','r')
labels=f.readlines()
f.close()
task = kpu.load(0x200000) 
info = kpu.netinfo(task)
print(info)
clock = time.clock()
while(True):
    img = sensor.snapshot()
    clock.tick()
    t1 = time.ticks_us()
    fmap = kpu.forward(task, img)
    t2 = time.ticks_diff(time.ticks_us(), t1) /1000
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist)	
    max_index=plist.index(pmax)	
    a = lcd.display(img, oft=(0,0))
    lcd.draw_string(0, 224, "%.2f:%s                            "%(pmax, labels[max_index].strip()))
    lcd.draw_string(0, 128, "%.4f fps                           "%(fps))
    lcd.draw_string(0, 144, "%.4f ms                           "%(t2))
    # print(fps)
a = kpu.deinit(task)
