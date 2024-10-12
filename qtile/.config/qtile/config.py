from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import hook
import os
import subprocess
from typing import List
from libqtile.widget import base

class TaskWidget(widget.base._TextBox):
    """
    Custom Qtile widget to display the number of task from Taskwarrior.
   """
    orientations = widget.base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 60, "Update interval in seconds."),
        ("markup", True, "Enable/disable Pango markup."),
    ]
    def __init__(self, **config):
        widget.base._TextBox.__init__(self, "", **config)
        self.add_defaults(TaskWidget.defaults)
        self.text = "init"
        self.add_callbacks({"Button1":lazy.spawn("rofi -modi tasks:rofi-taskwarrior -show tasks")})
    def update(self):
        try:
            command = ["/usr/bin/task","+PENDING","count"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            task_output = result.stdout.strip()
            if task_output:
                self.text = task_output + " Task(s)"
            else:
                self.text = "No tasks"
        except subprocess.CalledProcessError as e:
            self.text = f"Error: {e}"
    def tick(self):
        self.update()
    def timer_setup(self):
        self.update()
        self.timeout_add(self.update_interval,self.update)
           



mod = "mod1"
terminal = "kitty"

keys = [
# Window Management
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", 
        lazy.layout.shuffle_left().when(layout='columns'),
        lazy.layout.swap_left().when(layout='monadtall'),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", 
        lazy.layout.shuffle_right().when(layout='columns'),
        lazy.layout.swap_right().when(layout='monadtall'), 
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", 
        lazy.layout.grow_left().when(layout='columns'),
        lazy.layout.shrink().when(layout='monadtall'), 
        desc="Grow window to the left"),
    Key([mod, "control"], "l", 
        lazy.layout.grow_right().when(layout='columns'),
        lazy.layout.grow().when(layout='monadtall'), 
        desc="Grow window to the right"),
    Key([mod, "control"], "j", 
        lazy.layout.grow_down().when(layout='columns'), desc="Grow window down"),
    Key([mod, "control"], "k", 
        lazy.layout.grow_up().when(layout='columns'), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "period", lazy.next_screen(),desc="Next Monitor"),
    Key([mod, "shift"], "Return", 
        lazy.layout.toggle_split(), 
        desc="Toggle between split and unsplit sides of stack"),
# App & Menu Spawning Keybindings 
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "z", lazy.group['ScratchPad'].dropdown_toggle('term')),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "d", lazy.spawn("rofi -show drun"),desc="Rofi"),
    Key([mod], "p", lazy.spawn("rofi-pass"), desc="Password Manager"),
    Key([mod], "q", lazy.spawn("i3lock-fancy-dualmonitor"),desc="lock screen"),
    Key([mod, "shift"], "a", lazy.window.kill(), desc="Kill focused Window"),
    Key([mod, "shift"], "c", lazy.spawn("killall picom"), desc="Close Compositor"),
    Key([mod], "m", 
        lazy.spawn("/usr/bin/kitty -e neomutt"),desc="Launch neomutt"), 
    Key([mod], "c", 
        lazy.spawn("/home/corecaps/scripts/rofi_comics.sh"), 
        desc="read comics"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

groups = []
group_names = ["1","2","3","4","5","6","7","8","9","0"]
group_labels = ["1-󰖟","2-","3-","4-","5-","6-","7-","8-","9-","0-󰙯"]
group_layouts = ["max","monadtall","columns","columns","columns","columns","columns","columns","max","max"]

for i in range(len(group_names)):
#Groups 1 & 2 spawn their apps at startup
    if (i == 0):
        groups.append(
            Group(
                name=group_names[i],
                layout=group_layouts[i],
                label=group_labels[i],
                spawn='/usr/bin/google-chrome-stable'
            )
        )
    elif (i == 1):
        groups.append(
            Group(
                name=group_names[i],
                layout=group_layouts[i],
                label=group_labels[i],
                spawn='/usr/bin/kitty'
            )
        )
    else :
        groups.append(
            Group(
                name=group_names[i],
                layout = group_layouts[i],
                label=group_labels[i]
            )
        )
    keys.extend(
        [
            Key(
                [mod],
                group_names[i],
                lazy.group[group_names[i]].toscreen(),
                desc="Switch to group {}".format(group_names[i])
            ),
            Key(
                [mod,"shift"],
                group_names[i],
                lazy.window.togroup(group_names[i],switch_group=True),
                desc="Switch to & move focused window to group {}".format(group_names[i])
            )
        ]
    )

groups.append(
        ScratchPad("ScratchPad", [
            DropDown("term", "kitty", opacity=0.8, height = 0.25, width=0.9,x=0.05)
            ])
        )
layouts = [
        layout.Columns(
            border_focus_stack="#6c8e93",
            border_focus="#6c8e93",
            border_normal="#952d29",
            border_on_single="#6c8e93", 
            border_width=5,
            margin=15,
            margin_on_single=[5,0,5,0]),
    layout.Max(
            border_focus_stack="#6c8e93",
            border_focus="#6c8e93",
            border_normal="#952d29",
            border_on_single="#6c8e93", 
            border_width=2,
            margin=15,
            margin_on_single=[5,0,5,0]),
   layout.MonadTall(
        border_focus_stack="#6c8e93",
        border_focus="#6c8e93",
        border_normal="#952d29",
        border_on_single="#6c8e93", 
        border_width=2,
        margin=15,
        margin_on_single=[5,0,5,0]),
    layout.MonadWide(
        border_focus_stack="#6c8e93",
        border_focus="#6c8e93",
        border_normal="#952d29",
        border_on_single="#6c8e93", 
        border_width=2,
        margin=15,
        margin_on_single=[5,0,5,0]),
   layout.Zoomy(
        border_focus_stack="#6c8e93",
        border_focus="#6c8e93",
        border_normal="#952d29",
        border_on_single="#6c8e93", 
        border_width=2,
        margin=15,
        margin_on_single=[5,0,5,0]),
]

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=11,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
# First Screen (main)
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=20
                    ),
                widget.Sep(
                    background = "#952d29",
                    linewidth=0,
                    padding=6
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Image(
                    filename = "/home/corecaps/.config/qtile/arch_new.png",
                    scale = "False",
                    background = "#952d29"
                ),
                widget.Sep(
                    background = "#142127",
                    linewidth=0,
                    padding=6
                ),
               widget.GroupBox(
                    active="#6c8e93",
                    highlight_color="#ae595e",
                    background = "#142127",
                    other_current_screen_border="952d29",
                    #other_screen_border="#6c8e93",
                    hide_unused = True,
                    border_color = "#6c8e93",
                    fontsize=16,
                    highlight_method="block"
                ),
                widget.TextBox(
                    text=' ',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.TaskList(
                   foreground="#6c8e93"
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.CurrentLayoutIcon(
                    background="#122127",
                    foreground="#6c8e93"
                ),
               widget.CurrentLayout(
                    background="#122127",
                    foreground="#6c8e93"
                ),
                widget.TextBox(
                    text=' ',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                ),
               widget.ThermalZone(
                    format=" {temp}°C",
                    fgcolor_normal="#e3dadd",
                    fgcolor_high="#e3dadd",
                    fgcolor_crit="#e3dadd",
                    background="#952d29",
                    zone="/sys/class/thermal/thermal_zone0/temp"
                ),
                widget.TextBox(
                    text='',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                ),
               widget.Memory(
                    format="󰡴 {MemUsed: .0f}{mm}",
                    background="#122127",
                    foreground="#6c8e93",
                    interval=1.0
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
               widget.NetGraph(
                    format=" {interface}: {down} ↓↑ {up}",
                    type="line",
                    background="#952d29",
                    foreground="#6c8e93",
                    graph_color = "#6c8e93",
                    fill_color = "#6c8e93",
                    border_width = 0,
                    update_interval=1.0
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Clock(
                    background="#122127",
                    foreground="#6c8e93",
                    format=" %H:%M - %d/%m/%Y",
                    update_interval=60.0
                ),
                widget.TextBox(
                    text='',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                ),
                widget.Systray(),
                widget.QuickExit(
                    default_text="",
                    fontsize=16,
                    foreground="#6c8e93",
                    timer_interval=0,
                    countdown_format="拉"
                ),
                widget.Spacer(
                    length=5
                    ),
                widget.Sep(
                    background = "#952d29",
                    linewidth=0,
                    padding=2
                ),
                widget.TextBox(
                    text='',
                    background="#122127",
                    foreground="#952d29",
                    padding=0,
                    fontsize=23
                )
            ],
            23,
            background="#952d29",
            opacity=0.75
        ),
    bottom = bar.Bar([
               widget.TextBox(
                   text='',
                    foreground="#952d29",
                    background="#142127",
                    padding=0,
                    fontsize=23
                ),
                widget.TextBox(
                    text = ".::Nerdistan|Home::.",
                    background="#952d29",
                    foreground="#6c8e93",
                    padding=7
                ),
                widget.Backlight(
                    foreground="#6c8e93",
                    fmt='󰳲 {}'
                ),
                widget.TextBox(
                    text='',
                    foreground="#952d29",
                    background="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.TextBox(
                    text='󰀂 ',
                    foreground="6c8e93",
                    background="122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Wlan(
                    foreground="6c8e93",
                    background="122127",
                    interface='wlp3s0',
                    format='{essid} {percent:2.0%}'
                    ),
                widget.Spacer(
                    length=100,
                    background="#122127"
                    ),
                widget.TextBox(
                    text='',
                    background="#122127",
                    foreground="#952d29",
                    padding=0,
                    fontsize=23
                ),
                widget.Pomodoro(
                    background="#952d29",
                    color_inactive="#6c8e93",
                    padding=4
                ),                
                widget.Spacer(
                    length=200,
                    foreground="#122127"
                ),
                widget.TextBox(
                    text='',
                    background="#122127",
                    foreground="#952d29",
                    padding=0,
                    fontsize=23
                ),
                widget.KhalCalendar(
                    foreground="#6c8e93",
                    background="#122127",
                    width=300,
                    scroll=True,
                    scroll_fixed_width=300,
                    scroll_interval=0.1,
                    scroll_repeat=True,
                    scroll_step=2,
                    update_interval=1000
                ),
                widget.Spacer(
                    length=100,
                    background="#122127"
                ),
                widget.TextBox(
                    text='',
                    foreground="#952d29",
                    background="#122127",
                    padding=0,
                    fontsize=23
                ),
                TaskWidget(
                    foreground="#6c8e93",
                    background="#952d29"
                ),
                widget.Battery(
                    charge_char='󱎗',
                    discharge_char='󱟤',
                    fmt='Battery: {}',
                    background="#952d29",
                    foreground="6c8e93",
                    format="{char} {percent:2.0%}"
                    )
                ],
            23,
            background="#952d29",
            opacity=0.60
        )
),
# Second Screen (HDMI1)
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=20
                    ),
                widget.Sep(
                    background = "#952d29",
                    linewidth=0,
                    padding=6
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Image(
                    filename = "/home/corecaps/.config/qtile/arch_new.png",
                    scale = "False",
                    background = "#952d29"
                ),
                widget.Sep(
                    background = "#142127",
                    linewidth=0,
                    padding=6
                ),
               widget.GroupBox(
                    active="#6c8e93",
                    highlight_color="#ae595e",
                    background = "#142127",
                    other_current_screen_border="952d29",
                    hide_unused = True,
                    border_color = "#6c8e93",
                    fontsize=16,
                    highlight_method="block"
                ),
                widget.TextBox(
                    text=' ',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.TaskList(
                    foreground="#6c8e93"
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.CurrentLayoutIcon(
                    background="#122127",
                    foreground="#6c8e93"
                ),
               widget.CurrentLayout(
                    background="#122127",
                    foreground="#6c8e93"
                ),
                widget.TextBox(
                    text=' ',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                ),
               widget.ThermalZone(
                    format=" {temp}°C",
                    fgcolor_normal="#e3dadd",
                    fgcolor_high="#e3dadd",
                    fgcolor_crit="#e3dadd",
                    background="#952d29",
                    zone="/sys/class/thermal/thermal_zone0/temp"
                ),
                widget.TextBox(
                    text='',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                ),
               widget.Memory(
                    format="󰡴 {MemUsed: .0f}{mm}",
                    background="#122127",
                    foreground="#6c8e93",
                    interval=1.0
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
               widget.NetGraph(
                    format=" {interface}: {down} ↓↑ {up}",
                    type="line",
                    background="#952d29",
                    foreground="#6c8e93",
                    graph_color = "#6c8e93",
                    fill_color = "#6c8e93",
                    border_width = 0,
                    update_interval=1.0
                ),
                widget.TextBox(
                    text='',
                    background="#952d29",
                    foreground="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Clock(
                    background="#122127",
                    foreground="#6c8e93",
                    format=" %H:%M - %d/%m/%Y",
                    update_interval=60.0
                ),
                widget.TextBox(
                    text='',
                    foreground="#122127",
                    background="#952d29",
                    padding=0,
                    fontsize=23
                )
           ],
            23,
            background="#952d29",
            opacity=0.75
        ),
    bottom = bar.Bar([
               widget.TextBox(
                   text='',
                    foreground="#952d29",
                    background="#142127",
                    padding=0,
                    fontsize=23
                ),
                widget.TextBox(
                    text = ".::Nerdistan|Home::.",
                    background="#952d29",
                    foreground="#6c8e93",
                    padding=7
                ),

                widget.Spacer(
                    length=200
                ),
                widget.TextBox(
                    text='',
                    foreground="#952d29",
                    background="#122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Spacer(
                    background='#122127',
                    length=40
                ),
                widget.TextBox(
                    text='󰀂 ',
                    foreground="6c8e93",
                    background="122127",
                    padding=0,
                    fontsize=23
                ),
                widget.Net(
                    foreground="6c8e93",
                    background="122127"
                    ),
                widget.TextBox(
                    text='',
                    fontsize=20,
                    background='#122127',
                    foreground='#6c8e93'
                ),
                widget.Wttr(
                    format='%c %C - %t(%f) - %m - %p',
                    foreground="#6c8e93",
                    background="#122127",
                    fontsize=12
                ),
                widget.Spacer(
                    length=150,
                    background="#122127"
                    ),
                widget.TextBox(
                    text='',
                    background="#122127",
                    foreground="#952d29",
                    padding=0,
                    fontsize=23
                ),
                widget.Spacer(
                    length=100,
                    foreground="#122127",

                ),
                 widget.Mpd2(
                    background="#952d29",
                    color_inactive="#6c8e93",
                    padding=4
                ),                
                widget.Spacer(
                    length=100,
                    foreground="#122127",

                ),
                widget.TextBox(
                    text='',
                    background="#122127",
                    foreground="#952d29",
                    padding=0,
                    fontsize=23
                ),
                widget.Spacer(
                    length=100,
                    background="122127"
                ),
                widget.TextBox(
                    text='',
                    foreground="#952d29",
                    background="#122127",
                    padding=0,
                    fontsize=23
                ),
                TaskWidget(
                    foreground="#6c8e93",
                    background="#952d29"
                ),
                widget.Battery(
                    charge_char='󱎗',
                    discharge_char='󱟤',
                    fmt='Battery:{}',
                    #background="#122127",
                    foreground="6c8e93",
                    format="{char} {percent:2.0%}"
                )
            ],
            23,
            background="#952d29",
            opacity=0.60
        )
    )
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.startup_once
def autostart():
    processes = [
            ['/usr/bin/pasystray'],
            ['/usr/bin/nm-applet'],
            ['/usr/bin/cbatticon'],
            ['/usr/bin/dunst'],
            ['/home/corecaps/scripts/tablette_config.sh'],
            ['/usr/bin/feh','--bg-scale','/home/corecaps/wallpapers/a_black_and_white_image_of_a_room.jpeg','/home/corecaps/wallpapers/a_black_and_white_drawing_of_a_large_metal_structure.jpg'],
            ['/usr/bin/picom','-b','--conf','/home/corecaps/.config/picom/picom.conf']
            ]
    for p in processes:
        subprocess.Popen(p)

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
