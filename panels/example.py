import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

from ks_includes.KlippyGtk import KlippyGtk
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.screen_panel import ScreenPanel

class ExamplePanel(ScreenPanel):
    def initialize(self, panel_name):
        _ = self.lang.gettext
        # Create gtk items here
        return