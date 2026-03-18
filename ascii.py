from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import sys
from math import sin, cos, pi

# --- Функція створення рельєфу (без змін) ---
def createHillyGround(size=25, res=50):
    format = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData('ground', format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    color = GeomVertexWriter(vdata, 'color')
    
    for i in range(res + 1):
        for j in range(res + 1):
            x = (i / res - 0.5) * size * 2
            y = (j / res - 0.5) * size * 2
            z = sin(x * 0.4) * cos(y * 0.4) * 1.5 # Коефіцієнт висоти пагорбів
            vertex.addData3f(x, y, z)
            # Колір: чим вище, тим світліша трава
            color.addData4f(0.1, 0.4 + (z * 0.1), 0.1, 1)

    prim = GeomTriangles(Geom.UHStatic)
    for i in range(res):
        for j in range(res):
            r1, r2 = i * (res + 1), (i + 1) * (res + 1)
            prim.addVertices(r1 + j, r2 + j, r1 + j + 1)
            prim.addVertices(r1 + j + 1, r2 + j, r2 + j + 1)

    geom = Geom(vdata); geom.addPrimitive(prim)
    node = GeomNode('ground'); node.addGeom(geom)
    return NodePath(node)

class GolfGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        
        # Рельєф
        self.ground = createHillyGround()
        self.ground.reparentTo(self.render)
        
        # М'яч
        self.ball_radius = 0.3
        self.ball = self.loader.loadModel("models/smiley")
        self.ball.setScale(self.ball_radius)
        self.ball.reparentTo(self.render)
        # Початкова позиція над землею
        self.ball.setPos(0, 0, self.get_height(0, 0) + self.ball_radius)

        # Лунка
        self.hole_pos = Point3(14, 14, 0)
        self.hole_pos.setZ(self.get_height(14, 14))
        self.hole = self.loader.loadModel("models/smiley")
        self.hole.setPos(self.hole_pos)
        self.hole.setScale(0.6, 0.6, 0.05)
        self.hole.setColor(0, 0, 0, 1)
        self.hole.reparentTo(self.render)

        # Ключка (спрощена модель)
        self.club = self.loader.loadModel("models/smiley")
        self.club.setScale(0.1, 0.1, 1.8)
        self.club.setColor(0.8, 0.8, 0.8, 1)
        self.club.reparentTo(self.render)

        # Фізика
        self.vel = Vec3(0, 0, 0)
        self.gravity = -12.0
        self.club_angle = 0
        self.gameOver = False

        self.winText = OnscreenText(text="ГОЛ!", pos=(0, 0.5), scale=0.2, fg=(1,1,0,1))
        self.winText.hide()

        self.keyMap = {"left": False, "right": False}
        self.accept("arrow_left", self.updateKey, ["left", True])
        self.accept("arrow_left-up", self.updateKey, ["left", False])
        self.accept("arrow_right", self.updateKey, ["right", True])
        self.accept("arrow_right-up", self.updateKey, ["right", False])
        self.accept("space", self.hit_ball)
        
        self.taskMgr.add(self.update, "update")

    def updateKey(self, key, state):
        self.keyMap[key] = state

    def get_height(self, x, y):
        return sin(x * 0.4) * cos(y * 0.4) * 1.5

    def get_normal(self, x, y):
        eps = 0.1
        dzdx = (self.get_height(x + eps, y) - self.get_height(x - eps, y)) / (2 * eps)
        dzdy = (self.get_height(x, y + eps) - self.get_height(x, y - eps)) / (2 * eps)
        norm = Vec3(-dzdx, -dzdy, 1)
        norm.normalize()
        return norm

    def hit_ball(self):
        if self.vel.length() < 0.3:
            rad = self.club_angle * (pi / 180.0)
            # Удар в напрямку прицілювання
            self.vel = Vec3(-cos(rad), -sin(rad), 0) * 15

    def update(self, task):
        dt = globalClock.getDt()
        if dt > 0.1 or self.gameOver: return Task.cont

        pos = self.ball.getPos()
        # Поверхня під м'ячем ПЛЮС його радіус
        ground_z = self.get_height(pos.getX(), pos.getY()) + self.ball_radius
        
        # --- Покращена фізика ---
        if pos.getZ() > ground_z + 0.05:
            # У повітрі: діє тільки гравітація
            self.vel.setZ(self.vel.getZ() + self.gravity * dt)
        else:
            # На землі: діє нахил поверхні та тертя
            norm = self.get_normal(pos.getX(), pos.getY())
            
            # Сила скочування (проекція гравітації на площину)
            slope = Vec3(norm.getX() * 8, norm.getY() * 8, 0)
            self.vel += slope * dt
            
            # Тертя об траву
            self.vel *= 0.985
            
            # Утримання м'яча рівно на поверхні
            if pos.getZ() < ground_z:
                pos.setZ(ground_z)
                if self.vel.getZ() < 0: self.vel.setZ(0)

        # Рух
        new_pos = pos + self.vel * dt
        self.ball.setPos(new_pos)

        # Прицілювання (ключка)
        if self.vel.length() < 0.3:
            if self.keyMap["left"]: self.club_angle += 180 * dt
            if self.keyMap["right"]: self.club_angle -= 180 * dt
            rad = self.club_angle * (pi / 180.0)
            self.club.setPos(pos.getX() + cos(rad)*1.5, pos.getY() + sin(rad)*1.5, pos.getZ() + 0.5)
            self.club.lookAt(self.ball)
            self.club.show()
        else:
            self.club.hide()

        # Перевірка на перемогу
        if (self.ball.getPos() - self.hole_pos).length() < 0.9:
            self.winText.show()
            self.gameOver = True

        # Камера слідує плавно
        self.camera.setPos(pos.getX(), pos.getY() - 12, pos.getZ() + 8)
        self.camera.lookAt(self.ball)
        
        return Task.cont

game = GolfGame()
game.run()
