
from typing import List

import pygame
import random

FPS = 35
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

BOARD_WIDTH = 4
BOARD_HEIGHT = 4

TILE_WIDTH = 100
TILE_HEIGHT = 125
UNCOVER_SPEED = 10

LEFT_PANEL = 250
GAP_SIZE = 20
BORDER_GAP_X = (WINDOW_WIDTH - LEFT_PANEL - (BOARD_WIDTH * TILE_WIDTH) - (BOARD_WIDTH - 1) * GAP_SIZE) / 2
BORDER_GAP_Y = (WINDOW_HEIGHT - (BOARD_HEIGHT * TILE_HEIGHT) - (BOARD_HEIGHT - 1) * GAP_SIZE) / 2

COL_0 = (0, 0, 0)   
COL_1 = (0, 255, 0)   
COL_2 = (81, 74, 0)  
COL_3 = (0, 0, 255)  
COL_4 = (255, 255, 255)  
COL_5 = (9, 13, 20)   
COL_6 = (8, 11, 17)   
COL_7 = (33, 8, 38)  
COL_8 = (0, 8, 38)  
COL_9 = (54, 109, 108)
COL_10 = (178, 178, 178)
COL_11 = (96, 96, 96)  
COL_12 = (34, 34, 34)  

BG_COLOR = COL_0 
TILE_FRONT_COL = COL_9
PANEL_COL = COL_10 



new_game_btn = 'images/new_game_white.png'
img_1 = 'images/Fringe_apple.jpg'
img_2 = 'images/Fringe_butterfly.jpg'
img_3 = 'images/Fringe_frog.jpg'
img_4 = 'images/Fringe_hand.jpg'
img_5 = 'images/Fringe_leaf.jpg'
img_6 = 'images/Fringe_seahorse.jpg'
img_7 = 'images/Fringe_skull.jpg'
img_8 = 'images/Fringe_flower.jpg'
img_lst = [img_1, img_2, img_3, img_4, img_5, img_6, img_7, img_8]

left_txt1 = ''
left_txt2 = ''
left_txt3 = ''
left_txt4 = ''
left_txt5 = ''
left_txt6 = ''
you_win = 'You Win'
left_panel_texts = [left_txt1, left_txt2, left_txt3, left_txt4, left_txt5, left_txt6]
pixel_font = 'fonts/pixel_art/pixelart.ttf'


score = 0
trial_turns = 0
flipped_tiles = []
card_centres = []
turns = 0


