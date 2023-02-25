import tkinter as tk
import requests
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from timeit import default_timer as timer
import os
import csv
from datetime import date

# ------------------ CONSTANTS ------------------ #
EMAIL = os.environ.get('eMail')
KEY = os.environ.get('kEY')
ROOT = 'https://the-one-api.dev/v2/quote'
BGCOLOR = '#3B5946'
FONT = ("Cascadia Mono semiBold", 18)
FONT_INSTRUCTIONS = ("Cascadia Mono semiBold", 15)
FONTCOLOR = '#D7D9C7'
QUOTECOLOR = '#96A694'
HEADER = ['date', 'wpm', 'accuracy']

# ---------------- Global values ---------------- #
start = ''
quote = ''
name = ''
gross_wpm = 0
accuracy = 0

# ---------------- Functions ---------------- #
def test(event):
    global start
    start = timer()
    print(start)

def check(event):
    global gross_wpm
    global accuracy
    stop_ = timer()
    len_of_quote = len(quote)
    time_spent_sec = stop_ - float(start)
    time_spent_min = time_spent_sec / 60
    gross_wpm = (len_of_quote / 5) / time_spent_min
    accuracy = fuzz.ratio(quote, text_window.get('1.0', "end")[1:])
    # Widget placement
    results_wpm.config(text=f'Your WPM is {gross_wpm:.2f}')
    results_wpm.grid(row=3, column=0, sticky='w')
    results_acc.config(text=f'Your accuracy:{accuracy}%')
    results_acc.grid(row=4, column=0, sticky='w')
    again_button.grid(column=1, row=4)
    new_player_button.grid(column=2, row=4)
    save_score()
    print(quote)
    print(text_window.get('1.0', "end")[1:])
    print(gross_wpm)
    print(stop_)
    print(stop_ - float(start))

def get_quote():
    hdrs = {
        'Authorization': 'Bearer ' + str(KEY)
    }
    response = requests.get(url=ROOT, headers=hdrs)
    if response.status_code == 200:
        quotes = response.json()
    else:
        print('Error from server: ' + str(response.content))
    ran_number_for_quote = random.randint(0, 1001)
    global quote
    quote = quotes['docs'][ran_number_for_quote]['dialog']

def clear_text():
    results_wpm.grid_forget()
    results_acc.grid_forget()
    text_window.delete(1.0, "end")
    text_window.insert(1.0, " ")
    text_window.tag_add("txt", "1.0", "end")
    get_quote()
    quote_label.config(text=quote)


def start_page():
    # Hide previous elements
    instructions_label.grid_forget()
    quote_label.grid_forget()
    text_window.grid_forget()
    results_wpm.grid_forget()
    results_acc.grid_forget()
    again_button.grid_forget()
    new_player_button.grid_forget()
    refresh_quote_button.place_forget()
    # Show start page elements
    welcome_label.place(x=420, y=100, anchor='center')
    enter_name_label.place(x=240, y=220, anchor='center')
    name_txt.place(x=650, y=235, anchor='center')
    go_button.place(x=420, y=370, anchor='center')


def test_page():
    global name
    name = name_txt.get().lower()
    get_quote()
    # Hide previous elements
    welcome_label.place_forget()
    enter_name_label.place_forget()
    name_txt.place_forget()
    go_button.place_forget()
    # Show test page elements
    text_window.delete(1.0, "end")
    text_window.insert(1.0, " ")
    text_window.tag_add("txt", "1.0", "end")
    instructions_label.grid(row=0, column=0, columnspan=3, sticky="NESW", padx=(23, 0))
    quote_label.config(text=quote)
    quote_label.grid(row=1, column=0, columnspan=3, sticky="NESW", padx=(23, 0), pady=(25, 20))
    text_window.grid(row=2, column=0, columnspan=3, sticky="NESW", padx=(23, 0))
    refresh_quote_button.place(x=420, y=195, anchor='center')

def refresh_quote():
    get_quote()
    quote_label.config(text=quote)

def save_score():
    today = date.today()
    row = [today, float(gross_wpm), float(accuracy)]
    global name
    if name == '':
        name = 'anonymous'
    path = f'scores/{name}.csv'
    if os.path.exists(path):
        with open(f'scores/{name}.csv', 'a', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    else:
        with open(f'scores/{name}.csv', 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            writer.writerow(row)


# --------------------- UI ---------------------- #
# Screen set-up
window = tk.Tk()
window.title('Typing Speed Test')
window.config(bg=BGCOLOR)
window.geometry('840x550')

# All elements before placement
## Main screen
welcome_label = tk.Label(
    text='Hello!\nWelcome to the Lord of The Rings\nTyping Speed Test',
    bg=BGCOLOR, font=FONT, fg=FONTCOLOR)
enter_name_label = tk.Label(
    text='To Start\nPlease enter your Name:',
    bg=BGCOLOR, font=FONT, fg=FONTCOLOR)

name_txt = tk.Entry(font=FONT)

go_img = tk.PhotoImage(file='assets/go_button.png')
go_button = tk.Button(image=go_img, borderwidth=0, highlightthickness=0, activebackground=BGCOLOR, command=test_page)

## Test Screen
instructions_label = tk.Label(text="In this part you will be asked to write down generated quote.\n"
                                   "The timer will start automatically after you star\ntyping in the field.\n"
                                   "To stop the timer, press <ENTER> once you've done.\n"
                                   "If you do not like the quote, you can generate\nnew one before starting to type.",
                              bg=BGCOLOR, font=FONT_INSTRUCTIONS, fg=FONTCOLOR)
quote_label = tk.Label(text="quote", bg=BGCOLOR, font=FONT_INSTRUCTIONS, fg=QUOTECOLOR, wraplength=700)
text_window = tk.Text(width=20, height=3, font=FONT, fg='#214040', bg="#96A694")
text_window.tag_config("txt", justify='center')
text_window.insert(1.0, " ")
text_window.tag_add("txt", "1.0", "end")
text_window.bind('<Button-1>', test)
text_window.bind('<Return>', check)

results_wpm = tk.Label(text='', bg=BGCOLOR, font=FONT, fg=FONTCOLOR)
results_acc = tk.Label(text='', bg=BGCOLOR, font=FONT, fg=FONTCOLOR)

again_button_image = tk.PhotoImage(file='assets/again_burtton.png')
again_button = tk.Button(image=again_button_image, borderwidth=0, highlightthickness=0,
                         activebackground=BGCOLOR, command=clear_text)
new_player_button_image = tk.PhotoImage(file='assets/newplayer_button.png')
new_player_button = tk.Button(image=new_player_button_image, borderwidth=0, highlightthickness=0,
                              activebackground=BGCOLOR, command=start_page)

refresh_quote_image = tk.PhotoImage(file='assets/refresh_button.png')
refresh_quote_button = tk.Button(image=refresh_quote_image, borderwidth=0, highlightthickness=0,
                              activebackground=BGCOLOR, command=refresh_quote)

# ---------------- Run ---------------- #
start_page()


window.mainloop()