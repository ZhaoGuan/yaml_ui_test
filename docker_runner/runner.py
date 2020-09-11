#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import docker
import socket


def port_check(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", port))
        print(port)
        return port_check(port + 1)
    except OSError:
        return port
    finally:
        s.close()


class DockerBrowser:
    def __init__(self):
        self.chrome_image = "selenium/standalone-chrome-debug"
        self.firefox_image = "selenium/standalone-firefox-debug"
        self.opera_image = "selenium/standalone-opera-debug"
        self.docker = docker.from_env()
        self.docker_id = None
        self.base_port = 4444
        self.vnc_base_port = 5900

    def run(self):
        port = port_check(self.base_port)
        vnc_port = port_check(self.vnc_base_port)
        try:
            docker_id = self.docker.containers.run(self.chrome_image,
                                                   # environment={
                                                   # "HTTP_PROXY": "http://192.168.84.168:8899",
                                                   # "HTTPS_PROXY": "http://192.168.84.168:8899",
                                                   # "http_proxy": "http://192.168.84.168:8899",
                                                   # "https_proxy": "http://192.168.84.168:8899"
                                                   # },
                                                   ports={"4444": str(port), "5900": str(vnc_port)},
                                                   remove=True,
                                                   detach=True).id
            self.docker_id = docker_id
            print("Docker id:", docker_id, 'VNC port:', vnc_port, "VNC password: secret")
            return port
        except Exception as e:
            print(e)
            assert False, "Browser启动失败"

    def browser_status(self):
        return self.docker.containers.get(self.docker_id).status

    def browser_close(self):
        container = self.docker.containers.get(self.docker_id)
        container.kill()