def main():
    global screen, fps_clock

    pygame.init()

    fps_clock = pygame.time.Clock()
    text = " Fringe Memory Game"
    pygame.display.set_caption(text)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BG_COLOR)

    background = pygame.Surface(screen.get_size())
    background.fill(BG_COLOR)

    draw_control_panel(LEFT_PANEL, WINDOW_HEIGHT)
    pygame.time.wait(1000)

    x_mouse_pos = 0
    y_mouse_pos = 0
    choice_one = None

    game_board, revealed_sects = new_game()

    mainloop = True
    playtime = 0

    while mainloop:
        milliseconds = fps_clock.tick(FPS)
        playtime += milliseconds / 1000.0
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.type == pygame.MOUSEMOTION:
                x_mouse_pos, y_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                x_mouse_pos, y_mouse_pos = event.pos
                mouse_clicked = True
                print("Mouse clicked at:", x_mouse_pos, y_mouse_pos)

        text = " Fringe Memory Game FPS: {0:.2f}   Playtime: {1:.2f}".format(fps_clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        tile_pos = get_tile_at_pos(x_mouse_pos, y_mouse_pos)
        if (tile_pos[0] is None and tile_pos[1] is None) and mouse_clicked:
            new_game_rect = pygame.Rect(30, WINDOW_HEIGHT - 200, LEFT_PANEL - 50, 65)
            if new_game_rect.collidepoint(x_mouse_pos, y_mouse_pos):
                game_won(game_board)
                revealed_sects = initialize_exposed(False)
                draw_board(game_board, revealed_sects, TILE_WIDTH, BG_COLOR)
                pygame.time.wait(2000)

                game_board, revealed_sects = new_game()
                draw_board(game_board, revealed_sects)
                choice_one = None
        elif tile_pos[0] is not None and tile_pos[1] is not None:
            if not revealed_sects[tile_pos[0]][tile_pos[1]] and mouse_clicked:
                reveal_card_slide(game_board, [tile_pos])
                revealed_sects[tile_pos[0]][tile_pos[1]] = True
                if choice_one is None and choice_one != tile_pos:
                    choice_one = tile_pos
                    draw_board(game_board, revealed_sects)
                else:
                    first_tile = game_board[choice_one[0]][choice_one[1]]
                    second_tile = game_board[tile_pos[0]][tile_pos[1]]

                    if first_tile != second_tile:

                        pygame.time.wait(10)
                        cover_card_slide(game_board, [choice_one, tile_pos])
                        revealed_sects[choice_one[0]][choice_one[1]] = False
                        revealed_sects[tile_pos[0]][tile_pos[1]] = False
                    elif game_complete(revealed_sects):
                        game_won(game_board)
                        revealed_sects = initialize_exposed(False)
                        draw_board(game_board, revealed_sects, TILE_WIDTH, BG_COLOR)
                        pygame.time.wait(1000)

                        game_board, revealed_sects = new_game()

                    draw_board(game_board, revealed_sects)
                    choice_one = None

        pygame.display.flip()


def expose_start_gameboard(board):

    game_tiles = initialize_exposed(False)
    tiles = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            tiles.append((x, y))
    random.shuffle(tiles)


    draw_board(board, game_tiles)
    pygame.time.wait(2000)

    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        reveal_card_slide(board, boxes)
        cover_card_slide(board, boxes)


def game_won(board):

    game_tiles = initialize_exposed(True)
    tiles = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            tiles.append((x, y))
    random.shuffle(tiles)

    draw_board(board, game_tiles, color=BG_COLOR)

    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        cover_card_slide(board, boxes, BG_COLOR)


def board_reveal_animation(board):

    game_tiles = initialize_exposed(False)
    tiles = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            tiles.append((x, y))
    random.shuffle(tiles)

    draw_board(board, game_tiles, color=BG_COLOR)

    box_groups = []
    for i in range(0, len(tiles), 4):
        sect = tiles[i: i + 4]
        box_groups.append(sect)

    for boxes in box_groups:
        cover_card_slide(board, boxes, TILE_FRONT_COL, False)


def reveal_card_slide(board, cards):

    for width in range(TILE_WIDTH, (-UNCOVER_SPEED), -UNCOVER_SPEED):
        draw_board_covers(board, cards, width)


def cover_card_slide(board, cards, color=TILE_FRONT_COL, image=True):

    for width in range(0, TILE_WIDTH + 1, UNCOVER_SPEED):
        draw_board_covers(board, cards, width, color, image)


def create_random_board():
    all_images = img_lst * 2
    random.shuffle(all_images)


    game_board: List[List[str]] = []  
    for y in range(BOARD_HEIGHT):
        row = []

        for x in range(BOARD_WIDTH):
            row.append(all_images[0])
            del all_images[0]
        game_board.append(row)
    return game_board


def initialize_exposed(val):

    exposed = []
    for y in range(BOARD_HEIGHT):
        exposed.append([val] * BOARD_WIDTH)
    return exposed


def draw_board(board, exposed, width=TILE_WIDTH, color=TILE_FRONT_COL):

    for dummy_row in range(BOARD_HEIGHT):
        for dummy_col in range(BOARD_WIDTH):
            card = (dummy_row, dummy_col)
            coord_pos = top_coord(card)
            if not exposed[dummy_row][dummy_col]:
                pygame.draw.rect(screen, color, (coord_pos[0], coord_pos[1], width, TILE_HEIGHT))
            else:
                draw_board_icons(board, dummy_row, dummy_col, coord_pos)
    pygame.display.update()


def draw_board_icons(board, row, col, coord_pos):

    board_image = pygame.image.load(board[row][col]).convert()
    board_image = pygame.transform.scale(board_image, (TILE_WIDTH, TILE_HEIGHT))
    screen.blit(board_image, coord_pos)


def draw_board_covers(board, cards, width=TILE_WIDTH, color=TILE_FRONT_COL, image=True):

    for card in cards:
        coord_pos = top_coord(card)
        if image:
            draw_board_icons(board, card[0], card[1], coord_pos)
        if width > 0:
            pygame.draw.rect(screen, color, (coord_pos[0], coord_pos[1], width, TILE_HEIGHT))
    pygame.display.update()
    fps_clock.tick(FPS)


def top_coord(card):

    top_x = LEFT_PANEL + BORDER_GAP_X + card[0] * (TILE_WIDTH + GAP_SIZE)
    top_y = BORDER_GAP_Y + card[1] * (TILE_HEIGHT + GAP_SIZE)
    return top_x, top_y


def get_tile_at_pos(pos_x, pos_y):

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            top_x, top_y = top_coord((x, y))
            card_rect = pygame.Rect(top_x, top_y, TILE_WIDTH, TILE_HEIGHT)
            if card_rect.collidepoint(pos_x, pos_y):
                return x, y
    return None, None


def game_complete(revealed_sect):

    for item in revealed_sect:
        if False in item:
            return False
    return True


def draw_control_panel(width, height):




    new_game_logo = pygame.image.load(new_game_btn).convert()
    new_game_logo = pygame.transform.scale(new_game_logo, (width - 50, 65))
    new_logo_x = 30
    new_logo_y = height - 200

    screen.blit(new_game_logo, (new_logo_x, new_logo_y))

    font = pygame.font.Font(pixel_font, 16)
    for text in range(len(left_panel_texts)):
        text_x = font.render(left_panel_texts[text], True, COL_4, COL_0)
        text_rect = text_x.get_rect()
        text_rect.center = (0, 250 + text * 50)
        text_rect.left = 25
        screen.blit(text_x, text_rect)
        pygame.time.wait(500)
        pygame.display.flip()


def new_game():
    
    board = create_random_board()
    reveal_sects = initialize_exposed(False)
    pygame.time.wait(1200)
    board_reveal_animation(board)
    expose_start_gameboard(board)
    return board, reveal_sects


if __name__ == '__main__':
    main()