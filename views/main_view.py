import math
import tkinter as tk
from tkinter import ttk
from models.game_file import GameFile, GameFileType
from views.custom_tag_input import CustomTagInput
from views.directories_form import DirectoriesForm
from views.files_list import FilesList
from views.datum import Datum
from views.form_input import FormInput
from services.config_service import ConfigService
from styles.app import Layout


class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x1000')
        self.root.title('Rom Name Formatter')
        self.root.columnconfigure(0, weight=1)

        self.config_service = ConfigService('./config.json')
        config = self.config_service.load_config()
        tags = config.tags

        # self.roms_directory = tk.StringVar(value=config.roms_directory)
        # self.saves_directory = tk.StringVar(value=self.config.saves_directory)
        # self.states_directory = tk.StringVar(value=self.config.states_directory)

        self.selected_file: GameFile | None = None

        main_frame = ttk.Frame(self.root, padding=Layout.spacing(2))
        main_frame.grid(sticky='nsew')
        main_frame.columnconfigure(0, weight=1)

        # Directories of Roms, Saves, and States
        self.directories_form_container = DirectoriesForm(main_frame, self.config_service, self.directories_on_change)
        self.directories_form_container.grid(column=0, row=0, sticky='ew', padx=Layout.spacing(2))

        # Clear and Load Directories and Buttons
        button_group = ttk.Frame(main_frame)
        button_group.grid(column=0, row=1, sticky='ew')
        button_group.columnconfigure(0, weight=1)
        button_group.columnconfigure(3, weight=1)
        clear_button = ttk.Button(button_group, text='CLEAR', command=self.directories_form_container.clear)
        clear_button.grid(column=1, row=1, pady=Layout.spacing(2))
        load_roms_directory_button = ttk.Button(button_group, text='LOAD', command=self.load_roms_directory)
        load_roms_directory_button.grid(column=2, row=1, pady=Layout.spacing(2))

        # Rom Files List
        self.files_list = FilesList(main_frame)
        self.files_list.grid(column=0, row=2, padx=Layout.spacing(), pady=Layout.spacing(), sticky='nsew')

        # Current Selected File's Original Name
        self.selected_file_name = Datum(main_frame, 'OLD', '', padding=Layout.spacing())
        self.selected_file_name.grid(column=0, row=3, sticky='ew', padx=Layout.spacing())
        self.new_file_name_preview = Datum(main_frame, 'NEW', '', padding=Layout.spacing())
        self.new_file_name_preview.grid(column=0, row=4, sticky='ew', padx=Layout.spacing())

        # New File Name Format
        self.new_file_name_format = FormInput(main_frame, 'FORMAT', Layout.component_width(12), padding=Layout.spacing(), on_change=self.on_change_file_format)
        self.new_file_name_format.grid(column=0, row=5, sticky='ew', padx=Layout.spacing())

        # Tag Input Group
        self.tags_label = ttk.Label(main_frame, text='TAGS', anchor='w')
        self.tags_label.grid(column=0, row=6, sticky='w', padx=Layout.spacing(2), pady=(Layout.spacing(), 0))
        self.tags_container = ttk.Frame(main_frame)
        self.tags_container.grid(column=0, row=7, sticky='ew', padx=Layout.spacing(2))
        total_tags_rows = int(math.ceil(len(tags) / 3))
        print(total_tags_rows)
        for index, tag in enumerate(tags):
            column_number = int(index % 3)
            row_number = int(math.floor(index / 3))
            print(column_number, row_number)
            custom_tag_input = CustomTagInput(self.tags_container, tag, padding=Layout.spacing())
            custom_tag_input.grid(column=column_number, row=row_number, sticky='ew', padx=Layout.spacing())

        self.root.mainloop()

    def directories_on_change(self):
        pass
        # config = self.config_service.load_config()
        # self.roms_directory.set(config.roms_directory)

    def load_roms_directory(self):
        config = self.config_service.load_config()
        roms_path = config.roms_directory
        roms_files = self.directories_form_container.load_roms_directory()
        # game_directory = GameDirectory(config.roms_directory, file_type=GameFileType.ROM)
        self.files_list.update_list(roms_path, roms_files, self.on_click_the_file)

    def on_click_the_file(self, event):
        if event.type != '5':
            return
        item = self.files_list.container.selection()[0]
        file_index = int(self.files_list.container.item(item, 'values')[0]) - 1
        file = self.files_list.get_file_by_index(file_index)

        self.selected_file = file

        # Update components
        self.selected_file_name.set_value(file.get_file_fullname())
        self.new_file_name_preview.set_value(file.get_file_fullname())

        print(file.get_path())

    def on_change_file_format(self, event):
        if self.selected_file is None:
            return
        new_file_name = self.new_file_name_format.get_input()
        self.new_file_name_preview.set_value(new_file_name)
        print(new_file_name)
