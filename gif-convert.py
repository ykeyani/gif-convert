from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ntpath


def fps_to_ms(fps: int):
    return int(1000.0/fps)


class App:
    def __init__(self) -> None:
        super().__init__()

        self.root = Tk()

        # application vars
        self.file_paths = []
        self.frames = []
        self.frame_rate = IntVar()
        self.transparency = IntVar()
        self.disposal = StringVar()

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
                self._add_frame(file_path)
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
        if output_file_name[-4:] != ".gif":
            output_file_path = f"{output_file_name}.gif"
        else:
            output_file_path = output_file_name

        imageio.mimsave(output_file_path, self.frames)

    def _add_frame(self, image_path):
        self.frames.append(imageio.imread(image_path))


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

        self.transparency_select = ttk.Checkbutton(self, text="Transparency", variable=self.app.transparency)
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

        self.fps_select.current(0)
        self.disposal_select.current(0)

        self.layout()

    def layout(self):
        self.transparency_select.grid(column=0, row=0, columnspan=2, sticky=(W,))
        self.fps_label.grid(column=0, row=1, sticky=(W,))
        self.fps_select.grid(column=1, row=1, sticky=(W,))
        self.disposal_label.grid(column=0, row=2, sticky=(W,))
        self.disposal_select.grid(column=1, row=2, sticky=(W,))


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
