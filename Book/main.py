import tkinter as tk
from tkinter import messagebox

class Page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.textbox = tk.Text(self, height=10, width=40)
        self.textbox.pack(pady=10, fill="both", expand=True)

    def get_text(self):
        return self.textbox.get("1.0", tk.END)

    def set_text(self, text):
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", text)

class Book(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Book")
        self.geometry("650x500")

        self.pages = []
        self.current_page_index = 0

        self.top_frame = tk.Frame(self)
        self.left_frame = tk.Frame(self)
        self.middle_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)

        self.top_frame.pack(side="top", fill="x")
        self.left_frame.pack(side="left", fill="y")
        self.middle_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="y")
        self.bottom_frame.pack(side="bottom", fill="x", anchor="w")

        tk.Button(self.top_frame, text="Save Text", command=self.save_text).pack(side="left", padx=10, pady=10)
        tk.Button(self.top_frame, text="Load Text", command=self.load_text).pack(side="left", padx=10, pady=10)
        tk.Button(self.top_frame, text="Delete Page", command=self.delete_page).pack(side="left", padx=10, pady=10)

        tk.Button(self.left_frame, text="<--", command=self.go_left).pack(pady=20)
        tk.Button(self.right_frame, text="-->", command=self.go_right).pack(pady=20)

        tk.Button(self.bottom_frame, text="Quit", command=self.quit_app).pack(side="left", padx=10, pady=10)

        self.page_label = tk.Label(self.bottom_frame, font=("Arial", 12))
        self.page_label.pack(side="right", padx=20)

        first_page = Page(self.middle_frame)
        self.pages.append(first_page)
        first_page.pack(fill="both", expand=True)

        self.update_page_label()

    def go_left(self):
        if self.current_page_index == 0:
            return
        self.pages[self.current_page_index].pack_forget()
        self.current_page_index -= 1
        self.pages[self.current_page_index].pack(fill="both", expand=True)
        self.update_page_label()

    def go_right(self):
        if self.current_page_index == len(self.pages) - 1:
            new_page = Page(self.middle_frame)
            self.pages.append(new_page)
            self.pages[self.current_page_index].pack_forget()
            self.current_page_index += 1
            new_page.pack(fill="both", expand=True)
        else:
            self.pages[self.current_page_index].pack_forget()
            self.current_page_index += 1
            self.pages[self.current_page_index].pack(fill="both", expand=True)
        self.update_page_label()

    def delete_page(self):
        if len(self.pages) == 1:
            messagebox.showinfo("Cannot Delete", "You must have at least one page.")
            return
        page_to_delete = self.pages.pop(self.current_page_index)
        page_to_delete.pack_forget()
        if self.current_page_index >= len(self.pages):
            self.current_page_index = len(self.pages) - 1
        self.pages[self.current_page_index].pack(fill="both", expand=True)
        self.update_page_label()

    def save_text(self):
        page = self.pages[self.current_page_index]
        content = page.get_text()
        with open("saved_text.txt", "w", encoding="utf-8") as f:
            f.write(content)

    def load_text(self):
        try:
            with open("saved_text.txt", "r", encoding="utf-8") as f:
                content = f.read()
            page = self.pages[self.current_page_index]
            page.set_text(content)
        except FileNotFoundError:
            print("No saved_text.txt file found")

    def quit_app(self):
        answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if answer:
            self.destroy()

    def update_page_label(self):
        total = len(self.pages)
        current = self.current_page_index + 1
        self.page_label.config(text=f"Page {current} of {total}")

if __name__ == "__main__":
    app = Book()
    app.mainloop()