__author__ = 'Tymoteusz Paul'
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class WatchBuilder(FileSystemEventHandler):
    def on_any_event(self, event):
        filename = str(event.src_path.decode('utf-8')) # Ugly workaround but it will work with both 2.7 and 3.3
        extension = os.path.splitext(filename)[1]
        if extension == '.nasm':
            os.system('nasm -f elf %s 2>&1' % filename)
        elif extension == '.o':
            os.system('ld -m elf_i386 -s -o %s %s 2>&1 &> /dev/null' % (filename[:-2], filename))
        elif extension == '.c':
            os.system('cc -mpreferred-stack-boundary=2 -fno-stack-protector -ggdb %s -o %s'
                      % (filename, filename[:-2]))
            os.system('execstack -s %s' % filename[:-2])

if __name__ == '__main__':
    event_handler = WatchBuilder()
    observer = Observer()
    observer.schedule(event_handler, BASEDIR, recursive=True)
    observer.start() # Starts a loop over events, to quit just mash ctrl-c