#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gtk
import cairo
import gobject

ALPHA_BASE = 1.0
APP_NAME = "emulauncher"
APP_VERSION = "0.1"
COVER_DIR = "cover"
PCSX2_FLAGS = "--fullboot --fullscreen --nogui"
PCSX2_PATH = "/usr/games/PCSX2"
ROMS_DIR = "roms"
FONT_SIZE = 30

class Title():
    """
    """
    def __init__(self, desc):
        """
        """
        self.cover = desc["cover"]
        self.rom = desc["rom"]

class MainApp(gtk.Window):
    """
    """
    def __init__(self):
        """
        """
        super(MainApp, self).__init__()

        self.set_title(APP_NAME + ' ' + APP_VERSION)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)
        self.connect("window-state-event", self.window_state)

        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.connect("expose-event", self.expose)
        self.drawing_area.connect("key-press-event", self.key_press)

        self.drawing_area.add_events(gtk.gdk.ENTER_NOTIFY |
                                     gtk.gdk.LEAVE_NOTIFY |
                                     gtk.gdk.KEY_PRESS_MASK |
                                     gtk.gdk.KEY_RELEASE_MASK)

        self.add(self.drawing_area)
        self.drawing_area.set_flags(gtk.CAN_FOCUS)

        self.path = os.path.abspath(COVER_DIR)
        self.selected_item = 0
        self.is_fullscreen = False
        self.load_covers()

        self.alpha = ALPHA_BASE

        self.show_all()
        self.fullscreen()

    def window_state(self, widget, event):
        """
        """
        state = event.new_window_state
        self.is_fullscreen = (gtk.gdk.WINDOW_STATE_FULLSCREEN == state)

    def load_covers(self):
        """
        """
        desc = {}
        self.titles = []
        self.surface = []
        rom_path = os.path.abspath(ROMS_DIR)

        for cover in os.listdir(self.path):
            desc["cover"] = os.path.join(self.path, cover)
            desc["rom"] = os.path.join(rom_path, cover[:-4] + ".iso")
            s = cairo.ImageSurface.create_from_png(desc["cover"])
            self.surface.append(s)
            self.titles.append(Title(desc))

    def key_press(self, widget, event):
        """
        """
        key = gtk.gdk.keyval_name(event.keyval)

        if (key == "Escape"):
            gtk.main_quit()

        if (key == "Up"):
            self.alpha = ALPHA_BASE
            self.selected_item = (self.selected_item + 1) % len(self.surface)

        if (key == "Down"):
            self.alpha = ALPHA_BASE
            self.selected_item = (self.selected_item - 1) % len(self.surface)

        if (key == "F11"):
            if (self.is_fullscreen):
                self.unfullscreen()
            else:
                self.fullscreen()

        if (key == "space"):
            title = self.titles[self.selected_item]
            if (os.path.isfile(title.rom)):
                command = " ".join([PCSX2_PATH, PCSX2_FLAGS, title.rom])
                os.system(command)

        self.drawing_area.queue_draw()

    def expose(self, widget, event):
        """
        """
        self.resize(800, 600)

        context = widget.window.cairo_create()
        surface = self.surface[self.selected_item]

        w = self.allocation.width
        h = self.allocation.height

        context.rectangle(0, 0, w, h)
        context.set_source_rgb(1, 1, 1)
        context.paint()

        context.set_source_surface(surface,
                                   (w - surface.get_width()) / 2,
                                   (h - surface.get_height()) / 2)
        context.paint_with_alpha(self.alpha)

        context.set_source_rgb(0.4, 0.4, 0.4)
        context.select_font_face("Monospaced",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(FONT_SIZE)
        context.move_to(FONT_SIZE, h - FONT_SIZE)
        context.show_text(self.titles[self.selected_item].rom)

if __name__ == "__main__":
    """
    """
    MainApp()
    gtk.main()
