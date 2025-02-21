import tkinter as tk

root = tk.Tk()
root.title("Admin")
root.geometry("1000x800")

label = tk.Label(root, text="connected/in_voice/muted/deafen", font=("Arial", 30))
label.pack(pady=10)  # Add padding
def connected():

    label.config(text="connected")

def In_voice():
    label.config(text="In voice")

def Muted():
    label.config(text="Muted")

def Deafened():
    label.config(text="Deafened")

button1 = tk.Button(root, text="Connected users", command= connected)
button2 = tk.Button(root, text ="users in voice", command= In_voice)
button3 = tk.Button(root, text ="Muted", command= Muted)
button4 = tk.Button(root, text ="Deafened", command= Deafened)
button1.pack()
button2.pack()
button3.pack()
button4.pack()

root.mainloop()
