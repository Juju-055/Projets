#prj final : faire les sprite qui qd on saute
import pyxel
import random

class Joueur:
    def __init__(self, x, y):
        self.x = x + 8
        self.y = y
        #self.y_ = self.y
        self.vertical = 0  # vitesse vertical du joueur
        self.gravity = 0.35 # Gravité qui augmente 
        self.jump = -3.3 # Force du saut - pour monter
        self.game_over = False
        self.start = False
        self.vitesse = 2 #vitesse de l'oiseau
        self.score = 0
        self.record = self.score
        self.w_sprit = 19
        self.y_sprit = 12

    def update(self):

        if not self.game_over: 
            if self.start == True:
                # Ajout de la gravité à la vitesse
                self.x = self.x + self.vitesse
                self.vertical += self.gravity
                
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.vertical = self.jump
                    pyxel.play(1,1)

                # maj de la position en fonction de la vitesse
                self.y += self.vertical
                
                #if self.y != self.y_:self.w_sprit = 34
                
                # simule le rebond sur le mur + ajout de point
                if self.x == 100 :
                    self.vitesse = -2
                    self.w_sprit = 2
                    self.score += 1
                    pyxel.play(2,2)
                    
                if self.x == 10 :
                    self.vitesse = 2
                    self.w_sprit = 19
                    self.score += 1
                    pyxel.play(2,2)
                # game over si le jouer touche le haut/bas de l'écran
                if self.y > pyxel.height - 27 or self.y < 6:
                    self.game_over = True
                    self.w_sprit = 64
                    self.y_sprit = 20
                    pyxel.play(0,0)
                    
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.start = True
                self.vertical = self.jump

    def reset(self):
        self.x = x + 10 
        self.y = 65
        self.vertical = 0 # vitesse verticale du j
        self.game_over = False
        self.start = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.w_sprit, 0, self.y_sprit, 16, 15)

class Piques_gauche:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = random.randint(16, 50)
        self.w_sprit = 0
        self.y_sprit = 40
    
    def update(self): 
        if self.start:
            if self.Joueur.score == 1:
                self.height = random.randint(10, 80)
    #changement        
    def reset(self):
        #self.height = random.randint(10, 50)
        pass
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.w_sprit, 0, self.y_sprit, 16, 15)
  
class Game:
    def __init__(self):
        pyxel.init(120, 130, title="Don't touch the spikes !")
        self.joueur = Joueur(40, pyxel.height // 2)
        self.record = self.joueur.score
        self.frame_counter = 0  # Compteur de frames 
        
        pyxel.load("res.pyxres") 
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.joueur.game_over: # rajout
            self.joueur.update()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()
            pyxel.play(2, 2)# changement
        
        if self.record < self.joueur.score and self.joueur.game_over :
            self.record = self.joueur.score
            pyxel.play(3,3)
    
    def reset_game(self):
        self.joueur = Joueur(40, pyxel.height // 2)
        self.joueur.score = 0  # Initialisation du score
        
    def draw(self):
        pyxel.cls(6)
        self.joueur.draw()
        pyxel.text(15, 14, f"Score:{self.joueur.score}", 2)
        pyxel.text(72, 14, f"Record:{self.record}", 5)
        
        #pyxel.bltm(16, 6, 0, 11, 1, 6, 3, 15)#platformes en fond
        pyxel.bltm(11, 0, 0, 0, 3, 98, 16, 15)#piques du haut
        pyxel.bltm(11, 118, 0, 0, 24, 98, 12, 15)#piques du bas
        pyxel.bltm(-1, 0, 0, 0, 40, 98, 130, 15)# mur gauche
        pyxel.bltm(107, 0, 0, 0, 40, 98, 130, 15)# mur droit
        pyxel.bltm(107, 0, 0, 0, 40, 98, 130, 15)# fond
        
        if self.joueur.start == False:
            pyxel.text(27, 55, "Press on SPACE", 5)
        # Affichage "Game Over"
        if self.joueur.game_over:
            pyxel.text(38, 55, "GAME OVER!", pyxel.COLOR_RED)
            pyxel.text(38, 65, "Press on R", 5)
            # remplace l'ancien record par le nouveau
            if self.record < self.joueur.score:
                self.record = self.joueur.score
                

Game()