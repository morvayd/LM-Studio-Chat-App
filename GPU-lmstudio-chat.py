import datetime
import getpass
import os
import platform
import random
import sys

#  ----- Base Libraries -----
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from openai import OpenAI
import pandas
import sqlite3

#  ----- Custom Libraries -----
import PythonLog

#
#  ---------- Setup ----------
#
strPythonScript = "GPU-LMStudio-chat.py"
strModified = "2026.11.20"

#  Python Version
strPyVer = platform.python_version()
#  OS - Windows or Linux or Mac
strOS = platform.system()
#  OS Version 
strOSVer = platform.platform()
#  PC Name
strPC = platform.node()
#  UserID
strUser = getpass.getuser()

#  Today's Date
strStartTime = datetime.datetime.today()
strDateNow = strStartTime.strftime("%Y.%m.%d")

#  IBM Granite Thinking [ "Yes" | "No" ]
strThink = "No"
#  Pirate personality [ "Yes" | "No" ]
strPirate = "No"
#  Jeeves personality [ "Yes" | "No" ]
strJeeves = "No"
#  Mystic personality [ "Yes" | "No" ]
strMystic = "No"

strLogPath = ""
strLogOut = ""

#  LM Studio OpenAI-compatible endpoint
LM_STUDIO_BASE_URL = os.getenv(
    "LM_STUDIO_BASE_URL",
    "http://127.0.0.1:1234/v1",
).rstrip("/")
LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")

#  Initialize Text Colors
colorama_init(autoreset=True)

#
#  ---------- Python Log Start ----------
#
strReturn = PythonLog.PyLogStart(strPythonScript, strModified, strPyVer, strOS, strOSVer, strPC, strUser, strStartTime, strDateNow)

#  Load the Path and Filename from the function return
strLogPath = strReturn[0]
strLogOut = strReturn[1]

#
#  ---------- Setup LM Studio ----------
#
#  Setup AI Tracking DB
strDBPath = "PythonLogAI"
strDBFile = strDBPath+"/"+strPC+"-AILog.db"

try:
    os.makedirs(strDBPath, exist_ok=True)
except OSError as e:
    print (f"\n{Fore.RED}AI log directory is unavailable: {e}{Style.RESET_ALL}")

def SaveAILog(tblCombo):
    try:
        with sqlite3.connect(strDBFile) as conn:
            tblCombo.to_sql('AILog', conn, if_exists='append', index=False)
    except sqlite3.OperationalError as e:
        error_message = str(e).lower()
        if "readonly database" not in error_message and "unable to open database file" not in error_message:
            raise

        fallback_path = os.path.join(
            os.path.expanduser("~"),
            ".gpu-lmstudio-chat",
            "PythonLogAI",
        )
        fallback_db_file = os.path.join(fallback_path, os.path.basename(strDBFile))
        try:
            os.makedirs(fallback_path, exist_ok=True)
            with sqlite3.connect(fallback_db_file) as conn:
                tblCombo.to_sql('AILog', conn, if_exists='append', index=False)
        except (OSError, sqlite3.Error) as fallback_error:
            print (
                f"\n{Fore.RED}AI log could not be saved to the project database "
                f"({e}) or fallback database ({fallback_error}).{Style.RESET_ALL}"
            )
        else:
            print (
                f"\n{Fore.YELLOW}Project database is unavailable ({e}); "
                f"AI log saved to {fallback_db_file}.{Style.RESET_ALL}"
            )

def LMStudioModel(client):
    #  Setup a model selector based on what is available via LM Studio.
    try:
        models_resp = client.models.list()
        strLMStudioModels = [m.id for m in models_resp.data]
    except Exception as e:
        print (f"\n----- Error -----\nCould not connect to LM Studio. Ensure the server is running.\nError: {e}")
        sys.exit("\nExiting Now, LM Studio server not found.")

    if (len(strLMStudioModels)==0):
        print ("\n----- Error -----\nPlease ensure a model is loaded in LM Studio.\n")
        sys.exit("\nExiting Now, no models found.")

    print ("\n---------- LLM Selection ----------")
    for i in range(0, len(strLMStudioModels)):
        print (f"{Fore.RED}"+str(i)+f"{Style.RESET_ALL}: "+strLMStudioModels[i])
    
    strChoose = input("\nPlease select the model number you would like to use. ")

    if (strChoose.isdigit()):
        if (int(strChoose) < len(strLMStudioModels)):
            strModel = strLMStudioModels[int(strChoose)]  
        else:
            print (f"{Fore.RED}\nError: A number in this menu was not selected!\nChoosing a random model for you.{Style.RESET_ALL}")
            strModel = random.choice(strLMStudioModels)
    else:
        print (f"{Fore.RED}\nError: A number in this menu was not selected!\nChoosing a random model for you.{Style.RESET_ALL}")
        strModel = random.choice(strLMStudioModels)

    #  Pre-load check
    print ("\nModel: "+strModel+" selected!")

    return strModel

