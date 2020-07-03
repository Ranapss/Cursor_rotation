import serial.tools.list_ports
import serial

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)


ser = serial.Serial('COM3', 921600,timeout=1,write_timeout=1)

axes = [1,2,3,4,5,6]
counter = 0 



x = 0
start = 1+(x*4)
end = start + 4
bias = [8255, 8245, 8253, 8061, 8369, 8154]
sensitivity = [32.590,32.590,33.700,1635.000,1629.500,1633.500]
fixed = [1,2,3,4,5,6]
ser.write(b'R')
reading = ser.readline()
print(reading)

# ser.write(b'S')
# while True: #for x in range(10):
    
#     #print(rl.readline())
#     #ser.write(b's')


#     reading = ser.readline()

#     if len(reading) != 27 or str(reading)[-3:-1] != '\\n':
#         reading = ser.readline()

#     for x in range(6):
#         axes[x]=int(reading[1+(x*4):(1+(x*4))+4],16)
#         fixed[x] = round((axes[x]-bias[x])/sensitivity[x],3)
#     print(fixed)
#     #print(axes)
 


""" 
import serial.tools.list_ports
import serial

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

ser = serial.Serial('COM3', 921600,timeout=1,write_timeout=1)
rl = ReadLine(ser)

while True:

    print(rl.readline()) """