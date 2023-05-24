import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib

from ks_includes.screen_panel import ScreenPanel

def create_panel(*args):
    return SystemPanel(*args)

class SystemPanel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        grid = self._gtk.HomogeneousGrid()
        grid.set_row_homogeneous(False)

        reboot = self._gtk.Button('refresh', _('Restart'), 'color3')
        reboot.connect("clicked", self.reboot_poweroff, "reboot")
        reboot.set_vexpand(True)
        shutdown = self._gtk.Button('shutdown', _('Shutdown'), 'color4')
        shutdown.connect("clicked", self.reboot_poweroff, "poweroff")
        shutdown.set_vexpand(True)

        grid.attach(reboot, 0, 1, 1, 1)
        grid.attach(shutdown, 1, 1, 1, 1)
        self.content.add(grid)

    def restart(self, widget, program):
        if program not in ALLOWED_SERVICES:
            return

        logging.info(f"Restarting service: {program}")
        self._screen._ws.send_method("machine.services.restart", {"service": program})

    def reboot_poweroff(self, widget, method):
        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        if method == "reboot":
            label = Gtk.Label(label=_("Are you sure you wish to reboot the system?"))
        else:
            label = Gtk.Label(label=_("Are you sure you wish to shutdown the system?"))
        vbox.add(label)
        scroll.add(vbox)
        buttons = [
            {"name": _("Host"), "response": Gtk.ResponseType.OK},
            {"name": _("Printer"), "response": Gtk.ResponseType.APPLY},
            {"name": _("Cancel"), "response": Gtk.ResponseType.CANCEL}
        ]
        dialog = self._gtk.Dialog(self._screen, buttons, scroll, self.reboot_poweroff_confirm, method)
        if method == "reboot":
            dialog.set_title(_("Restart"))
        else:
            dialog.set_title(_("Shutdown"))

    def reboot_poweroff_confirm(self, dialog, response_id, method):
        self._gtk.remove_dialog(dialog)
        if response_id == Gtk.ResponseType.OK:
            if method == "reboot":
                os.system("systemctl reboot")
            else:
                os.system("systemctl poweroff")
        elif response_id == Gtk.ResponseType.APPLY:
            if method == "reboot":
                self._screen._ws.send_method("machine.reboot")
            else:
                self._screen._ws.send_method("machine.shutdown")