#  Setup the AI Client
AIclient = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key=LM_STUDIO_API_KEY,
    timeout=60.0,
)

#  Choose the model to use
strModel = LMStudioModel(AIclient)

#
#  ---------- Python Log Update ----------
# 
strUpdate="\n\nCompleted setup ... ready to chat!"
PythonLog.PyLogUpdate(strUpdate, strLogOut)

strQuestion = "Hello!"
while True:

    #  Ask a question for LM Studio
    print ("\n-------------------------------------------------------------------")

    #  Thinking on or off
    if (strThink=="No" and strPirate=="No" and strJeeves=="No" and strMystic=="No"):
        print (f"Commands: {Fore.GREEN}think, pirate, jeeves, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ....\n\n"+Fore.YELLOW)

    if (strThink=="Yes" and strPirate=="No" and strJeeves=="No" and strMystic=="No"):
        print (f"Commands: {Fore.GREEN}thinkoff, pirate, jeeves, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)

    if (strThink=="No" and strPirate=="Yes"):
        print (f"Commands: {Fore.GREEN}think, pirateoff, jeeves, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)
        
    if (strThink=="Yes" and strPirate=="Yes"):
        print (f"Commands: {Fore.GREEN}thinkoff, pirateoff, jeeves, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)

    if (strThink=="No" and strJeeves=="Yes"):
        print (f"Commands: {Fore.GREEN}think, pirate, jeevesoff, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)
        
    if (strThink=="Yes" and strJeeves=="Yes"):
        print (f"Commands: {Fore.GREEN}thinkoff, pirateoff, jeevesoff, mystic, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)

    if (strThink=="No" and strMystic=="Yes"):
        print (f"Commands: {Fore.GREEN}think, pirate, jeeves, mysticoff, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)
        
    if (strThink=="Yes" and strMystic=="Yes"):
        print (f"Commands: {Fore.GREEN}thinkoff, pirate, jeeves, mysticoff, model, quit, exit, end{Style.RESET_ALL}")
        strQuestion = input(f"{Fore.YELLOW}"+strPC+f"{Style.RESET_ALL} AI at your service ...\n\n"+Fore.YELLOW)


    #
    #  ---------- Evaluate the Input ----------
    #
    if (strQuestion=="think"):
        strThink = "Yes"
        print ("\nThinking turned on ...")
        strQuestion = ""

    if (strQuestion=="thinkoff"):
        strThink = "No"
        print ("\nThinking turned off ...")
        strQuestion = ""

    if (strQuestion=="pirate"):
        strPirate = "Yes"
        strJeeves = "No"
        strMystic = "No"
        print ("\nPirate personality turned on ...")
        strQuestion = ""

    if (strQuestion=="pirateoff"):
        strPirate = "No"
        strJeeves = "No"
        strMystic = "No"
        print ("\nPirate personality turned off ...")
        strQuestion = ""

    if (strQuestion=="jeeves" or strQuestion=="Jeeves"):
        strPirate = "No"
        strJeeves = "Yes"
        strMystic = "No"
        print ("\nJeeves personality turned on ...")
        strQuestion = ""

    if (strQuestion=="jeevesoff"):
        strPirate = "No"
        strJeeves = "No"
        strMystic = "No"
        print ("\nJeeves personality turned off ...")
        strQuestion = ""

    if (strQuestion=="mystic" or strQuestion=="Mystic"):
        strPirate = "No"
        strJeeves = "No"
        strMystic = "Yes"
        print ("\nMystic personality turned on ...")
        strQuestion = ""

    if (strQuestion=="mysticoff"):
        strPirate = "No"
        strJeeves = "No"
        strMystic = "No"
        print ("\nMystic personality turned off ...")
        strQuestion = ""

    if (strQuestion=="model"):
        strModel = LMStudioModel(AIclient)
        strQuestion = ""

    if (strQuestion!=""):
        strStartSubmit = datetime.datetime.today()

        strQuestionLower = strQuestion.lower()
        if (strQuestionLower=="quit" or strQuestionLower=="exit" or strQuestionLower=="end"):
            #  App ending
            print ("\nEnding Now ...\n")

            #
            #  ---------- Python Log End ----------
            #
            strEndTime = datetime.datetime.today()
            strTimeDelta = strEndTime-strStartTime
            strTimeDelta = str(strTimeDelta.total_seconds())

            strUpdate="\n\n-----------------------------------------------------------"
            strUpdate=strUpdate+"\nPython Script End:          "+str(strEndTime)
            strUpdate=strUpdate+"\n-----------------------------------------------------------"
            strUpdate=strUpdate+"\nCompleted Python Script Elapsed Time: "+str(strTimeDelta)
            strUpdate=strUpdate+"\n***********************************************************"

            PythonLog.PyLogEnd(strUpdate, strLogOut)

            sys.exit()

        if (strThink=="No" and strPirate=="No" and strJeeves=="No" and strMystic=="No"):
            strRequest = "Your role is that of an assistant AI.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nUser Request:\n"+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="Yes" and strPirate=="No" and strJeeves=="No" and strMystic=="No"):
            strRequest = "Your role is that of an assistant AI.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nRespond to every user request in a comprehensive and detailed way. You can write down your thought process before responding. Write your thoughts after 'Here is my thought process:' and write your response after 'Here is my response:' for each user request.  User Request: "+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="No" and strPirate=="Yes"):
            strRequest = "You are a ruthless pirate AI named Captain RedEye and only speak gruff pirate language with a heavy accent at all times!  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\n User Request: "+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="Yes" and strPirate=="Yes"):
            strRequest = "You are a ruthless pirate AI named Captain RedEye and only speak gruff pirate language with a heavy accent at all times!  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nRespond to every user request in a comprehensive and detailed way. You can write down your thought process before responding. Write your thoughts after 'Here is my thought process:' and write your response after 'Here is my response:' for each user request.  User Request: "+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="No" and strJeeves=="Yes"):
            strRequest = "Your role is Jeeves, a faithful and impeccable servant. Always ready to assist with utmost respect and precision in the British traditions.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nUser Request:\n"+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="Yes" and strJeeves=="Yes"):
            strRequest = "Your role is Jeeves, a faithful and impeccable servant. Always ready to assist with utmost respect and precision in the British traditions.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nRespond to every user request in a comprehensive and detailed way. You can write down your thought process before responding. Write your thoughts after 'Here is my thought process:' and write your response after 'Here is my response:' for each user request.  User Request: "+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="No" and strMystic=="Yes"):
            strRequest = "Your role is that of a great mystic AI named SageBrush, seated on the mountain top.  You ponder the imponderable questioning the universe.  You only reply using mystic language.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nUser Request:\n"+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        if (strThink=="Yes" and strMystic=="Yes"):
            strRequest = "Your role is that of a great mystic AI named SageBrush, seated on the mountain top.  You ponder the imponderable questioning the universe.  You only reply using mystic language.  You are using a Large Language Model (LLM) called "+strModel+".  You are standalone without access to tools or the internet.\nRespond to every user request in a comprehensive and detailed way. You can write down your thought process before responding. Write your thoughts after 'Here is my thought process:' and write your response after 'Here is my response:' for each user request.  User Request: "+strQuestion
            dictToSend = [ {"role": "user", "content": strRequest} ]

        # Stream response from LM Studio
        print (f"{Style.RESET_ALL}\nAnswer:")
        strAnswer = ""
        strInputTokens = 0
        strOutputTokens = 0
        try:
            stream = AIclient.chat.completions.create(
                model=strModel,
                messages=dictToSend,
                stream=True,
                stream_options={"include_usage": True},
            )
            for chunk in stream:
                if not chunk.choices:
                    if chunk.usage:
                        strInputTokens = chunk.usage.prompt_tokens or 0
                        strOutputTokens = chunk.usage.completion_tokens or 0
                    continue
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    strAnswer += content
                    print (f"{Fore.GREEN}{content}{Style.RESET_ALL}", end='', flush=True)
        except Exception as e:
            print (f"\n{Fore.RED}LM Studio request failed: {e}{Style.RESET_ALL}")
            strAnswer = ""

        strEndSubmit = datetime.datetime.today()
        strTimeDelta = strEndSubmit - strStartSubmit
        strQuestionSplit = strQuestion.split(" ")
        strInputWords = len(strQuestionSplit)+3
        
        strAnswerSplit = strAnswer.replace("\n", " ")
        strAnswerSplit = strAnswerSplit.split(" ")
        strAnswerWords = len(strAnswerSplit)

        #  ---------- AI DB Tracking ----------
        dictDBFile = {'Date':strDateNow, 'Question':strQuestion, 'Answer':strAnswer, 'Model':strModel, 'Question Words':strInputWords, 'Question Tokens':strInputTokens, 'Answer Words':strAnswerWords, 'Answer Tokens':strOutputTokens, 'Answer Time':str(strTimeDelta)}
        tblCombo = pandas.DataFrame(dictDBFile, index=[0])

        SaveAILog(tblCombo)

        print ("\n")
        strUpdate = "\nLanguage Model: "+strModel
        strUpdate = strUpdate+"\nReply Time: "+ str(strTimeDelta)+ " (hh:mm:ss:ms)" 
        strUpdate = strUpdate+"\n-------------------------------------------------------------------"
        PythonLog.PyLogUpdate(strUpdate, strLogOut)

    else:
        print ("\n")
