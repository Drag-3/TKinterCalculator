import tkinter as tk  # Import tkinter library
import math  # Import math lib
import re  # Import this thing too
from tkinter import font  # in python 9 does not work without this (it works in 7 right)
import decimal
from decimal import Decimal as D

class Calculator:
    """
    A class used to implement the functions of a calculator
    """
    op_set = {"*", "/", "+", "-"}

    def __init__(self, answer, equation):
        self.answer_set = answer
        self.equation_set = equation
        self.expression = ""
        self.paren = False
        self.prev_expression = []
        self.itr = ""

    def set_prev_expr(self):
        """
        Stores all changes to the expression in a list
        """
        self.prev_expression.append((self.expression, self.paren))

    def get_prev_expr(self):
        try:
            print("Getting last entry")
            self.expression, self.paren = self.prev_expression.pop()
            self.equation_set(self.expression)
        except IndexError:
            print("No values in undo")
            self.answer_set("Can't undo")

    def clear(self):
        """
        Resets Variables used to defaults
        """
        self.set_prev_expr()
        print("Clearing")
        self.paren = False
        self.expression = ""
        self.answer_set(self.expression)
        self.equation_set(self.expression)
        self.itr = ""
        print("Clearing complete")

    def insert_paren(self):
        """
        Inserts paren into equation
        """
        self.set_prev_expr()
        if not self.paren:
            self.expression += "("
            self.equation_set(self.expression)
            self.paren = True  # Keeps track of paren orientation
            print(self.expression)
        else:
            self.expression += ")"
            self.paren = False
            self.equation_set(self.expression)
            print(self.expression)

    def percent(self):
        """
        divides expression by 100
        """
        self.set_prev_expr()
        self.expression += " / 100"
        self.evaluate(self.expression)

    def square(self):
        self.set_prev_expr()
# If the last number is in paren applies to entire paren block
        match = None
        rem_expression = ""
        print(self.expression)
        try:
            match = re.match(r'\([^)]*\)$|\S+$', self.expression)
            rem_expression = self.expression[:match.span()[0]] + self.expression[match.span()[1]:]
            match = match.group()
        except (SyntaxError, AttributeError):
            print("SyntaxError")
            self.answer_set("SyntaxError")
        else:
            print(f"match = {match}")
        try:
            last = float(self.evaluate(match))
            print(f"expression = {rem_expression} last = {last}")
            self.expression = f" {rem_expression}{(D(last) ** D(2))}"
            print(f"expression after combine = {self.expression}")
            print(self.expression)
            self.evaluate(self.expression)
        except:  # Any errors should be picked up by evaluate function so no need to print to screen
            print("Error")
            self.answer_set("Cannot Calculate Ans")

    def press(self, num: str):
        self.set_prev_expr()
        if num in self.op_set:  # Adds spaces either side of operators. Special operators are handled separately
            self.expression = f"{self.expression} {num} "
        else:  # Negative is included here
            self.expression = str(self.expression) + str(num)
        self.equation_set(self.expression)
        print(self.expression)

    def square_root(self):
        self.set_prev_expr()
