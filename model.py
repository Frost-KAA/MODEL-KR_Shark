import numpy as np


class Model:
    # loading and parsing spritesheets
    def __init__(self, r, alpha, is_moving):
        if is_moving:
            self.Shark = Shark(r, alpha, 6)
        else:
            self.Shark = Shark(r, alpha, 0)

        dt = 0.01
        self.t_min = 60.0
        self.idx = 0
        for b in range(0, 180):
            harp = Harpoon(b)
            idx = 0
            for i in np.arange(0.01, 10, dt): 
                if (np.abs(self.Shark.X[idx]-harp.X[idx]) < 0.2) and (np.abs(self.Shark.H-harp.Y[idx]) < 0.1):
                    if (i < self.t_min):
                        self.idx = idx
                        self.Harpoon = harp
                idx += 1
        if (self.idx != 0):
            self.Harpoon.Y = np.array(self.Harpoon.Y)    
            self.Harpoon.Y = self.Harpoon.Y[self.Harpoon.Y >= min(0, self.Shark.H-0.5)]
            self.Harpoon.Y = self.Harpoon.Y.tolist()
            idx = len(self.Harpoon.Y)
            self.Harpoon.X = self.Harpoon.X[:idx]
            self.Harpoon.Vx = self.Harpoon.Vx[:idx]
            self.Harpoon.Vy = self.Harpoon.Vy[:idx]
            self.Shark.V = self.Shark.V [:idx]
            self.Shark.X = self.Shark.X[:idx]
            self.Shark.Y = self.Shark.Y[:idx]
            self.b_res = self.Harpoon.B + self.Shark.A - 90
            self.h_res = self.Shark.R *  np.tan(self.b_res*2*np.pi/360)
            
    def table(self):
        cnt_all = len(self.Harpoon.X)
        self.data = []
        cnt = len(self.Harpoon.X[:self.idx])
        kol = 9
        h = cnt // kol
        self.heading = [round(0.01+i*0.01,2) for i in range(0, self.idx, h)]
        self.heading.append(round(0.01+self.idx*0.01,2))
        self.heading = [str(x) for x in self.heading]
        self.heading.insert(0, "Время, с")
        # 1 row
        list = self.Shark.V[:self.idx:h] 
        list.append(self.Shark.V[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Скорость акулы, м/с")
        self.data.append(list)
        # 2 row
        list = np.sqrt( np.power(self.Harpoon.Vx[:self.idx:h], 2) + np.power(self.Harpoon.Vy[:self.idx:h], 2) )
        list = list.tolist()
        list.append( np.sqrt(self.Harpoon.Vx[self.idx]**2 +  self.Harpoon.Vy[self.idx]**2) )
        list = [round(x,2) for x in list]
        list.insert(0, "Скорость гарпуна, м/с")
        self.data.append(list)
        # 3 row
        list = self.Harpoon.Vx[:self.idx:h] 
        list.append(self.Harpoon.Vx[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Скорость гарпуна по оси X, м/с")
        self.data.append(list)
        # 4 row
        list = self.Harpoon.Vy[:self.idx:h] 
        list.append(self.Harpoon.Vy[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Скорость гарпуна по оси Y, м/с")
        self.data.append(list)
        # 5 row
        list = self.Shark.X[:self.idx:h] 
        list.append(self.Shark.X[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Координата акулы по оси X, м")
        self.data.append(list)
        # 6 row
        list = self.Harpoon.X[:self.idx:h] 
        list.append(self.Harpoon.X[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Координата гарпуна по оси X, м")
        self.data.append(list)
        # 7 row
        list = self.Shark.Y[:self.idx:h] 
        list.append(self.Shark.Y[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Координата акулы по оси Y, м")
        self.data.append(list)
        # 8 row
        list = self.Harpoon.Y[:self.idx:h] 
        list.append(self.Harpoon.Y[self.idx])
        list = [round(x,2) for x in list]
        list.insert(0, "Координата гарпуна по оси Y, м")
        self.data.append(list)
        # 9 row
        X0 = np.array(self.Shark.X[:self.idx:h]) - np.array(self.Harpoon.X[:self.idx:h])
        Y0 = np.array(self.Shark.Y[:self.idx:h]) - np.array(self.Harpoon.Y[:self.idx:h])
        X0 = X0**2
        Y0 = Y0**2
        list = np.sqrt(X0 + Y0)
        list = list.tolist()
        X0 = self.Shark.X[self.idx] - self.Harpoon.X[self.idx]
        Y0 = self.Shark.Y[self.idx] - self.Harpoon.Y[self.idx]
        list.append(np.sqrt(X0**2+Y0**2))
        list = [round(x,2) for x in list]
        list.append(round(0.01+self.idx*0.01,2))
        list.insert(0, "Расстояние от акулы до гарпуна, м")
        self.data.append(list)
        
    
class Shark:
    def __init__(self, r, alpha, V):
        self.R = r
        self.A = alpha
        self.H = r / np.tan(alpha*2*np.pi/360)
        self.V0 = V
        #движение
        Sx_shark = self.R
        dt = 0.01
        self.X = []
        self.V = []
        self.Y = []
        for i in np.arange(0.01, 10, dt):
            self.V.append(self.V0)
            Sx_shark = Sx_shark - self.V0 * dt
            self.X.append(Sx_shark)
            self.Y.append(self.H)
        
class Harpoon:
    def __init__(self, b):
        self.B = b
        V0 = 25
        m = 0.5
        k1 = 0.02
        k2 = 0.000035
        g = 9.8
        dt = 0.01
        Vx = V0 * np.sin(b*2*np.pi/360)
        Vy = V0 * np.cos(b*2*np.pi/360)
        Sx = 0
        Sy = 0  
        self.X = []
        self.Y = []
        self.Vx = []
        self.Vy = []
        for i in np.arange(0.01, 10, dt):
            a = (k1+k2*np.sqrt(Vx**2 + Vy**2)) / m #замедление от сопротивления воды
            ax = a*Vx
            ay = a*Vy
            Vx = Vx - ax*dt
            Vy = Vy - (g + ay)*dt
            Sx = Sx + Vx * dt
            Sy = Sy + Vy * dt - (g+a)*dt**2 / 2
            self.X.append(Sx)
            self.Y.append(Sy)
            self.Vx.append(Vx)
            self.Vy.append(Vy)
            