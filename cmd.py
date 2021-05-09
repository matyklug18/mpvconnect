import readline
from mpvconnect import MPVConnection as MPV

mpv = MPV(conn_type="network")
mpv.connect(host="10.0.0.23", timeout=0.1)

while True:
    cmd = input("> ")
    if cmd.startswith("p"):   # pause             
        mpv.set_pause(not mpv.get_pause())
    elif cmd.startswith("v"): # volume
        volume = int(mpv.get_volume())
        if len(cmd) > 1:
            volume = int(eval(cmd[1:], {'v':volume}, {}))
            mpv.set_volume(volume)
        print(f"{volume}%")
    elif cmd.startswith("l"): # playlist
        playlist = int(mpv.get_playlist())
        if len(cmd) > 1:
            playlist = int(eval(cmd[1:], {'l':playlist}, {}))
            mpv.set_playlist(playlist)
        print(f"{playlist}.")
    elif cmd.startswith("s"): # playback (seek)
        playback = mpv.get_playback()
        if len(cmd) > 2:
            result = eval(cmd[2:], {'t':playback["time"], 'p':playback["percent"], 'm':playback["max"]}, {})
            if cmd[1] == 't':
                mpv.set_playback_time(result)
            elif cmd[1] == 'p':
                mpv.set_playback_percent(result)
        playback = mpv.get_playback()
        print(f't:{playback["time"]}s / m:{playback["max"]}s (p:{playback["percent"]}%)')
    elif cmd.startswith("i"):
        print(mpv.get_name())
