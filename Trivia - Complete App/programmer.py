import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import pandas as pd
import urllib.request, json
import random

#global dictionary of dynamically changing parameters
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct_answer": [],
    "score" : [],
    "index" : [random.randint(0,49)]
              }

#global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "button": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "score": [],
    "message": [],
    "message2": []
    }

#load databese of trivia questions:
#Open Trivia Data Base (https://opentdb.com)

#open a json file from URL and fetch the content
#Thank you Anurag Uniyal of Stack Overflow:
#https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
with urllib.request.urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as url:
    data = json.loads(url.read().decode())
    data_frame = pd.DataFrame(data['results'])

# a function to select specific parameters at a certain index
# pre-process them, and store them in the global dictionary of parameters
def preload_data(idx):
    #select parameters at a given index
    question = data_frame['question'][idx]
    correct = data_frame['correct_answer'][idx]
    wrong = data_frame['incorrect_answers'][idx]

    #charecters with bad formatting and their correction
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
        ]

    #replace bad charecters in strings
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    #replace bad charecters in lists
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    #shuffle answers in a random order
    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    #store parameters in the global disctionary
    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])
    parameters["question"].append(question)
    parameters["correct_answer"].append(correct)

    print("CURRENT QUESTION:\n", parameters["question"][-1])
    print("CORRECT ANSWER:\n", parameters["correct_answer"][-1])

def clear_widgets():
    ''' remove all existing widgets from the window
        & clear the dictionary of widgets'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
            for i in range(0,len(widgets[widget])):
                widgets[widget].pop()

def clear_parameters():
    '''clear the dictionary of parameters'''
    for param in parameters:
        if parameters[param] != []:
            for i in range(0, len(parameters[param])):
                parameters[param].pop()

def try_again():
    '''a press on the "try again" button'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
            widgets[widget].pop()
    frame1()

def start_game():
    '''a press on the "PLAY" button'''
    clear_widgets()
    clear_parameters()

    #set initial score and index
    parameters["score"].append(0)
    parameters["index"].append(random.randint(0,49))

    preload_data(parameters["index"][-1])
    frame2()

def is_correct(answer_btn):
    '''check wether users answer was correct or not'''
    if answer_btn.text() == parameters['correct_answer'][-1]:
        #ANSWER IS CORRECT

        #update index
        parameters['index'].pop()
        parameters['index'].append(random.randint(0,49))

        #update score
        temp_score = parameters['score'][-1] + 10
        parameters["score"].pop()
        parameters["score"].append(temp_score)

        #load data with new index
        preload_data(parameters['index'][-1])

        #update widgets text values with new data
        widgets["score"][-1].setText(str(parameters['score'][-1]))
        widgets["question"][0].setText(parameters['question'][-1])
        widgets["answer1"][0].setText(parameters['answer1'][-1])
        widgets["answer2"][0].setText(parameters['answer2'][-1])
        widgets["answer3"][0].setText(parameters['answer3'][-1])
        widgets["answer4"][0].setText(parameters['answer4'][-1])

        #WINNING THE GAME
        if parameters["score"][-1] == 100:
            clear_widgets()
            frame3()
    else:
        #LOOSING THE GAME - INCORRECT ANSWER
        clear_widgets()
        frame4()

def answer_button(answer, left_m, right_m):
    '''a function that creates identical buttons for all 4 answers'''
    button = QPushButton(answer)
    button.setStyleSheet(
        "*{border: 4px solid '#BC006C'; color: 'white'; font-family: 'Shanti'; font-size: 16px; border-radius: 25px; padding:15px 0px; margin-left:"+ str(left_m)+ "px; margin-right:"+ str(right_m)+"px; margin-top:20px;} *:hover{background:'#BC006C';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.clicked.connect(lambda x:is_correct(button))
    return button

#*********************************************
#                  FRAME 1
#*********************************************

def frame1():
    #logo widget
    pixmap = QPixmap('logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:100px;"
    )

    widgets["logo"].append(logo)

    #button widget
    button = QPushButton('PLAY')
    button.setStyleSheet(
        "*{padding:25px 0px; margin-top:100px; margin-right:200px; margin-left:200px; margin-bottom:120px; border: 5px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 35px; border-radius: 50px;} *:hover{background:'#BC006C';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    #button callback
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    #place widgets on the grid
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)
    widgets["logo"][-1].show()
    widgets["button"][-1].show()

#*********************************************
#                  FRAME 2
#*********************************************
def frame2():
    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setFixedHeight(150)
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        "font-family: 'Shanti';" +
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 24px 12px 0px 5px;"+
        "margin: 20px 190px 40px 200px;"+
        "background: #64a314;"+
        "border: 1px solid #64a314;"+
        "border-radius: 40px;"
    )
    widgets["score"].append(score)

    #question widget
    question = QLabel(parameters['question'][-1])
    question.setWordWrap(True)
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; padding:75px; height: 150px;"
        )

    widgets["question"].append(question)

    #answer buttons
    answer_btn1 = answer_button(parameters['answer1'][-1], 85, 5)
    answer_btn2 = answer_button(parameters['answer2'][-1], 5, 85)
    answer_btn3 = answer_button(parameters['answer3'][-1], 85, 5)
    answer_btn4 = answer_button(parameters['answer4'][-1], 5, 85)

    widgets["answer1"].append(answer_btn1)
    widgets["answer2"].append(answer_btn2)
    widgets["answer3"].append(answer_btn3)
    widgets["answer4"].append(answer_btn4)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :20px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 2, 2)
    grid.addWidget(widgets["answer1"][-1], 3, 0)
    grid.addWidget(widgets["answer2"][-1], 3, 1)
    grid.addWidget(widgets["answer3"][-1], 4, 0)
    grid.addWidget(widgets["answer4"][-1], 4, 1)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

    widgets["logo"][-1].show()

#*********************************************
#             FRAME 3 - WIN GAME
#*********************************************

def frame3():
    #congradulations widget
    message = QLabel("Congradulations! You\nare a true programmer!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel("100")
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    #button callback
    button.clicked.connect(try_again)
    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4():
    #sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{padding:25px 0px; background: '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 35px; border-radius: 40px; margin: 10px 200px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    #button callback
    button.clicked.connect(try_again)
    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)

#initialize the GUI application
app = QApplication(sys.argv)

#window object settings
window = QWidget()
window.setWindowTitle("Who wants to be a programmer?")
window.setFixedWidth(1000)
window.setStyleSheet("background: #161219;")

#initiallize grid
grid = QGridLayout()

frame1()

#set grid and show window
window.setLayout(grid)
window.show()

sys.exit(app.exec()) #terminate app
