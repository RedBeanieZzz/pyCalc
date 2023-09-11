import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

COLOR_BACKGROUND = "#3d3c50"
COLOR_NUMBERS = "#140c1c"
COLOR_BUTTONS1 = "#a9a7bf"
COLOR_BUTTONS2 = "#a4a4fb"
COLOR_OPTIONAL3 = "#7e7cc4"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.digits = {
            7: (1,1), 8: (1,2), 9 : (1,3),
            4: (2,1), 5: (2,2), 6 : (2,3),
            1: (3,1), 2: (3,2), 3 : (3,3),
            0: (4,1), '.' : (4,2)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.total_label, self.label = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range (1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        
        self.create_digits_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        
        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_square_root_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text = self.total_expression, anchor = tk.E, bg = COLOR_NUMBERS, fg = COLOR_BUTTONS2, padx = 24, font= SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text = self.current_expression, anchor = tk.E, bg = COLOR_NUMBERS, fg = COLOR_BUTTONS2, padx = 24, font= LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg = COLOR_BACKGROUND)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digits_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text = str(digit), bg = COLOR_NUMBERS, fg = COLOR_BUTTONS1, font = DIGITS_FONT_STYLE, borderwidth = 0, command= lambda x=digit: self.add_to_expression(x))
            button.grid(row = grid_value[0], column = grid_value[1], sticky = tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=COLOR_BACKGROUND, fg=COLOR_OPTIONAL3, font=DEFAULT_FONT_STYLE, borderwidth=0, command= lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()    

    def create_clear_button(self):
        button = tk.Button(
            self.buttons_frame, text="C",
            bg=COLOR_BACKGROUND,
            fg=COLOR_OPTIONAL3,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0,
            command= self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2",
            bg=COLOR_BACKGROUND,
            fg=COLOR_OPTIONAL3,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0, 
            command= self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square_root(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_square_root_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax",
            bg=COLOR_BACKGROUND,
            fg=COLOR_OPTIONAL3,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0, 
            command= self.square_root)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except Exception as e:
            self.current_expression = "Error"
        
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=COLOR_BUTTONS2, fg=COLOR_OPTIONAL3, font=DEFAULT_FONT_STYLE, borderwidth=0, command= self.evaluate)
        button.grid(row=4, column=3, columnspan=3, sticky=tk.NSEW)


    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')    
        self.total_label.config(text=expression)
    
    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()