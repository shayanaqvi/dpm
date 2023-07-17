from client import client
from currently_playing import queue
from info_panel import info_panel
from cs import cs
from Colours import colours
import os

from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


console = Console()


def generate_layout():
    # left table
    ltable = Table(
        expand=True,
        box=box.SIMPLE,
        style=colours["accent1"]
    )
    ltable.add_column(
        "#",
        style=colours["accent1"],
        header_style=colours["accent1"]
    )
    ltable.add_column(
        "Toggles",
        header_style=colours["accent1"]
    )

    # middle table
    mtable = Table(
        expand=True,
        box=box.SIMPLE,
        style=colours["accent1"]
    )
    mtable.add_column("#", style=colours["accent1"], header_style=colours["accent1"])
    mtable.add_column(
        "Playlist",
        header_style=colours["accent1"]
    )

    # right table
    rtable = Table(
        expand=True,
        box=box.SIMPLE,
        style=colours["accent1"]
    )
    rtable.add_column("#", style=colours["accent1"], header_style=colours["accent1"])
    rtable.add_column(
        "Playback",
        header_style=colours["accent1"]
    )
    # layout
    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="middle"),
        Layout(name="right")
    )

    # layout size
    _width, _height = os.get_terminal_size()
    console.size = (_width, 9)

    lstrings = [
        "Toggle Repeat",
        "Toggle Random",
        "Toggle Consume",
        "Toggle Single",
        "Toggle Playback",
    ]

    mstrings = [
        "Clear",
        "Crop",
    ]

    rstrings = [
        "Shuffle Playlist",
        "Previous Track",
        "Next Track",
        "Stop Playback",
    ]

    display_index = 1
    for item in lstrings:
        ltable.add_row(str(display_index), item)
        display_index += 1

    for item in mstrings:
        mtable.add_row(str(display_index), item)
        display_index += 1

    for item in rstrings:
        rtable.add_row(str(display_index), item)
        display_index += 1

    # add to layout
    layout["left"].split(
        Layout(
                ltable,
        )
    )
    layout["middle"].split(
        Layout(
                mtable,
        )
    )
    layout["right"].split(
        Layout(
                rtable,
        )
    )

    return layout


def playlist_options(cli_arguments):
    current_level = 1
    match len(cli_arguments):
        case 2:
            cs()
            while True:
                match current_level:
                    case 1:
                        console.print(generate_layout())
                        info_panel("⟵ Ctrl+c to exit", "information")
                        current_level += 1
                    case 2:
                        try:
                            operation = input("Do: ")
                            handle_input(operation, "app")
                        except (KeyboardInterrupt, EOFError):
                            cs()
                            return
                    case _:
                        pass
        case 3:
            handle_input(cli_arguments, "cli")


def handle_input(user_input, access_type):
    confirmation = ""
    status = client.status()

    repeat_tgl = 1 if status["repeat"] == "1" else 0
    random_tgl = 1 if status["random"] == "1" else 0
    consume_tgl = 1 if status["consume"] == "1" else 0
    single_tgl = 1 if status["single"] == "1" else 0

    match access_type:
        case "app":
            while True:
                if len(user_input) <= 11:
                    match user_input:
                        case "1":
                            repeat_tgl ^= 1
                            client.repeat(repeat_tgl)
                            confirmation = "Repeat is on" if repeat_tgl == 1 else "Repeat is off"
                            info_panel(confirmation, "affirmative")
                            break
                        case "2":
                            random_tgl ^= 1
                            client.random(random_tgl)
                            confirmation = "Random mode is on" if random_tgl == 1 else "Random mode is off"
                            info_panel(confirmation, "affirmative")
                            break
                        case "3":
                            consume_tgl ^= 1
                            client.consume(consume_tgl)
                            confirmation = "Consume is on" if consume_tgl == 1 else "Consume is off"
                            info_panel(confirmation, "affirmative")
                            break
                        case "4":
                            single_tgl ^= 1
                            client.single(single_tgl)
                            confirmation = "Single mode is on" if single_tgl == 1 else "Single mode is off"
                            info_panel(confirmation, "affirmative")
                            break
                        case "5":
                            # check if toggle is needed
                            client.pause()
                            info_panel("Playback toggled", "affirmative")
                            break
                        case "6":
                            client.clear()
                            info_panel("Playlist cleared", "affirmative")
                            break
                        case "7":
                            playlist = queue()
                            status = client.status()
                            current_song = playlist["current song"]
                            current_song_progress = status["elapsed"]
                            client.clear()
                            client.add(current_song["file"])
                            client.seek(0, current_song_progress)
                            client.play()
                            break
                        case "8":
                            client.shuffle()
                            info_panel("Shuffled", "affirmative")
                            break
                        case "9":
                            client.previous()
                            info_panel("Playing previous song", "affirmative")
                            break
                        case "10":
                            client.next()
                            info_panel("Playing next song", "affirmative")
                            break
                        case "11":
                            client.stop()
                            info_panel("Playback stopped", "affirmative")
                            break
                        case _:
                            info_panel("Invalid selection", "error")
                            break
                else:
                    info_panel("Invalid selection", "error")
                    break
        case "cli":
            while True:
                match user_input[2]:
                    case "r":
                        repeat_tgl ^= 1
                        client.repeat(repeat_tgl)
                        confirmation = "Repeat is on" if repeat_tgl == 1 else "Repeat is off"
                        info_panel(confirmation, "affirmative")
                        break
                    case "z":
                        random_tgl ^= 1
                        client.random(random_tgl)
                        confirmation = "Random mode is on" if random_tgl == 1 else "Random mode is off"
                        info_panel(confirmation, "affirmative")
                        break
                    case "a":
                        consume_tgl ^= 1
                        client.consume(consume_tgl)
                        confirmation = "Consume is on" if consume_tgl == 1 else "Consume is off"
                        info_panel(confirmation, "affirmative")
                        break
                    case "o":
                        single_tgl ^= 1
                        client.single(single_tgl)
                        confirmation = "Single mode is on" if single_tgl == 1 else "Single mode is off"
                        info_panel(confirmation, "affirmative")
                        break
                    case "t":
                        # check if toggle is needed
                        # start playback if it hasn't started yet
                        client.pause()
                        info_panel("Playback toggled", "affirmative")
                        break
                    case "s":
                        client.shuffle()
                        info_panel("Shuffled", "affirmative")
                        break
                    case "p":
                        client.previous()
                        info_panel("Playing previous song", "affirmative")
                        break
                    case "n":
                        client.next()
                        info_panel("Playing next song", "affirmative")
                        break
                    case "x":
                        client.stop()
                        info_panel("Playback stopped", "affirmative")
                        break
                    case "e":
                        client.clear()
                        info_panel("Playlist cleared", "affirmative")
                        break
                    case "c":
                        playlist = queue()
                        status = client.status()
                        current_song = playlist["current song"]
                        current_song_progress = status["elapsed"]
                        client.clear()
                        client.add(current_song["file"])
                        client.seek(0, current_song_progress)
                        client.play()
                        break
                    case _:
                        info_panel("Invalid operation", "error")
                        break
