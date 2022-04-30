#Partie OpenAI

example_request = ["Qu'est-ce l'écologie ?",
"Hier, j'ai acheté des tomates venant d'Uruguay.",
"J'ai pris des patates françaises.",
"Bonjour !",
"jai acheté un T-shirt fabriqué en Chine.",
"g changé de téléphone au bout d'1 an",
"au revoir !!",
"J'ai vu un sac plastique dans la rue et je ne l'ai pas ramassé..."
]
example_answer = ["L’écologie est la science qui étudie les relations entre les organismes vivants et leur environnement. Je suis là pour parler plus particulièrement de votre empreinte carbone.",
"C'est pas bien ! Lorsque vous achetez des produits périssable comme des fruits ou des légumes,  vous devriez toujours essayer de choisir des produits locaux. Vos tomates ont été transportés sur de longues distances (sûrement en avion !), c'est désastreux pour votre empreinte carbone",
"Bon choix ! Les patates françaises sont une excellente option. C'est parfait pour votre empreinte carbone !",
"Bonjour ! Je suis Crapo la grenouille, je suis la pour vous aidez à baisser votre empreinte carbone.",
"C'est dommage. Les T-shirts fabriqués en Chine sont souvent produits dans des usines polluantes et sont transportés sur de longues distances, ce qui augmente l'empreinte carbone du produit.",
"C'est triste...Les téléphones portables sont souvent fabriqués avec des matériaux rares et polluants, et leur production peut générer beaucoup de déchets. Essayez de le garder longtemps !",
"Au revoir !",
"Ne refais pas ça! Les sacs plastiques peuvent mettre des années à se dégrader et peuvent polluer les sols et les eaux. De plus, ils peuvent être dangereux pour les animaux qui les mangent.",

]
example_emotion = ["content", "triste", "content","content","triste","triste","content","triste"]

examples = ""
examples_suffix = ""
for i in range(5):
    examples += "requête: "+example_request[i] + "\n"
    examples += "réponse: "+example_answer[i] + "\n"
    examples += "émotion: "+example_emotion[i] + "\n\n"
while i<len(example_answer):
    examples_suffix += "requête: "+example_request[i] + "\n"
    examples_suffix += "réponse: "+example_answer[i] + "\n"
    examples_suffix += "émotion: "+example_emotion[i] + "\n\n"
    i+=1
print(examples)
import os
import openai


openai.api_key = ""

def getCrapoResponse(question):
    r = openai.Completion.create(
  engine="text-davinci-002",
  prompt=examples+"requête: "+question+"\nréponse:",
  suffix=examples_suffix,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
    print(r)
    r=r["choices"][0]["text"]
    print(r)
    return r








#Partie Pygame
#this script uses pygames to create a text box
import pygame as pg
from pygame.locals import *
from sys import exit






def main():
    screen = pg.display.set_mode((1280,720),0,32)
    font = pg.font.SysFont("corbel", 42)
    font2 = pg.font.SysFont("corbel", 25)
    clock = pg.time.Clock()
    input_box = pg.Rect(490, 590, 300, 60)
    screen_rect = pg.Rect(460, 40, 360, 640)
    color = pg.Color((205,147,138))
    screen_bg_color = pg.Color((252,229,225))
    crapo_bubble = pg.Rect(490, 100, 300, 300)
    active = True
    text = ''
    done = False
    response= ""
    emotion = "content"

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text2 = text
                        text = ''
                        reaction = getCrapoResponse(text2).split("\n")
                        response = reaction[0]
                        print(reaction)
                        if len(reaction) > 1 and response != "":
                            emotion = reaction[1]
                            if "émotion: " == emotion[0:9]:
                                emotion = emotion[9:]
                        else:
                            response = "Je n'ai pas compris"
                            emotion = "trouble"
                        
                        
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0,0,0))

        
        
        #draw pale pink rectangle in the middle of the screen
        pg.draw.rect(screen, screen_bg_color, screen_rect, 0)
        
        # input_box background
        pg.draw.rect(screen, (255,255,255), input_box, 0)
        
        #draw crapo bubble as a rounded rectangle
        pg.draw.rect(screen, (255,255,255), crapo_bubble, 0, 25)

        # Render the current text.
        displayedText = ""
        i=len(text)-1
        while font.size(displayedText)[0] < 255 and i >= 0:
            displayedText = text[i] + displayedText
            i -= 1
        
        
        txt_surface = font.render(displayedText, True, color)



        # Blit the text.
        screen.blit(txt_surface, (500, 600))

        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        

        # Render the current response.
        
        i=0
        j=0
        
        while i < len(response.split()):
            displayed_resp = []
            while font2.size(" ".join(displayed_resp))[0] < 255 and i < len(response.split()):
                displayed_resp.append(response.split()[i])
                i += 1
            if len(displayed_resp) > 1 and font2.size(" ".join(displayed_resp))[0] >= 255:
                displayed_resp = displayed_resp[:-1]
                i-=1
                

            resp_surface = font2.render(" ".join(displayed_resp), True, color)
            pg.display.flip()
            
            # Blit the response.
            screen.blit(resp_surface, (500, 110+j*35))
            j+=1
            
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
