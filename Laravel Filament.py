import os
import shlex
import subprocess
import sublime
import sublime_plugin

class LaravelFilamentCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(LaravelFilamentCommand, self).__init__(*args, **kwargs)
        settings = sublime.load_settings('Laravel Filament.sublime-settings')
        self.php_path = settings.get('php_path')
        self.artisan_path = settings.get('artisan_path')

    def run(self, *args, **kwargs):
        try:
            # The first folder needs to be the Laravel Project
            self.PROJECT_PATH = self.window.folders()[0]
            artisan_path = os.path.join(self.PROJECT_PATH, self.artisan_path)
            self.args = [self.php_path, artisan_path]

            if os.path.isfile("%s" % artisan_path):
                self.command = kwargs.get('command', None)
                self.fill_in_accept = kwargs.get('fill_in', False)
                self.fill_in_label = kwargs.get('fill_in_label', 'Enter the resource name')
                self.fill_in_two_accept = kwargs.get('fill_in_two', False)
                self.fill_in_two_label = kwargs.get('fill_in_two_label', 'Enter the resource name')
                self.fill_in_three_accept = kwargs.get('fill_in_three', False)
                self.fill_in_three_label = kwargs.get('fill_in_three_label', 'Enter the resource name')
                self.args = [self.php_path, artisan_path]
                if self.command is None:
                    self.window.show_input_panel('Command name w/o args:', '', self.on_command_custom, None, None)
                else:
                    self.on_command(self.command)
            else:
                sublime.status_message("Artisan not found")
        except IndexError:
            sublime.status_message("Please open a Laravel Project")

    def on_command(self, command):
        self.args.extend(shlex.split(str(self.command)))

        if self.fill_in_accept is True:
            self.window.show_input_panel(self.fill_in_label, "", self.on_fill_in, None, None)
        else:
            self.on_done()

    def on_fill_in(self, fill_in):
        if 'make:filament-user' in self.command:
            self.args.append('--name=' + fill_in)
        else:
            self.args.append(fill_in)

        if self.fill_in_two_accept is True:
            self.window.show_input_panel(self.fill_in_two_label, "", self.on_fill_in_two, None, None)
        else:
            self.on_done()

    def on_fill_in_two(self, fill_in):
        if fill_in != '':
            if 'make:filament-user' in self.command:
                self.args.append('--email=' + fill_in)
            elif 'make:filament-page' in self.command:
                self.args.append('--resource=' + fill_in)
            elif 'make:filament-widget' in self.command:
                self.args.append('--resource=' + fill_in)
            else:
                self.args.append(fill_in)

            if self.fill_in_three_accept is True:
                self.window.show_input_panel(self.fill_in_three_label, "", self.on_fill_in_three, None, None)
            else:
                self.on_done()
        else:
            self.on_done()

    def on_fill_in_three(self, fill_in):
        if fill_in != '':
            if 'make:filament-user' in self.command:
                self.args.append('--password=' + fill_in)
            elif 'make:filament-page' in self.command:
                self.args.append('--type=' + fill_in)
            else:
                self.args.append(fill_in)

            self.on_done()
            sublime.status_message(self.args)
        else:
            self.on_done()

    def on_command_custom(self, command):
        self.args.extend(shlex.split(str(command)))
        self.on_done()

    def on_done(self):
        if os.name != 'posix':
            self.args = subprocess.list2cmdline(self.args)
        try:
            self.window.run_command("exec", {
                "cmd": self.args,
                "shell": os.name == 'nt',
                "working_dir": self.PROJECT_PATH})
        except IOError:
            sublime.status_message('IOError - command aborted')