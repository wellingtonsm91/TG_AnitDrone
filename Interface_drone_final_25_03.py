from tkinter import *
import tkinter.messagebox
import os
import serial
#import runpy
import subprocess
import sys


#COM1 pode ser modificado de acordo com a conexao usada no arduino
#ser = Serial("COM9", baudRate = 9600, timeout=0, writeTimeout=0)
ser = serial.Serial('COM9', 115200, timeout=.1)

principal = Tk()
principal.title("Anti-Drone")

#Definição das funções
def botao_liga():
	#os.system('DeteccaoTG_SSD_22_02_Detec4_30000.py')
	#os.open('DeteccaoTG_SSD_22_02_Detec4_30000.py')
	#run("DeteccaoTG_SSD_22_02_Detec4_30000.py", shell=True, check=True)
	#runpy.run_path('DeteccaoTG_SSD_22_02_Detec4_30000.py')
	subprocess.Popen([sys.executable, "DeteccaoTG_SSD_22_02_Detec4_30000.py"]) # Call subprocess

def botao_gera():
	os.system('historico.txt')
	#os.open('DeteccaoTG_SSD_22_02_Detec4_30000.py')
	#run("DeteccaoTG_SSD_22_02_Detec4_30000.py", shell=True, check=True)
	#runpy.run_path('DeteccaoTG_SSD_22_02_Detec4_30000.py')
	#subprocess.Popen([sys.executable, "historico.txt"]) # Call subprocess

def botao_opcao(op):
	if op == "a":
		ser.write(b'a')			#comando para Arduino
		#posicao_graus.config(state = 'disabled')
		#ser.write('a')
	else:
		ser.write(b'm')			#comando para Arduino
		#ser.write('m')

def botao_horario():
	ser.write(b'z')

def botao_antihorario():
	ser.write(b'x')

def botao_liga_ilu():
	ser.write(b'l')

def botao_desliga_ilu():
	ser.write(b'd')	


titulo_1 = Label(principal, text = "Sistema de vigilância Anti-Drone", font=('Calibri','12','bold'))
titulo_1.grid(row = 0, column = 0, columnspan = 2)

titulo_2 = Label(principal, text = "Selecione o tipo de funcionamento:", font=('Calibri','10','bold'))
titulo_2.grid(row = 2, column = 0, columnspan = 2)

titulo_3 = Label(principal, text = "Selecione o movimento gradual (modo manual):", font=('Calibri','10','bold'))
titulo_3.grid(row = 4, column = 0, columnspan = 2)

titulo_4 = Label(principal, text = "Ligar ou desligar lâmpada (modo manual):", font=('Calibri','10','bold'))
titulo_4.grid(row = 6, column = 0, columnspan = 2)

botao_liga = Button(principal, text = "Ligar camera", padx = 8, fg = "white", bg = "green", command = botao_liga)
botao_liga.grid(row = 1, column = 0)

botao_gera= Button(principal, text = "Histórico", fg = "white", bg = "green", command = botao_gera)
#botao_gera = Button(principal, text = "Desligar camera", fg = "white", bg = "red", command = "<q>")
botao_gera.grid(row = 1, column = 1)

botao_aut = Button(principal, text = "Automático", padx = 28, pady = 10, fg = "white", bg = "black", command = lambda: botao_opcao("a"))
botao_aut.grid(row = 3, column = 0)

botao_man = Button(principal, text = "Manual", padx = 28, pady = 10, fg = "white", bg = "gray", command = lambda: botao_opcao("m"))
botao_man.grid(row = 3, column = 1)

botao_antihorario = Button(principal, text = "<<<", padx = 28, pady = 10, fg = "white", bg = "gray", command = botao_antihorario)
botao_antihorario.grid(row = 5, column = 0)

botao_horario = Button(principal, text = ">>>", padx = 28, pady = 10, fg = "white", bg = "gray", command = botao_horario)
botao_horario.grid(row = 5, column = 1)

botao_liga_ilu = Button(principal, text = "Iluminacao_ON", padx = 28, pady = 10, fg = "white", bg = "orange", command = botao_liga_ilu)
botao_liga_ilu.grid(row = 7, column = 0)

botao_desliga_ilu = Button(principal, text = "Iluminacao_OFF", padx = 28, pady = 10, fg = "white", bg = "blue", command = botao_desliga_ilu)
botao_desliga_ilu.grid(row = 7, column = 1)

# botao_ok = Button(principal, text = "OK", padx = 116, fg = "white", bg = "green", command = botao_ok)
# botao_ok.grid(row = 6, column = 0, columnspan = 2)

# botao_limpar = Button(principal, text = "Limpar", padx = 106, command = botao_limpar)
# botao_limpar.grid(row = 7, column = 0, columnspan = 2)

principal.mainloop()
