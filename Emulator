import argparse
import zipfile
import os
import sys
from vfs import VirtualFileSystem

class ShellEmulator:
    def __init__(self, username, hostname, fs_archive, startup_script=None):
        self.username = username
        self.hostname = hostname
        self.fs = VirtualFileSystem(fs_archive)
        self.current_dir = "/"
        self.startup_script = startup_script

    def run_startup_script(self):
        if self.startup_script is not None:
            with self.fs.open(self.startup_script, 'r') as f:
                for line in f:
                    self.execute(line.strip())

    def prompt(self):
        return f"{self.username}@{self.hostname}:{self.current_dir}$ "

    def execute(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "ls":
            self.ls(*args)
        elif cmd == "cd":
            self.cd(*args)
        elif cmd == "exit":
            sys.exit(0)
        elif cmd == "head":
            self.head(*args)
        elif cmd == "pwd":
            self.pwd()
        elif cmd == "cp":
            self.cp(*args)
        else:
            print(f"Command '{cmd}' not found.")

    def ls(self, *args):
        path = args[0] if args else "."
        entries = self.fs.list_dir(path)
        for entry in sorted(entries):
            print(entry)

    def cd(self, *args):
        if not args:
            print("Usage: cd <directory>")
            return
        path = args[0]
        if self.fs.is_directory(path):
            self.current_dir = path
        else:
            print(f"Directory '{path}' does not exist.")

    def head(self, *args):
        if not args:
            print("Usage: head <file> [number_of_lines]")
            return
        filename = args[0]
        num_lines = int(args[1]) if len(args) > 1 else 10
        try:
            with self.fs.open(filename, 'r') as f:
                for i, line in enumerate(f):
                    if i >= num_lines:
                        break
                    print(line.strip())
        except FileNotFoundError:
            print(f"File '{filename}' does not exist.")

    def pwd(self):
        print(self.current_dir)

    def cp(self, source, destination):
        if not self.fs.exists(source):
            print(f"Source file '{source}' does not exist.")
            return
        if not self.fs.is_regular_file(destination):
            print(f"Destination file '{destination}' is not a regular file.")
            return
        with self.fs.open(source, 'rb') as infile:
            data = infile.read()
        with self.fs.open(destination, 'wb') as outfile:
            outfile.write(data)
        print(f"Successfully copied '{source}' to '{destination}'.")

    def start(self):
        self.run_startup_script()
        while True:
            try:
                command = input(self.prompt())
                if command:
                    self.execute(command)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break

def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("-u", "--username", help="Username to display in the prompt.", required=True)
    parser.add_argument("-h", "--hostname", help="Hostname to display in the prompt.", required=True)
    parser.add_argument("-f", "--fs-archive", help="Path to the archive containing the virtual filesystem.", required=True)
    parser.add_argument("-s", "--startup-script", help="Path to the startup script inside the virtual filesystem.")
    args = parser.parse_args()

    emulator = ShellEmulator(args.username, args.hostname, args.fs_archive, args.startup_script)
    emulator.start()

if __name__ == "__main__":
    main()
