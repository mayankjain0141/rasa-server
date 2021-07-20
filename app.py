import os
import logging
import uuid
import asyncio
import subprocess
import json
from flask import Flask
from flask import request,abort
from rasa.core.agent import Agent
#from waitress import serve

logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')

loop = asyncio.get_event_loop()
app = Flask(__name__)

agents = {}

def __load_agent(game):
    model_path = './models/{}.tar.gz'.format(game)
    return Agent.load(model_path=model_path)

def __load_all_agents():
    ''' Function for loading all the agents
        and storing them in a dictionary '''
    with open('models.json', 'r') as filehandle:
        data = json.load(filehandle)        
        for key in data:
            agents[key] = __load_agent(key)
    
    
@app.route('/create_game',methods=['GET','POST'])
def create_game():
    ''' Route for creating a game '''    
    game = str(request.json.get('game'))
    
    with open('models.json', 'r') as filehandle:
        data = json.load(filehandle)
    
    if(data.get(game) is not None):
        abort(404,description="Model already exists")
    # Executes script for training the model
    val = subprocess.check_call("./script.sh '%s'" % game,shell=True)
    agents[game] = __load_agent(game)    

    data[game] = 1
    with open('models.json', 'w') as filehandle:
        json.dump(data,filehandle,indent=2)
    
    return "SUCCESS! Model has been created!"



@app.route('/update_game',methods=['GET','POST'])
def update_game():
    ''' Route for updating a game '''    
    game = str(request.json.get('game'))
    
    with open('models.json', 'r') as filehandle:
        data = json.load(filehandle)
    
    if(data.get(game) is None):
        abort(404,description="Model doesn't exist")
    
    # Executes script for training the model
    val = subprocess.check_call("./script.sh '%s'" % game,shell=True)
    agents[game] = __load_agent(game)    

    data[game] = 1
    with open('models.json', 'w') as filehandle:
        json.dump(data,filehandle,indent=2)
    
    return "SUCCESS! Model has been updated!"

@app.route('/delete_game',methods=['GET','POST'])
def delete_game():    
    ''' Route for deleting a game '''
    game = str(request.json.get('game'))
    
    with open('models.json', 'r') as filehandle:
        data = json.load(filehandle)
    
    if(data.get(game) is None):
        abort(404,description="Model doesn't exist")
    
    model_path = './models/{}.tar.gz'.format(game)
    os.remove(model_path)     # Deleting the model.tar.gz file    
    del agents[game]          # Deleting the loaded model from agents dict   
    del data[game]            # Deleting the model from models.json  
    with open('models.json', 'w') as filehandle:
        json.dump(data,filehandle,indent=2)
    
    return "SUCCESS! Model has been deleted!"

@app.route('/', methods=['GET', 'POST'])
def play_game():
    ''' Route for playing a game '''
    sid = str(request.json.get('sid'))
    message = str(request.json.get('message'))
    game = str(request.json.get('game'))    
    agent = agents.get(game)
    
    if(agent is None):
        abort(404,description="Model not found")
    
    bot_response = loop.run_until_complete(
        agent.parse_message_using_nlu_interpreter(message_data=message)
    )
    return bot_response

if __name__ == '__main__':
	#serve(app, host = "0.0.0.0", port = 8080)
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    __load_all_agents()
    app.run(host, port, debug=False, use_reloader=False)
