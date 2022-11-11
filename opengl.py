import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

###
### https://stackoverflow.com/questions/61396799/how-can-i-blit-my-pygame-game-onto-an-opengl-surface
### Function to convert a PyGame Surface to an OpenGL Texture
### Maybe it's not necessary to perform each of these operations
### every time.
###
texID = glGenTextures(1)


def surface_to_texture(pygame_surface):
    global texID
    rgb_surface = pygame.image.tostring(pygame_surface, 'RGB')
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE,
                 rgb_surface)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
