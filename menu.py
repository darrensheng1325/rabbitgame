from buttons import Button, TextButton
quit_button = TextButton("retry_button", "Quit")
quit_button.onclick(quit)
back_button = TextButton("retry_button", "Back")
def draw_menu():
    quit_button.draw()
    back_button.draw_button()

def exit_menu():
    global paused
    paused=false
back_button.onclick(exit_menu)
    