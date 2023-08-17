import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *

mytheme = pygame_menu.themes.THEME_GREEN.copy()
font = pygame_menu.font.FONT_MUNRO
mytheme.font = font
sub_theme = mytheme.copy()
# sub_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT


class Window:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
        self.index = 0
        self.timer = Timer(200)

        
        self.menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Main Menu',
            width=1280
        )

        self.menu_genes = pygame_menu.Menu(
            height=720,
            center_content=False,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Menu with Genes',
            width=1280
        )

        self.menu_met = pygame_menu.Menu(
            height=720,
            center_content=False,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Menu with Metabolites',
            width=1280
        )


        self.menu_contributors = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Contributors',
            width=1280
        )

        # Add table to contributors
        table_contrib = self.menu_contributors.add.table()
        table_contrib.default_cell_padding = 5
        table_contrib.default_row_background_color = 'grey'
        bold_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        table_contrib.add_row(['Nº', 'Github User'], cell_font=bold_font)
        for i in range(len(pygame_menu.__contributors__)):
            table_contrib.add_row([i + 1, pygame_menu.__contributors__[i]], cell_font=bold_font if i == 0 else None)

        table_contrib.update_cell_style(-1, -1, font_size=15)  # Update all column/row
        table_contrib.update_cell_style(1, [2, -1], font=pygame_menu.font.FONT_OPEN_SANS_ITALIC)


        self.menu_reactions = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=sub_theme,
            title='Reactions',
            width=1280
        )

        for i in range(len(OPTIONS['Reactions'])):
            # menu_reactions.add.label(f'Reaction {OPTIONS["Reactions"][i]}', font_size=18)
            self.menu_reactions.add.range_slider(OPTIONS["Reactions"][i], (REACTIONS.lb[i],REACTIONS.ub[i]), (-1000, 1000), 10, font_size=30) #, rangeslider_id=OPTIONS['Reactions'][i])
            # menu_reactions.add.range_slider('LB', REACTIONS.lb[i], (-1000, 1000), 10, font_size=15) #, rangeslider_id=OPTIONS['Reactions'][i])
            # menu_reactions.add.range_slider('UP', REACTIONS.ub[i], (-1000, 1000), 10, font_size=16) #, rangeslider_id=OPTIONS['Reactions'][i])
            # menu_reactions.add.vertical_margin(20)

        
    # MENU SUB (Genes)

        label = '{}'

        for i in range(len(OPTIONS['Genes'])):
            txt = label.format(OPTIONS['Genes'][i])
            # menu_sub.add.button(txt, on_button_click, txt + ' -> ' + str(i+1))
            self.menu_genes.add.toggle_switch(txt, True, onchange=self.toggle_gene, kwargs=txt, toggleswitch_id=txt)
        
        self.menu_genes.add.button('Back', pygame_menu.events.BACK)



        label = '{}'
        for i in range(len(OPTIONS['Metabolites'])):
            txt = label.format(OPTIONS['Metabolites'][i])
            self.menu_met.add.toggle_switch(txt, True, onchange=self.toggle_gene, kwargs=txt)
        
        self.menu_met.add.button('Back', pygame_menu.events.BACK)



    def data_fun(self) -> None:
            """
            Print data of the menu.
            """
            print('Settings data:')
            data_method = self.menu.get_input_data()
            data_genes = self.menu_genes.get_input_data()
            data_met = self.menu_met.get_input_data()
            data_reac = self.menu_reactions.get_input_data()
            for k in data_method.keys():
                print(f'\t{k}\t=>\t{data_method[k]}')
            for k in data_genes.keys():
                print(f'\t{k}\t=>\t{data_genes[k]}')
            for k in data_met.keys():
                print(f'\t{k}\t=>\t{data_met[k]}')
            for k in data_reac.keys():
                print(f'\t{k}\t=>\t{data_reac[k]}')

            sceneExit = False
            time = 1500
            while not sceneExit:

                text_surf = self.font.render(f'Simulation saved',False,'black')
                text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-20))
                pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10,10),0,2) #ultimos 2 argumentos se quiser bordas redondas pode-se adicionar estes argumentos
                self.display_surface.blit(text_surf, text_rect)

                pygame.display.update()

                passed_time = pygame.time.Clock().tick(60)
                time -= passed_time
                if time <= 0:
                    sceneExit = True
            #end of function


        

    def setup(self):

        self.menu.add.dropselect(title='Simulation Method: ',
                            items=[('FBA', 'fba'),
                                   ('pFBA', 'pfba'),
                                   ('MOMA', 'moma'),
                                   ('lMOMA', 'lmoma'),
                                   ('ROOM','room')],
                                   default=0,
                                   selection_box_height=4)
        self.menu.add.text_input('Objective: ', default=str(OPTIONS['Objective']))
        self.menu.add.button('Genes', self.menu_genes)
        self.menu.add.button('Metabolites', self.menu_met)
        self.menu.add.button('Table', self.menu_contributors)
        self.menu.add.button('Reactions 2', self.menu_reactions)
        self.menu.add.vertical_margin(50)  # Adds margin
        self.menu.add.button('Save Simulation', action=self.data_fun, background_color=(50,100,100))        
        self.menu.add.vertical_margin(20)  # Adds margin
        # menu.add.button('Restore / Cancel', menu.reset_value, background_color=(100,0,0))

        self.menu.mainloop(self.display_surface)



    
    def on_button_click(self, value: str, text = None) -> None:
        if not text:
            print(f'Hello from {value}')
        else:
            print(f'Hello from {text} with {value}')


    def toggle_gene(self, txt, **id) -> None:
        """
        Button event on menus.

        :param value: Button value
        :param text: Button text
        """
        if txt:
            print(f'{id} on')
        else:
            print(f'{id} knockout')



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        


