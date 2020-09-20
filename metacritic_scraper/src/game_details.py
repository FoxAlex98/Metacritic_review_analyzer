import requests
import inquirer
import json
import yaml

with open('conf/settings.yaml') as yaml_conf:
    config_map = yaml.safe_load(yaml_conf)

KEY = config_map['key']

supported_platforms = {"PC (Microsoft Windows)":"pc", \
                        "PlayStation 4":"playstation-4","Xbox One":"xbox-one", \
                        "PlayStation 3":"playstation-3","Xbox 360":"xbox-360", \
                        "PlayStation 2":"playstation-2","Xbox":"xbox","PlayStation":"playstation", \
                        "PlayStation Portable":"psp","PlayStation Vita":"playstation-vita", \
                        "PlayStation 5":"playstation-5","Xbox Series X":"xbox-series-x", \
                        "Nintendo Switch":"switch","Wii":"wii", \
                        "Wii U":"wii-u","Nintendo 3DS":"3ds", \
                        "Google Stadia":"stadia","iOS":"ios"}
                        #n64 to add


def parse_name_to_request(name):
    name = name.strip()
    name = name.lower()
    name = name.replace(" ","%20")
    return name

def get_details(game_name):
    url = "https://api-v3.igdb.com/games/?search="
    url += parse_name_to_request(game_name)
    url += "&fields=id,name,platforms.name"
    #key
    headers = {'user-key': KEY}
    response = json.loads(requests.request("GET", url, headers=headers).text)
    #print(response)
    return response

def get_all_details(games, answers):
    game_platform = []
    game_index = int(answers[:answers.index(')')])
    for i in range(len(games[game_index]['platforms'])):
        game_platform.append(games[game_index]['platforms'][i]['name'])
    
    print(games[game_index])
    return {"game_name": games[game_index]['name'], "platforms": platform_filter(game_platform)}

def platform_filter(platforms):
    new_platforms = []
    for i in range(len(platforms)):
        try:
            new_platforms.append(supported_platforms[platforms[i]])
        except KeyError as err:
            print("platform " + platforms[i] + " not supported")
            continue
    return new_platforms

def get_game_details():
    games = []
    while not games:
        game_name = input('Please enter the name of name that you want to analyze: ')
        if game_name.strip() != "":
            games = get_details(game_name)
            if not games:
                print("Nothing found :(\n Try again ...")
        else:
            print("Not Valid Input")

    games_list = []
    for i in range(len(games)):
        tmp = str(i) + ") " + str(games[i]['name']) + "   {"
        try:
            for j in range(len(games[i]['platforms'])):
                tmp += " - " + str(games[i]['platforms'][j]['name'])
            tmp += " - }"
            games_list.append(tmp)
        except KeyError as err:
            continue


    questions = [
        inquirer.List('game',
                    message="I found these results. Which one do you want to choose?",
                    choices=games_list,
                    carousel=True
                    ),
    ]
    answers = inquirer.prompt(questions)

    return get_all_details(games, answers['game'])