# If the last number is in paren applies to entire paren block
        match = None
        rem_expression = ''
        print(self.expression)
        try:
            match = re.match(r'\([^)]*\)$|\S+$', self.expression)  # gets last match
            rem_expression = self.expression[:match.span()[0]] + self.expression[match.span()[1]:]
            match = match.group()
        except (SyntaxError, AttributeError):
            print("SyntaxError")
            self.answer_set("SyntaxError")
        else:
            print(f"match = {match}")
        try:
            last = float(self.evaluate(match))
            print(f"expression = {rem_expression} last = {last}")
            self.expression = f" {rem_expression}{D(last).sqrt()}"
            print(f"expression after combine = {self.expression}")
            print(self.expression)
            self.evaluate(self.expression)
        except ValueError:  # Should be called if try negative num
            print("Error")
            self.answer_set("Imaginary Answer")

    def backspace(self):
        self.set_prev_expr()
        if self.expression[-1] == ")":  # If you delete a paren re-add paren flag
            self.paren = True
        elif self.expression[-1] == "(":  # Removes set paren flag if start paren is deleted
            self.paren = False
        self.expression = self.expression[:-1]
        print(self.expression)
        self.equation_set(self.expression)

    # Function to find weight
    # of operators.
    def _weight(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    # Function to perform arithmetic
    # operations.
    def _arith(self, a, b, op):
        try:
            if op == '+':
                return a + b
            elif op == '-':
                return a - b
            elif op == '*':
                return a * b
            elif op == '/':
                return a / b
            else:
                return None
        except ZeroDivisionError:
            print("Invalid Operation: Div by Zero")
            self.answer_set("ZeroDivisionError")
            return "ZeroDiv"

    # Function that returns value of
    # expression after evaluation.
    def evaluate(self, tokens: str):
        self.set_prev_expr()
        
        # adds support for negative numbers by adding a valid equation
        token_lst = tokens.split(" ")
        #print(token_lst)
        for index, elem in enumerate(token_lst):
            if "—" in elem:
                token_lst[index] = elem.replace("—", "(0 -") + ")" 
        #print(token_lst)
        tokens = " ".join(token_lst)
        print(tokens)
        
        # stack to store integer values.
        values = []

        # stack to store operators.
        ops = []
        i = 0

        while i < len(tokens):

            # Current token is a whitespace,
            # skip it.
            if tokens[i] == ' ':
                i += 1
                continue

            # Current token is an opening 
            # brace, push it to 'ops'
            elif tokens[i] == '(':
                ops.append(tokens[i])

            # Current token is a number or decimal point, push 
            # it to stack for numbers.
            elif (tokens[i].isdigit()) or (tokens[i] == "."):
                val = ""

                # There may be more than one
                # digits in the number.
                while (i < len(tokens) and
                       (tokens[i].isdigit() or tokens[i] == ".")):
                    val += str(tokens[i])
                    i += 1
                val = D(val)
                values.append(val)

                # right now the i points to 
                # the character next to the digit,
                # since the for loop also increases 
                # the i, we would skip one 
                #  token position; we need to 
                # decrease the value of i by 1 to
                # correct the offset.
                i -= 1

            # Closing brace encountered, 
            # solve entire brace.
            elif tokens[i] == ')':

                while len(ops) != 0 and ops[-1] != '(':
                    try:
                        val2 = values.pop()
                        val1 = values.pop()
                        op = ops.pop()
                    except IndexError:
                        print("Syntax Error")
                        self.answer_set("Syntax Error")
                        self.get_prev_expr()
                        self.get_prev_expr()  # Returns expr to previous state
                        return None

                    values.append(self._arith(val1, val2, op))
                    if values[-1] == "ZeroDiv":
                        return None

                # pop opening brace.
                ops.pop()

            # Current token is an operator.
            else:

                # While top of 'ops' has same or 
                # greater _weight to current 
                # token, which is an operator. 
                # Apply operator on top of 'ops' 
                # to top two elements in values stack.
                while (len(ops) != 0 and
                       self._weight(ops[-1]) >=
                       self._weight(tokens[i])):

                    try:
                        val2 = values.pop()
                        val1 = values.pop()
                        op = ops.pop()
                    except IndexError:
                        print("Syntax Error")
                        self.answer_set("Syntax Error")
                        self.get_prev_expr()  # Returns expr to previous state
                        self.get_prev_expr()
                        return None

                    values.append(self._arith(val1, val2, op))
                    if values[-1] == "ZeroDiv":
                        return None

                # Push current token to 'ops'.
                ops.append(tokens[i])

            i += 1

        # Entire expression has been parsed 
        # at this point, apply remaining ops 
        # to remaining values.
        while len(ops) != 0:

            try:
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
            except IndexError:
                print("Syntax Error")
                self.answer_set("Syntax Error")
                self.get_prev_expr()  # Returns expr to previous state
                self.get_prev_expr()
                return None

            values.append(self._arith(val1, val2, op))
            if values[-1] == "ZeroDiv":
                return None

        # Top of 'values' contains result,
        # return it.
        try:
            if (values[-1] % 1 == 0):  # Checks if the value has decimal
                values[-1] = int(values[-1])
            if (values[-1] >= 9.9e+8) or (values[-1] <= -9.9e+8):
                raise OverflowError
            values[-1] = round(values[-1], 10)  # rounds a decimal number to 10 digits (max on screen is 20 in smallest size)
            self.expression = str(values[-1])
            self.expression = self.expression.replace("-", "—")  # If the answer starts with a dash replace with neg marker
            self.equation_set(self.expression)
            self.answer_set(self.expression)

            return values[-1]
        except SyntaxError:
            print("Syntax Error")
            self.answer_set("Syntax Error")
            return None
        except OverflowError:
            print("Overflow")
            self.answer_set("Overflow")
            self.get_prev_expr()  # Returns to previous state (for special funct) deletes extra step in normal ops
            self.get_prev_expr()
            return None


class CalcGui(Calculator):
    
    BOX_HEIGHT = 2
    BOX_WIDTH = 8
    CLEAR_COLOR = "#c2b2b2"
    SPECIAL_BUTTONS_COLOR = "#b1b1b1"
    OPERATOR_COLOR = "dark grey"
    NUM_COLOR = "#cfcaca"
    SCREEN_COLOR = "light grey"
 
    def __init__(self, main_win: tk.Tk):
        self.main_win = main_win
        self.answer = tk.StringVar()
        self.equation = tk.StringVar()
        Calculator.__init__(self, self.answer.set, self.equation.set)
        self.create_text_canvas()
        self.create_button_canvas()
    
    def create_text_canvas(self):

        entry_canv = tk.Canvas(bg=self.SCREEN_COLOR)  # Contains the output screens
        font_eq = font.Font(entry_canv, family="System", size=10)
        font_ans = font.Font(entry_canv, family="system", size=15)
        entry1 = tk.Entry(entry_canv,
                          text=self.equation,
                          textvariable=self.equation,
                          bg=self.SCREEN_COLOR,
                          borderwidth=0,
                          highlightthickness=0,
                          font=font_eq
                          )
        entry1.grid(pady=1, padx=2, row=1, column=0, columnspan=5, rowspan=1, sticky="nwse")
        
        ans_box = tk.Label(entry_canv,
                           textvariable=self.answer,
                           #width=20,
                           bg=self.SCREEN_COLOR,
                           borderwidth=0,
                           highlightthickness=0,
                           font=font_ans,
                           justify="right"  # Print from left of the text box
                           )
        ans_box.grid(pady=2, row=2, column=5, columnspan=4, rowspan=1, sticky="nwse")
        
        tk.Grid.rowconfigure(entry_canv, (0, 1, 2), weight=1)
        tk.Grid.columnconfigure(entry_canv, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        entry_canv.pack(padx=5, pady=3, fill=tk.BOTH, expand=True)
    
    def create_button_canvas(self):
        
        buttons = [  # List of all button info
             #chr.    x  y  color                     command
            ("clear", 0, 0, self.CLEAR_COLOR          , self.clear             ),
            ("↺"   , 1, 0, self.SPECIAL_BUTTONS_COLOR, self.get_prev_expr     ),
            ("x²"   , 2, 0, self.SPECIAL_BUTTONS_COLOR, self.square            ),
            ("√x"   , 3, 0, self.SPECIAL_BUTTONS_COLOR, self.square_root       ),
            ("—"    , 0, 1, self.SPECIAL_BUTTONS_COLOR, lambda: self.press("—")),
            ("()"   , 1, 1, self.SPECIAL_BUTTONS_COLOR, self.insert_paren      ),
            ("%"    , 2, 1, self.SPECIAL_BUTTONS_COLOR, self.percent           ),
            ("÷"    , 3, 1, self.OPERATOR_COLOR       , lambda: self.press("/")),
            ("7"    , 0, 2, self.NUM_COLOR            , lambda: self.press("7")),
            ("8"    , 1, 2, self.NUM_COLOR            , lambda: self.press("8")),
            ("9"    , 2, 2, self.NUM_COLOR            , lambda: self.press("9")),
            ("x"    , 3, 2, self.OPERATOR_COLOR       , lambda: self.press("*")),
            ("4"    , 0, 3, self.NUM_COLOR            , lambda: self.press("4")),
            ("5"    , 1, 3, self.NUM_COLOR            , lambda: self.press("5")),
            ("6"    , 2, 3, self.NUM_COLOR            , lambda: self.press("6")),
            ("-"    , 3, 3, self.OPERATOR_COLOR       , lambda: self.press("-")),
            ("1"    , 0, 4, self.NUM_COLOR            , lambda: self.press("1")),
            ("2"    , 1, 4, self.NUM_COLOR            , lambda: self.press("2")),
            ("3"    , 2, 4, self.NUM_COLOR            , lambda: self.press("3")),
            ("+"    , 3, 4, self.OPERATOR_COLOR       , lambda: self.press("+")),
            ("⌫"   , 0, 5, self.NUM_COLOR            , self.backspace         ),
            ("0"    , 1, 5, self.NUM_COLOR            , lambda: self.press("0")),
            ("."    , 2, 5, self.NUM_COLOR            , lambda: self.press(".")),
            ("="    , 3, 5, "orange"             , lambda: self.evaluate(self.expression)),
            ]
        
        button_canv = tk.Canvas(bg="red")  # Contains Input buttons
        button_font = font.Font(button_canv, family="system", size=13)
        for (character, x, y, color, command) in buttons:
            button = tk.Button(button_canv, text=character, bg= color,  # Unique
                               relief=tk.RAISED, compound=tk.LEFT, font=button_font)  # Defaults
            
            button.grid(row=y, column=x, sticky="nsew")
            tk.Grid.rowconfigure(button_canv, y, weight=1)
            tk.Grid.columnconfigure(button_canv, x, weight=1)
            button.configure(command=command)
        button_canv.pack(padx=5, pady=5, expand= True, fill=tk.BOTH)


def main():
    main_win = tk.Tk()
    main_win.configure(background="light blue")
    main_win.title("Calculator")
    main_win.minsize("305", "390")
    #main_win.resizable(False, False)  # Becomes ugly if you resize it
    #main_win.grid_columnconfigure(4, minsize= 100)
    calculator = CalcGui(main_win)
    main_win.mainloop()


if __name__ == "__main__":
    main()
