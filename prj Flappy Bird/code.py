#lien du vrai https://www.pyxelstudio.net/studio/uqjswk
# Explications en hashtags

import pyxel
import random

class Joueur:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.velocity = 0  # vitesse verticale du joueur
        self.gravity = 0.35 # Gravité qui augmente la vitesse de chute
        self.jump = -3.3 # Force du saut - pour monter
        self.game_over = False
        self.start = False

    def update(self):
        if not self.game_over: # rajout
            if self.start == True:
                # Ajout de la gravité à la vitesse
                self.velocity += self.gravity
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.velocity = self.jump

                # maj de la position en fonction de la vitesse
                self.y += self.velocity
                
                # empêcher le joueur de sortir de l'écran par le bas
                if self.y > pyxel.height - 8:  # taille joueur 8
                    self.y = pyxel.height - 8
                    self.velocity = 0
                    
                # Empêcher le joueur de sortir par le haut
                if self.y < 0:
                    self.y = 0
                    self.velocity = 0 #rajout
                    
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.start = True
                self.velocity = self.jump

            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(1, 1)

    def reset(self):
        self.x = 40 
        self.y = 65
        self.velocity = 0 # vitesse verticale du j
        self.game_over = False
        self.start = False
        
    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 2)
        pyxel.bltm(self.x, self.y, 0, 0, 0, 8, 8)

class Tuyaux:
    def __init__(self, x, y, c1, c2):
        self.c1 = c1
        self.c2 = c2
        self.x = x
        self.y = y
        self.width = 15
        self.height = random.randint(10, 80)
        self.vitesse = 2
        self.start = False
        self.scored = False  # Pour vérifier si le tuyau a été franchi
    
    def update(self): 
        if self.start:
            self.x -= self.vitesse
        # Réinitialisation du tuyau quand il sort de l'écran
        if self.x + self.width < 0:
            self.x = pyxel.width + 30
            self.height = random.randint(10, 80)
            self.scored = False  # Réinitialise le score pour ce tuyau
    #changement  et  =+ changer en false
            
    #changement        
    def reset(self):
        self.x = pyxel.width + 30 # changement
        self.height = random.randint(10, 80)
        self.scored = False #rajouter
        self.start = False
        
    # rajout
    def check_collision(self, joueur): 
        # Vérification des collisions avec les parties supérieures et inférieures des tuyaux
        joueur_rect = (joueur.x, joueur.y, joueur.x + 8, joueur.y + 8)  # Rectangle du joueur
        tuyau_haut_rect = (self.x, self.y, self.x + self.width, self.y + self.height)  # Rectangle du tuyau haut
        tuyau_bas_rect = (self.x, self.y + self.height + 40, self.x + self.width, pyxel.height)  # Rectangle du tuyau bas

        # Vérifier si les rectangles se chevauchent
        return (self.rect_overlap(joueur_rect, tuyau_haut_rect) or 
            self.rect_overlap(joueur_rect, tuyau_bas_rect))
            
    @staticmethod
    def rect_overlap(rect1, rect2):
        # Vérifie si deux rectangles se chevauchent
        return not (rect1[2] <= rect2[0] or rect1[0] >= rect2[2] or rect1[3] <= rect2[1] or rect1[1] >= rect2[3])
    
    def draw(self): 
        pyxel.rect(self.x, self.y, self.width, self.height, self.c1) 
        pyxel.rect(self.x, self.y + self.height + 40, self.width, pyxel.height - self.height - 40, self.c2) 

class Game:
    def __init__(self):
        pyxel.init(200, 130, title="Flappy Bird")
        self.joueur = Joueur(40, pyxel.height // 2)
        self.tuyaux = [Tuyaux(160 + 60 * i, 0, 10, 11) for i in range(4)]
        self.score = 0  # Initialisation du score
        self.record = self.score
        self.frame_counter = 0  # Compteur de frames pour vérifier quand augmenter le score
        
        pyxel.load("res.pyxres") 
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.joueur.game_over: # rajout
            self.joueur.update()
            for tuyau in self.tuyaux:
                tuyau.update()
                
                # Vérification des collisions
                if tuyau.check_collision(self.joueur):
                    self.joueur.game_over = True
                    pyxel.play(0, 0)  # Jouer un son de collision
                    break  # rajout

        if self.joueur.start:
            for tuyau in self.tuyaux:
                tuyau.start = True

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()
            pyxel.play(2, 2)# changement

        # Calcul du score quand le joueur passe un tuyau 
        for tuyau in self.tuyaux:
            if not tuyau.scored and self.joueur.x > tuyau.x + tuyau.width:
                self.score += 1
                tuyau.scored = True  # Marque le tuyau comme franchi
        
        if self.record < self.score and self.joueur.game_over :
                pyxel.play(3,3)
    
    def reset_game(self):
        self.joueur = Joueur(40, pyxel.height // 2)
        self.tuyaux = [Tuyaux(160 + 60 * i, 0, 10, 11) for i in range(4)]
        self.score = 0  # Initialisation du score
        self.frame_counter = 0  # Compteur de frames pour vérifier quand augmenter le score
        
    def draw(self):
        pyxel.cls(6)
        self.joueur.draw()
        for tuyau in self.tuyaux:
            tuyau.draw()
        pyxel.text(10, 8, f"Score: {self.score}", 2)
        pyxel.text(150, 8, f"Record: {self.record}", 5)
        
        # Affichage "Game Over"
        if self.joueur.game_over:
            pyxel.text(80, 55, "GAME OVER!", pyxel.COLOR_RED) # rajout
            pyxel.text(30, 65, "Appuyez sur R pour relancer la partie", 5)
            # remplace l'ancien record par le nouveau
            if self.record < self.score:
                self.record = self.score
                

Game()
