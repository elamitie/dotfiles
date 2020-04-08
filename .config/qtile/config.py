# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import pywal
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

mod = "mod4"
term = "alacritty"
app_launcher = "dmenu_run -c -l 20 -p 'Run: '"
home = os.path.expanduser("~")

keys = [
    Key([mod         ], "Return", lazy.spawn(term)),              # Launch terminal, set by local term variable
    Key([mod, "shift"], "Return", lazy.spawn(app_launcher)),      # Launch application launcher, set by local app_launcher variable
    Key([mod         ], "Tab"   , lazy.next_layout()),            # Cycle through layouts
    Key([mod, "shift"], "c"     , lazy.window.kill()),            # Close the currently highlighed window
    Key([mod, "shift"], "r"     , lazy.restart()),                # Restart qtile
    Key([mod, "shift"], "q"     , lazy.shutdown()),               # Quit qtile
    Key([mod         ], "k"     , lazy.layout.down()),            # Switch between windows in current stack pane
    Key([mod         ], "j"     , lazy.layout.up()),              # Switch between windows in current stack pane
    Key([mod, "shift"], "k"     , lazy.layout.shuffle_down()),    # Move windows down in current stack
    Key([mod, "shift"], "j"     , lazy.layout.shuffle_up()),      # Move windows up in current stack
    Key([mod         ], "h"     , lazy.layout.grow()),            # Grow size of current window (monadtall)
    Key([mod         ], "l"     , lazy.layout.shrink()),          # Shrink size of current window (monadtall)
    Key([mod         ], "n"     , lazy.layout.normalize()),       # Reset window sizes back to default
    Key([mod         ], "m"     , lazy.layout.maximize()),        # Maximize current window
    Key([mod, "shift"], "f"     , lazy.window.toggle_floating()), # Toggle floating window
    Key([mod, "shift"], "space" , lazy.layout.flip()),            # Switch side main panel occupies (monadtall)
]

group_names = [("www",  {'layout': 'monadtall'}),
               ("dev",  {'layout': 'monadtall'}),
               ("chat", {'layout': 'monadtall'}),
               ("game", {'layout': 'floating' }),
               ("spot", {'layout': 'monadtall'}),
               ("vbox", {'layout': 'monadtall'})]
groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod         ], str(i), lazy.group[name].toscreen())) # Switch to another group 
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Move window to another group

# Read in pywal colors from json file, and merge the special and colors sub dictionaries
colors_json = pywal.colors.file(home + "/.cache/wal/colors.json")
colors = colors_json["colors"] 
special = colors_json["special"]
colors.update(special)

layout_theme = { "border_width":  2,
                 "margin":        12,
                 "border_focus":  colors["color5"],  # Replace with pywal color
                 "border_normal": colors["color0"]   # Replace with pywal color
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='Rec Mono Casual',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("config", name="default"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
]

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
