from tkinter import *
import vimeo
import csv
from tkinter import filedialog


numToken = ""
numKey = ""
numSecret = ""



def conectarVimeo(tokenF, keyF, secretF):
    v = vimeo.VimeoClient(
        token=tokenF,
        key=keyF,
        secret=secretF
    )
    print(tokenF)
    # Make the request to the server for the "/me" endpoint.
    about_me = v.get('/me')
    # Make sure we got back a successful response.
    #assert about_me.status_code == 200

    # Load the body's JSON data.
    respostaStatus = about_me.json()
    print(respostaStatus)
    return respostaStatus



def clicaConectar():
    numToken = entrada1.get()
    numKey = entrada2.get()
    numSecret = entrada3.get()
    statusConexao.delete(0.0, END)
    statusConexao.insert(END, conectarVimeo(numToken,numKey,numSecret))


window = Tk()
window.title("Deleta Vídeos do Vimeo")


#Labels e Entradas de Texto

Label (window, text="Token").grid(row=0, column=0, sticky=W)
entrada1 = Entry(window, width=30, bg="white")
entrada1.grid(row=0, column=1, sticky=W)

Label (window, text="Key (Client Identifier)").grid(row=1, column=0, sticky=W)
entrada2 = Entry(window, width=30, bg="white")
entrada2.grid(row=1, column=1, sticky=W)

Label (window, text="Client Secrets").grid(row=2, column=0, sticky=W)
entrada3 = Entry(window, width=30, bg="white")
entrada3.grid(row=2, column=1, sticky=W)



Button(window, text="conectar", width=6, command=clicaConectar).grid(row=3, column=1, sticky=W)


#STATUS
statusConexao = Text(window, width=60, height=4, wrap=WORD, background="white")
statusConexao.grid(row=5, column=0, columnspan=2, sticky=W)

localdoarquivo = "123"
def browsefunc():
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)
    global  localdoarquivo
    localdoarquivo = filename


browsebutton = Button(window, text="Selecione o arquivo CSV", command=browsefunc)
browsebutton.grid(row=10, column=0, sticky=W)

pathlabel = Label(window)
pathlabel.grid(row=11, column=0, sticky=W)

def percorreCSV(localarquivo):
    with open(localarquivo) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        statusConexao.delete(0.0, END)
        for row in csv_reader:
            print(row[1])
            apagaVideos(row[1])
    #print(localarquivo)


def apagaVideos(video):
    numToken = entrada1.get()
    numKey = entrada2.get()
    numSecret = entrada3.get()
    v = vimeo.VimeoClient(
        token=numToken,
        key=numKey,
        secret=numSecret
    )

    response = v.delete("/videos/" + str(video))
    chave = ""
    valor = ""
    try:
        resposta = response.json()
        for key, value in resposta.items():
            chave = key
            valor = value
    except:
        pass



    statusConexao.insert(END, "\nVideo ID: " + video + "\nStatus: " + str(response) + chave + valor)


Button(window, text="Apagar Vídeos", width=10, command=lambda: percorreCSV(localdoarquivo)).grid(row=13, column=0, sticky=W)


window.mainloop()
