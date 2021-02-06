import os
import json
import shutil

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import (UIButton, UISelectionList, UILabel)

from pygame_engine.engine import Engine
from pygame_engine.scene import Scene
from pygame_engine.window import Window

from src.game_scene import GameScene


class MainMenuScene(Scene):
    def on_starting(self):
        self._current_saving = ''
        self._available_savings = {}
        self._deleted = set()
        self.screen_surface = Window.get_screen_surface()
        self.ui_manager = UIManager(Window.get_size())
        self.init_ui()
        self.load_savings()

    def init_ui(self):
        width, height = Window.get_size()
        self.exit_button = UIButton(
            manager=self.ui_manager,
            text='Выход',
            relative_rect=pygame.Rect((50, height - 150), (200, 100))
        )

        self.credits_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 250), (200, 100)),
            text='Создатели'
        )

        self.deleting_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 350), (200, 100)),
            text='Удалить игру'
        )

        self.creating_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 450), (200, 100)),
            text='Новая Игра'
        )

        self.loading_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 550), (200, 100)),
            text='Загрузить игру'
        )
        self.loading_button.hide()

        self.games_list = UISelectionList(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((width - 450, height - 550), (400, 500)),
            item_list=[]
        )

        self.main_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, 50), (width - 100, height - 650)),
            text='The Best Minecraft Mod'
        )
        font = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.main_label.font = font
        self.main_label.rebuild()

    def load_savings(self):
        self._current_saving = ''
        for saving in os.listdir('../savings'):
            saving = f'../savings/{saving}'
            if os.path.isdir(saving):
                data = json.load(open(f'{saving}/base/base.json', 'r', encoding='utf-8'))
                name = data['name']
                sys_name = data['sys_name']
                if sys_name not in self._deleted:
                    self._available_savings[name] = sys_name
        self.games_list.set_item_list(list(self._available_savings.keys()))
        self.games_list.rebuild()

    def on_updating(self, delta_time: float):
        self.ui_manager.update(delta_time)
        self.ui_manager.draw_ui(self.screen_surface)

    def on_any_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

    def on_userevent(self, event: pygame.event.Event):
        if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            self._current_saving = event.text
            self.loading_button.show()
        elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button:
                Engine.running = False
            elif event.ui_element == self.credits_button:
                pass
            elif event.ui_element == self.deleting_button:
                self._deleted.add(self._available_savings[self._current_saving])
                self.load_savings()
            elif event.ui_element == self.creating_button:
                pass
            elif event.ui_element == self.loading_button:
                Engine.set_scene(GameScene(self._available_savings[self._current_saving]))

    def on_closing(self):
        pass
