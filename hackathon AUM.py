import cv2
import datetime
import os
import speech_recognition as sr
import pyttsx3
import openai 
import random
import time
import numpy as np

apikey = '#'

engine = pyttsx3.init()
recognizer = sr.Recognizer()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Arya: "
    response = openai.completions.create(model="gpt-3.5-turbo-instruct",
    prompt= chatStr,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    say(response.choices[0].text)
    chatStr += f"{response.choices[0].text}\n"
    return response.choices[0].text

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *\n\n"
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            engine.say(text)
            engine.runAndWait()
            say("please enter the address")
            audio = recognizer.listen(source)
            address = recognizer.recognize_google(audio)
            engine.say(address)
            engine.runAndWait()
            say("please enter the purpose")
            audio = recognizer.listen(source)
            purpose = recognizer.recognize_google(audio)
            engine.say(purpose)
            engine.runAndWait()

            if not os.path.exists("AUB DBS"):
                os.mkdir("AUB DBS")

            with open(f"AUB DBS/Name.txt", "a") as file:
                file.write("NAME:" + text + "\n")
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write("TIME:" + strfTime + "\n") 
                file.write("ADRESS:" + address + "\n")
                file.write("PURPOSE:" + purpose + "\n")

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            print("Please check your internet connection and try again.")

        except Exception as ex:
            print(f"An error occurred: {ex}")


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            r.pause_threshold = 2
            print("Listening...")
            audio = r.listen(source, timeout=20)

            try:
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query

            except sr.UnknownValueError:
                say("Sorry, I did not hear your request. Please repeat.")
                print("Sorry, I did not hear your request. Please repeat.")

            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service: {e}")
                return "Could not request results from Google Speech Recognition service"

def find_room_number(x):
    room = ["aiml", "cse", "vc", "hod", "engineering staff room", "computer lab", "library", "registard"]
    room_numbers = [207, 206, 105, 201, 202, 203, 208, 199]

    x_lower = x.lower()

    for room, room_number in zip(room, room_numbers):
        if room in x_lower:
            return f"It is on the second floor. Room number {room_number}"

    say("Room not found.")
    return "Room not found."

def main():
    global chatStr
    query = ""
    timestamp = int(time.strftime('%H'))
    time_now = timestamp

    morning = ["Oh! Good Morning . Hope you are enjoying this peaceful morning.", "Peaceful Morning. Welcome to Amity University Bangalore",
               "Morning! I'm here to make your day smoother. Welcome to Amity University Bangalore",
               "Hello there! Wishing you a wonderful morning. Welcome to Amity University Bangalore", "Hello there! Welcome to Amity University Bangalore",
                "Happy Morning. Welcome to Amity University Bangalore"]
    afternoon = ["Hello and Good afternoon!", "Hello there! Welcome to Amity University Bangalore",
                 "Good afternoon! It's a pleasure to see you. Welcome to Amity University Bangalore",
                 "Afternoon! If there's anything you need, feel free to ask. I'm here to help.",
                 "Hello and good afternoon!. Welcome to Amity University Bangalore ", "Afternoon! I hope you're having a great day."]
    evening = ["Good evening! It's always a pleasure to see you. Welcome to Amity University Bangalore ", "Good evening! I hope your day has been fantastic",
               "Good evening! I trust you had a productive day", "Good evening! I hope the day treated you well.",
               "Good evening! I'm here to make your evening even better", "Good evening! I'm here and ready to assist"]

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img, 0.45, 0.2)

        if objectInfo:
                if time_now < 12:
                  say(random.choice(morning))
                elif time_now < 18:
                  say(random.choice(afternoon))
                else:
                  say(random.choice(evening))

        say("Aarryya under charge . Let's complete the formalities . may i know your name please?")
        ai(prompt=query)
        say("Hope you have filled your details in the register.")
        say("How can I assist you today?")
        break

        cv2.imshow("Output", img)
        cv2.waitKey(1)

    while True:
        query = takeCommand().lower()

        if "exit" in query:
            say("Goodbye!")
            break
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"the time is {strfTime}")
        elif "using artificial intelligence" in query:
            ai(prompt=query)
        elif "quit" in query:
            say("Goodbye")
            exit()
        elif "reset chat" in query:
            chatStr = ""
            say("Chat reset")
        elif "how are you" in query:
            how_are_you = ["I'm doing great, thank you for asking. How can I help you?",
                           "Feeling happy today, feel free to ask. I am there at your service.",
                           "Feeling excited to help you out. What brings you here today?"]
            say(random.choice(how_are_you))
        elif "your purpose" in query:
            say("I am a humanoid receptionist robot created by the team Roboverse for amity university bengaluru. my purpose is to handel all the receptonist task and to provide guidance, assistance and to interact with the visitors. ")
        elif "creator" in query or "father" in query:
            say("I am created by the team roboverse. The team consists of four members: Team leader and main programmer "
            "Shyamji Pandey, programmer Harshul Singh, prototyper Utkarsh Mishra, and Sumith Kumar Gupta.")
        elif "birthday" in query:
            say("As I am an artificially intelligent robot, I dont have any birthday like human. but, I was created on second of the febraury  2024 by the team roboverse .")
        elif "introduce yourself" in query:
            say("My name is Aarryaa. Aarryaa stands for Artificial Receptionist Yielding Assistance. "
                "I am a humanoid receptionist robot. I am invented to handle all the tasks of a receptionist "
                "and to guide and interact with the visitors. I am powered by AI. I have Raspberry Pi 5, which "
                "is a 64-bit quad-core processor clocked at 2.4 Giga hertz.")
        elif "shutdown" in query:
            say("Shutting down")
            os.system("shutdown /s /t 1")
        elif any(room in query for room in
                 ["aiml", "cse", "vc", "hod", "engineering staff room", "computer lab", "library", "registrard"]):
            room_info = find_room_number(query)
            say(room_info)
        elif "thank you" in query:
            say("You're most welcome! Have a nice day. Goodbye...")
            exit()
        elif "located" in query:
            say("It is located near Doddaballapura DC office, Chapparaddkallu, in Bengaluru rural district, Karnataka.")
        elif "who is head of department" in query:
            say("The head of the department for B.Tech is Dr. Swarnalatha k s")
        elif "who is the chancellor" in query:
            say("The Chancellor for Amity University Bengaluru is Dr. P Sali ")
        elif "who is the vice chancellor" in query:
            say("The Vice Chancellor for Amity University Bengaluru is Dr. Sudhakar ")
        elif "courses" in query:
            say("For UG the available programs in B tech are , Computer Science and Engineering , and , Artificial Intelligence and Machine Learning . For PG the available programs are MBA , MSc in cyber security , MSc in Data Sciences and MCA")
        elif "about amity" in query:
            say("Amity University, Bengaluru is a private university located in Bengaluru rural district in Karnataka. It was established in 2023. It has campuses in India and overseas branch campuses in London, Dubai,Singapore, and New York. The founder of the whole Amity group is Mr. Ashok Chauhan. ")
        elif "Arya Quit".lower() in query.lower():
            exit()
        else:
            print("Chatting...")
            chat(query)
classNames = []
classFile = "C:\\Users\\shyam\\Downloads\\Object_Detection_Files\\Object_Detection_Files\\coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "C:\\Users\\shyam\\Downloads\\Object_Detection_Files\\Object_Detection_Files\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "C:\\Users\\shyam\\Downloads\\Object_Detection_Files\\Object_Detection_Files\\frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)

    if len(objects) == 0:
        objects = classNames
    objectInfo = []

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0], box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0], box[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return img, objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img, 0.45, 0.2)

        # Checking if person is detected
        if objectInfo:
            main()
            break

        cv2.imshow("Output", img)
        cv2.waitKey(1)