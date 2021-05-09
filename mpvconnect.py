import socket
import os
import json

class MPVConnection:
    def __init__(self, conn_type="direct"):
        self.__conn_type = conn_type
        if conn_type == "direct":
            self.__socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        elif conn_type == "network":
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, socket_file="./mpv-ipc.socket", timeout=0.005, host="127.0.0.1", port=4895):
        if self.__conn_type == "direct":
            self.__socket.connect(os.path.abspath(socket_file))
        elif self.__conn_type == "network":
            self.__socket.connect((host, port))

        self.__socket.settimeout(timeout)

    def disconnect(self):
        self.__socket.close()

    def __send_cmd(self, cmd):
        self.__socket.send(f'{cmd}\n'.encode("utf-8"))

        buff = ''

        while True:
            try:
                data = self.__socket.recv(1024)
            except socket.timeout as e:
                break
            buff += data.decode("utf-8")
        return buff

    def __get_prop(self, prop):
        try:
            return json.loads(self.__send_cmd(f'{{ "command": ["get_property", "{prop}"] }}'))["data"]
        except json.decoder.JSONDecodeError:
            return self.__get_prop(prop)

    def __set_prop(self, prop, value):
        str_val = value
        if type(value) == bool:
            str_val = "true" if value else "false"
        if type(value) == str:
            str_val = f'"{value}"'
        self.__send_cmd(f'{{ "command": ["set_property", "{prop}", {str_val}] }}')

    def get_volume(self):
        return self.__get_prop("volume")

    def set_volume(self, value):
        self.__set_prop("volume", value)

    def get_pause(self):
        return self.__get_prop("pause")

    def set_pause(self, value):
        self.__set_prop("pause", value)

    def get_playback(self):
        return {"time":self.__get_prop("time-pos"), "max":self.__get_prop("duration"), "percent":self.__get_prop("percent-pos")}

    def set_playback_time(self, value):
        self.__set_prop("time-pos", value)

    def set_playback_percent(self, value):
        self.set_playback_time(self.get_playback()["max"] / 100 * value)

    def get_playlist(self):
        return self.__get_prop("playlist-pos")

    def set_playlist(self, value):
        self.__set_prop("playlist-pos", value)

    def get_name(self):
       return self.__get_prop("media-title")

