import os
import signal
import subprocess
import time

from django.core.management.base import BaseCommand
from django.utils import autoreload

import psutil


DELAY_UNTIL_START = 5.0


class Command(BaseCommand):

    help = ''

    def kill_celery(self, parent_pid):
        os.kill(parent_pid, signal.SIGTERM)

    def run_celery(self):
        time.sleep(DELAY_UNTIL_START)
        subprocess.run(self.args)

    def get_main_process(self):
        for process in psutil.process_iter():
            if process.ppid() == 0:  # PID 0 has no parent
                continue

            parent = psutil.Process(process.ppid())

            if process.name() == 'celery' and parent.name() == 'celery':
                return parent

        return

    def reload_celery(self):
        parent = self.get_main_process()

        if parent is not None:
            self.stdout.write('[*] Killing Celery process gracefully..')
            self.kill_celery(parent.pid)

        self.stdout.write('[*] Starting Celery...')
        self.run_celery()

    def add_arguments(self, parser):
        """Добавляет парсер аргументов которые попадут в args метода handle."""

        parser.add_argument(nargs='*', type=str, dest='args', help='')

    def handle(self, *args, **options):
        self.args = args[0].split(' ')
        autoreload.run_with_reloader(self.reload_celery)
