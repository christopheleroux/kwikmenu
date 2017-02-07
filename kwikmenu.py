#!/usr/bin/env python
# -*- coding: utf-8 -*-


# http://wolfvollprecht.de/blog/gtk-python-and-css-are-an-awesome-combo/
# https://gist.github.com/fcwu/5794494
# Python 3 + gtk 3 !!!
# http://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html

#!/usr/bin/python3
from gi.repository import Gtk, Gdk
import sys
import yaml
import os
import subprocess

KEY_ESC=65307
KEY_ENTER=65293

KEY_UP=65362
KEY_RIGHT=65363
KEY_DOWN=65364
KEY_LEFT=65361

class KwikMenu(Gtk.Window):

    def __init__(self,data):
        # Style de fenetre
        Gtk.Window.__init__(self)
        self.set_name('KwikMenu')
        self.connect("key-press-event",self.on_key_pressed)
        self.set_decorated(False)

        self.box = Gtk.VBox()
        self.box.set_halign(Gtk.Align.CENTER)
        self.box.set_valign(Gtk.Align.CENTER)
        self.add(self.box)

        # Creaton des boutons
        self.buttonDict = {}
        self.commandDict = {}
        index = 0
        for i in data:
            button = Gtk.ToggleButton(i['name'])
            self.buttonDict[index] = button
            self.commandDict[index] = i['command']
            index += 1
        # Activation des bouton au démarrage
        self.selected = 0
        self.buttonDict[self.selected].set_active(True)
        self.render()

    # rendering des boutons
    def render(self):
        for key in self.buttonDict:
            self.box.pack_start(self.buttonDict[key], True, True, 0)

    def on_key_pressed(self,widget,event):
        # Escape
        # http://stackoverflow.com/questions/23111362/key-binding-for-window-app-in-python-gtk-3-without-menu-items-ui-manager-etc

        if (event.keyval == KEY_ESC):
            Gtk.main_quit()
        if (event.keyval == KEY_ENTER):
            self.run_command()
        if event.keyval == KEY_UP or event.keyval == KEY_LEFT:
            self.select_next(-1)
        if event.keyval == KEY_DOWN or event.keyval == KEY_RIGHT:
            self.select_next(1)

    def select_next(self,prevnext):
        self.buttonDict[self.selected].set_active(False)
        self.selected = (self.selected + prevnext) % (max(self.buttonDict.keys()) + 1)
        self.buttonDict[self.selected].set_active(True)

    def run_command(self):
        command = self.commandDict[self.selected]
        print("command="+ str(command.split()))
        pid = subprocess.Popen(command.split())
        print(pid)
        Gtk.main_quit()


def main(argv):
    configfile = os.getenv("HOME") + "/.kwikmenu.yaml"

    if os.path.isfile(configfile):
        with open(configfile, 'r') as stream:
            data = yaml.load(stream)
    else:
        print("Aucun fichier de configuration trouvé $HOME/.kwikmenu.yaml")
        sys.exit()

    def gtk_style():
        css = b"""
/*
* {
    transition-property: color, background-color, border-color, background-image, padding, border-width;
    transition-duration: 1s;
    font: Cantarell 20px;
}*/

.button {
    color: black;
    background-color: #bbb;
    border-style: solid;
    border-width: 2px 0 2px 2px;
    border-color: #333;
    padding: 12px 4px;
}

        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    gtk_style()

    win = KwikMenu(data)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main(sys.argv)

# # TODO empecher les instances multiples