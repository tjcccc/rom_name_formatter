import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from views.form_input import FormInput
from services.config_service import ConfigService
from styles.app import Layout


class DirectoriesForm(ttk.Frame):
    def __init__(self, root, config_service: ConfigService, on_change=None):
        super().__init__(master=root)

        # self.roms_directory = ''
        # self.saves_directory = ''
        # self.states_directory = ''
        self.on_change = on_change
        self.config_service = config_service
        self.config = config_service.load_config()

        # Layout
        self.roms_directory_input = FormInput(self, 'ROMS', Layout.component_width(12), state='disabled')
        self.roms_directory_input.grid(column=0, row=0, sticky='ew')
        self.saves_directory_input = FormInput(self, 'SAVES', Layout.component_width(12), state='disabled')
        self.saves_directory_input.grid(column=0, row=1, sticky='ew', pady=Layout.spacing())
        self.states_directory_input = FormInput(self, 'STATES', Layout.component_width(12), state='disabled')
        self.states_directory_input.grid(column=0, row=2, sticky='ew')
        self.choose_rom_directory_button = ttk.Button(self, text='Choose', command=lambda: self.choose_directory('roms'))
        self.choose_rom_directory_button.grid(column=1, row=0, sticky='ew', padx=Layout.spacing())
        self.choose_saves_directory_button = ttk.Button(self, text='Choose', command=lambda: self.choose_directory('saves'))
        self.choose_saves_directory_button.grid(column=1, row=1, sticky='ew', padx=Layout.spacing())
        self.choose_states_directory_button = ttk.Button(self, text='Choose', command=lambda: self.choose_directory('states'))
        self.choose_states_directory_button.grid(column=1, row=2, sticky='ew', padx=Layout.spacing())

        # Initialize values
        self.initialize_directories(self.config.roms_directory, self.config.saves_directory, self.config.states_directory)

    def initialize_directories(self, roms_directory, saves_directory, states_directory):
        self.roms_directory_input.set_input(roms_directory)
        self.saves_directory_input.set_input(saves_directory)
        self.states_directory_input.set_input(states_directory)

    def choose_directory(self, type: str):
        folder_path = filedialog.askdirectory()

        if folder_path:
            if type == 'roms':
                self.config.roms_directory = folder_path
                self.roms_directory_input.set_input(folder_path)
            elif type == 'saves':
                self.config.saves_directory = folder_path
                self.saves_directory_input.set_input(folder_path)
            elif type == 'states':
                self.config.states_directory = folder_path
                self.states_directory_input.set_input(folder_path)

        self.config_service.save_config(self.config)

        if self.on_change:
            self.on_change()

    # def get_directories(self):
    #     return self.roms_directory_input.get_input(), self.saves_directory_input.get_input(), self.states_directory_input.get_input()

