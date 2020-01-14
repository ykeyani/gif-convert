#  Copyright (c) 2020. Yasin Keyani
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser
import ntpath
import subprocess


def fps_to_ms(fps: int) -> int:
    return int(1000.0/fps)


def fps_to_hs(fps: int) -> int:
    return int(fps_to_ms(fps) / 10)


class App:
    def __init__(self) -> None:
        super().__init__()

        self.root = Tk()

        # application vars
        self.file_paths = []
        self.frames = []
        self.frame_rate = IntVar()
        self.disposal = StringVar()
        self.optimization = StringVar()
        self.scale = IntVar(value=100)
        # self.background = StringVar(value="")

        # child frames
        self.window = ttk.Frame(self.root, padding=8)
        self.import_frame = ImportFrame(self.window, self)
        self.export_frame = ExportFrame(self.window, self)
        self.import_controls = ImportControls(self.window, self)
        self.export_controls = ExportControls(self.window, self)

        self._layout()
        self._key_bindings()

    def _layout(self):
        self.window.pack(expand=True, fill="both")
        self.import_frame.grid(column=0, row=0, sticky=(W, N, E, S))
        self.export_frame.grid(column=1, row=0, sticky=(W, N, E, S))
        self.import_controls.grid(column=0, row=1, sticky=(W,))
        self.export_controls.grid(column=1, row=1, sticky=(E,))

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)

    def _key_bindings(self):
        self.root.bind("<Delete>", self.delete_images)
        self.root.bind("<BackSpace>", self.delete_images)

    def run(self):
        self.root.mainloop()

    def import_images(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            try:
                if file_path in self.file_paths:
                    continue
                self.file_paths.append(file_path)
                self.import_frame.file_list.insert("end", ntpath.basename(file_path))
            except EXCEPTION:
                continue

    def clear_images(self):
        self.file_paths = []
        self.frames = []
        self.import_frame.file_list.delete(0, "end")

    def delete_images(self, *args):
        selections = self.import_frame.file_list.curselection()
        if len(selections) >= 1:
            selections = sorted(selections, reverse=True)
            for selection in selections:
                self.import_frame.file_list.delete(selection)
                del self.frames[selection]
                del self.file_paths[selection]

    def save_images(self):
        output_file_name = filedialog.asksaveasfilename()
        if not output_file_name or len(output_file_name) == 0:
            return
        if output_file_name[-4:] != ".gif":
            output_file_path = f"{output_file_name}.gif"
        else:
            output_file_path = output_file_name

        import os
        if os.name == 'posix':  # mac / linux
            convert_cmd = "convert"
            gifsicle_cmd = "gifsicle"
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            convert_cmd = ntpath.join(base_path, "bin", "imagemagick", "convert.exe")
            gifsicle_cmd = ntpath.join(base_path, "bin", "gifsicle", "gifsicle.exe")

        try:
            convert_add = []

            result = subprocess.run(
                [convert_cmd,
                 "-delay", str(fps_to_hs(self.frame_rate.get())),
                 "-loop", str(0),
                 "-dispose", self.disposal.get()[:1]] + convert_add +
                self.file_paths + [output_file_path]
            )
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            messagebox.showerror(message=f"Imagemagick conversion failed: {e}")
            return

        try:
            gifsicle_add = []
            if int(self.scale.get()) != 100:
                gifsicle_add += [
                    "--scale", f"{int(self.scale.get())/100.0:.4f}"
                ]

            result = subprocess.run(
                [gifsicle_cmd,
                 "-b",
                 f"-{self.optimization.get()[:2]}",
                 # "--colors", "256"
                 ] + gifsicle_add + [
                    output_file_path
                ]
            )
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            messagebox.showerror(message=f"gifsicle processing failed: {e}")
            return

    def select_background(self):
        background = colorchooser.askcolor(initialcolor="#ffffff")[1]
        if background and len(background) > 1:
            self.background.set(background)
        else:
            self.clear_background()

    def clear_background(self):
        self.background.set("")


class AppFrame(ttk.Frame):
    def __init__(self, master, app: App, **kw):
        super().__init__(master, **kw)
        self.app = app


class ImportFrame(AppFrame):
    def __init__(self, master, app: App, **kw):
        super().__init__(master, app, **kw)

        self.file_list = Listbox(self, height=10, selectmode=EXTENDED)
        self.file_scroll = Scrollbar(self, orient=VERTICAL, command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=self.file_scroll.set)

        self.layout()

    def layout(self):
        self.file_list.grid(column=0, row=0, sticky=(W, N, E, S))
        self.file_scroll.grid(column=1, row=0, sticky=(N, S))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class ImportControls(AppFrame):
    def __init__(self, master, app: App, **kw):
        super().__init__(master, app, **kw)

        self.import_button = ttk.Button(self, text="Import", command=self.app.import_images)
        self.delete_button = ttk.Button(self, text="Delete", command=self.app.delete_images)
        self.clear_button = ttk.Button(self, text="Clear", command=self.app.clear_images)

        self.layout()

    def layout(self):
        self.import_button.grid(column=0, row=0)
        self.delete_button.grid(column=1, row=0)
        self.clear_button.grid(column=2, row=0)


class ExportFrame(AppFrame):
    def __init__(self, master, app: App, **kw):
        super().__init__(master, app, **kw)

        # controls
        self.fps_label = ttk.Label(self, text="Framerate: ")
        self.fps_select = ttk.Combobox(self, textvariable=self.app.frame_rate,
                                       values=tuple(fps for fps in range(24, 31)))
        self.disposal_label = ttk.Label(self, text="Disposal: ")
        self.disposal_select = ttk.Combobox(self, textvariable=self.app.disposal,
                                            values=(
                                                "0: None Specified",
                                                "1: Do not dispose",
                                                "2: Restore to background color",
                                                "3: Restore to previous content"
                                            ))

        self.optimize_label = ttk.Label(self, text="Optimisation: ")
        self.optimize_select = ttk.Combobox(self, textvariable=self.app.optimization,
                                            values=(
                                                "O1: Store Changes",
                                                "O2: Shrink using transparency",
                                                "O3: Excessive"
                                            ))

        # self.colour_label = ttk.Label(self, textvariable=self.app.background)
        # self.colour_select = ttk.Button(self, text="Background...", command=self.app.select_background)
        # self.colour_clear = ttk.Button(self, text="Clear...", command=self.app.clear_background)

        self.scale_label = ttk.Label(self, text="Scale: ")
        self.scale = ttk.Scale(self, from_=1, to=200, variable=self.app.scale, command=self.update_scale)
        self.scale_value = ttk.Label(self, text="100")

        # default values
        self.fps_select.current(0)
        self.disposal_select.current(2)
        self.optimize_select.current(0)
        self.app.scale.set(100)

        self.layout()

    def layout(self):
        self.fps_label.grid(column=0, row=1, sticky=(W,))
        self.fps_select.grid(column=1, row=1, sticky=(W,), columnspan=2)
        self.disposal_label.grid(column=0, row=2, sticky=(W,))
        self.disposal_select.grid(column=1, row=2, sticky=(W,), columnspan=2)
        self.optimize_label.grid(column=0, row=3, sticky=(W,))
        self.optimize_select.grid(column=1, row=3, sticky=(W,), columnspan=2)
        # self.colour_label.grid(column=0, row=4, sticky=(W, E))
        # self.colour_select.grid(column=1, row=4, sticky=(W,))
        # self.colour_clear.grid(column=2, row=4, sticky=(W,))
        self.scale_label.grid(column=0, row=5, sticky=(W,))
        self.scale.grid(column=1, row=5, sticky=(W, E), columnspan=1)
        self.scale_value.grid(column=2, row=5, sticky=(W,))

    def update_scale(self, *ign):
        self.scale_value["text"] = int(self.app.scale.get())


class ExportControls(AppFrame):
    def __init__(self, master, app: App, **kw):
        super().__init__(master, app, **kw)

        self.save_button = ttk.Button(self, text="Save", command=self.app.save_images)

        self.layout()

    def layout(self):
        self.save_button.grid(column=0, row=0)


if __name__ == "__main__":
    application = App()
    application.run()
