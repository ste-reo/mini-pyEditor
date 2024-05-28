from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import sys
import front_end

my_compiler = Tk()
my_compiler.title('Group 6 IDE')
my_path = ''
line_number_bar = Text(my_compiler, width=2, padx=3, takefocus=0, border=0, background='darkgray', state='disabled')
line_number_bar.pack(side='left', fill='y')

editor_frame = Frame(my_compiler)
editor_frame.pack(fill='both', expand=True)

my_editor = Text(editor_frame, wrap='none', undo=True)
my_editor.pack(side='left', fill='both', expand=True)

scrollbar_y = Scrollbar(editor_frame, command=my_editor.yview)
scrollbar_y.pack(side='right', fill='y')
my_editor['yscrollcommand'] = scrollbar_y.set

my_editor['yscrollcommand'] = scrollbar_y.set

my_output = Text(height=15)
my_output.pack()

def update_line_numbers(event=None):
    lines = str(my_editor.get(1.0, 'end-1c')).count('\n')
    line_number_bar.config(state='normal')
    line_number_bar.delete(1.0, 'end-1c')
    line_number_bar.insert('insert', '\n'.join(map(str, range(1, lines + 1))))
    line_number_bar.config(state='disabled')

def set_path(path):
    global my_path
    my_path = path

def opener():
    path = askopenfilename(defaultextension=".py", filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        my_code = file.read()
        my_editor.delete('1.0', END)
        my_editor.insert('1.0', my_code)
        set_path(path)
        update_line_numbers()

def saves_as():
    if my_path == '':
        path = asksaveasfilename(defaultextension=".py", filetypes=[('Python Files', '*.py')])
    else:
        path = my_path
    with open(path, 'w') as file:
        my_code = my_editor.get('1.0', END)
        file.write(my_code)
        set_path(path)

def run_code():
    global my_path
    if my_path == '':
        saves_as()  # Save the file before running if not saved

    python_executable = f'C:\\python_install\\python.exe'
    command = f'"{python_executable}" "{my_path}"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    my_output.delete('1.0', END)
    my_output.insert('1.0', output.decode('utf-8'))

    if error:
        my_output.insert(END, f"\nError: {error.decode('utf-8')}")

# Bind events
my_editor.bind('<Key>', update_line_numbers)
my_editor.bind('<MouseWheel>', update_line_numbers)
my_editor.bind('<Button-4>', update_line_numbers)
my_editor.bind('<Button-5>', update_line_numbers)

# Menu
main_menu = Menu(my_compiler)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Open', command=opener)
file_menu.add_command(label='Save', command=saves_as)
file_menu.add_command(label='Save as', command=saves_as)
file_menu.add_command(label='Exit', command=sys.exit)
main_menu.add_cascade(label='File', menu=file_menu)

run_menu = Menu(main_menu, tearoff=0)
run_menu.add_command(label='Run', command=run_code)
main_menu.add_cascade(label='Run', menu=run_menu)

my_compiler.config(menu=main_menu)

my_compiler.mainloop()
