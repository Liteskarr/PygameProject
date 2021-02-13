import os
import json
import shutil
import random
import string

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import (UIButton, UISelectionList, UILabel)

from pygame_engine.engine import Engine
from pygame_engine.scene import Scene
from pygame_engine.window import Window

from src.scenarios.all import (BaseScenarioBuilder)
from src.game_scene import GameScene


def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


SCENARIOS_DICT = {
    'Базовый сценарий': BaseScenarioBuilder
}


class MainMenuScene(Scene):
    def on_starting(self):
        self._available_savings = {}
        self._deleted = set()
        self.screen_surface = Window.get_screen_surface()
        self.ui_manager = UIManager(Window.get_size(), '../data/theme.json')
        self.init_ui()
        self.load_savings()

    def init_ui(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        width, height = Window.get_size()
        self.exit_button = UIButton(
            manager=self.ui_manager,
            text='Выход',
            relative_rect=pygame.Rect((50, height - 150), (200, 100))
        )
        self.exit_button.font = self.font
        self.exit_button.rebuild()

        self.deleting_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 350), (200, 100)),
            text='Удалить игру'
        )
        self.deleting_button.font = self.font
        self.deleting_button.rebuild()
        self.deleting_button.disable()

        self.creating_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 450), (200, 100)),
            text='Новая Игра'
        )
        self.creating_button.font = self.font
        self.creating_button.rebuild()
        self.creating_button.disable()

        self.loading_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, height - 550), (200, 100)),
            text='Загрузить игру'
        )
        self.loading_button.font = self.font
        self.loading_button.rebuild()
        self.loading_button.disable()

        self.games_list = UISelectionList(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((width - 450, height - 500), (400, 450)),
            item_list=[]
        )
        self.games_list.font = self.font
        self.games_list.rebuild()

        self.games_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((width - 449, height - 549), (398, 48)),
            text='Сохранения'
        )
        self.games_label.font = self.font
        self.games_label.rebuild()

        self.scenarios_list = UISelectionList(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((width - 850, height - 500), (400, 450)),
            item_list=list(SCENARIOS_DICT.keys())
        )
        self.scenarios_list.font = self.font
        self.scenarios_list.rebuild()

        self.scenarios_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((width - 849, height - 549), (398, 48)),
            text='Сценарии'
        )
        self.scenarios_label.font = self.font
        self.scenarios_label.rebuild()

        self.main_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((50, 50), (width - 100, height - 650)),
            text='The Best Minecraft Mod'
        )
        self.font = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.main_label.font = self.font
        self.main_label.rebuild()

    def load_savings(self):
        for saving in os.listdir('../savings'):
            saving = f'../savings/{saving}'
            if os.path.isdir(saving):
                data = json.load(open(f'{saving}/base/base.json', 'r', encoding='utf-8'))
                name = data['name']
                sys_name = data['sys_name']
                if sys_name not in self._deleted:
                    self._available_savings[name] = sys_name
        self.games_list.set_item_list([k for k in self._available_savings.keys()
                                       if self._available_savings[k] not in self._deleted])
        self.games_list.font = self.font
        self.games_list.rebuild()

    def on_updating(self, delta_time: float):
        self.ui_manager.update(delta_time)
        self.ui_manager.draw_ui(self.screen_surface)

    def on_any_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

    def on_userevent(self, event: pygame.event.Event):
        if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.games_list:
                self.loading_button.enable()
                self.deleting_button.enable()
                self.creating_button.disable()
            elif event.ui_element == self.scenarios_list:
                self.loading_button.disable()
                self.deleting_button.disable()
                self.creating_button.enable()
        elif event.user_type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
            if event.ui_element == self.games_list:
                self.loading_button.disable()
                self.deleting_button.disable()
            elif event.ui_element == self.scenarios_list:
                self.creating_button.disable()
        elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button:
                Engine.running = False
            elif event.ui_element == self.deleting_button:
                self._deleted.add(self._available_savings[self.games_list.get_single_selection()])
                self.load_savings()
            elif event.ui_element == self.creating_button:
                loading_name = id_generator(8)
                scenario = self.scenarios_list.get_single_selection()
                builder = SCENARIOS_DICT[scenario]()
                builder.build(f'{builder.get_prefix()}{loading_name}', loading_name)
                builder.save(loading_name)
                self.load_savings()
            elif event.ui_element == self.loading_button:
                game_scene = GameScene(self._available_savings[self.games_list.get_single_selection()])
                game_scene.main_menu_game_scene_cls = self.__class__
                Engine.set_scene(game_scene)

    def on_closing(self):
        for saving in self._deleted:
            shutil.rmtree(f'../savings/{saving}')
