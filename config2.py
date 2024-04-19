class Colors:
    TITLE = '\x1b[1;34;47m'
    NUM_CHARS = '\x1b[1;30;43m'
    END_COLOR = '\x1b[0m'
    QUESTION = '\x1b[1;37;44m'
    CONNECT = '\x1b[1;32;40m'
    TIMER = '\x1b[1;91;40m'
    TIMER_V2 = '\x1b[1;37;41m'
    HOLONIA = '\x1b[1;33;45m'
    PLAYER = '\x1b[1;95;40m'
    LOVE = '\x1b[1;95m'
    JUNGLE = '\x1b[1;33;40m'


names = [
    "Napoleong Meowparte",
    "Genghis Cat",
    "Cleopetra",
    "Queen Elizabark",
    "Abraham Lincolnt",
    "Winston Purrchill",
    "Mahatma Ghandog",
    "Nelson Meowdela",
    "Che Guevarraffe",
    "Barack Obeagle",
    "Donald Trumpasaurus Rex",
    "Joe Bidenten",
    "Vladimir Pawtin",
    "Angela Mer-cat",
    "Justin Tru-doe-doe",
    "Kim Jong-Unicorn",
    "Jacinda Ardernimal",
    "Emmanuel Macaw",
    "Scott Morrisonkey",
    "Jair Bolsonarrow"
]

conspquestions = [
    # Science and Technology
    "The Earth revolves around the Sun.",
    "Dinosaurs went extinct due to a meteor impact.",
    "Wi-Fi signals cause cancer.",
    "5G technology is used to control minds.",
    "Humans share about 50% of their DNA with bananas.",
    "The moon is made of cheese.",
    "GMOs are dangerous and cause health problems.",
    "Scientists are hiding the existence of Bigfoot.",

    # History and Events
    "World War II ended in 1945.",
    "The Titanic sank after hitting an iceberg.",
    "The 9/11 attacks were orchestrated by the US government.",
    "The Apollo 11 mission was a hoax.",
    "The assassination of JFK was a conspiracy.",
    "The Bermuda Triangle causes ships and planes to disappear.",
    "Area 51 houses evidence of extraterrestrial life.",
    "The Earth is less than 10,000 years old.",

    # Health and Medicine
    "Smoking cigarettes can cause lung cancer.",
    "Vaccines help prevent diseases.",
    "Drinking water is essential for human survival.",
    "Eating too much sugar is bad for your health.",
    "Positive thinking can cure cancer.",
    "Pharmaceutical companies are hiding natural cures for diseases.",
    "Chemtrails are used to control the population.",
    "The COVID-19 pandemic was planned.",

    # Society and Culture
    "Shakespeare wrote many famous plays.",
    "The Mona Lisa painting was stolen in 1911 and later recovered.",
    "The Earth is hollow and inhabited by a secret civilization.",
    "Reptilian humanoids control world governments.",
    "Paul McCartney died in the 1960s and was replaced by a look-alike.",
    "The Illuminati controls Hollywood and the music industry.",
    "Secret societies rule the world.",
    "The moon landing was filmed in a Hollywood studio.",

    # Miscellaneous
    "The population of the Earth is over 7 billion people.",
    "The Great Wall of China is visible from space.",
    "The Earth's core is extremely hot.",
    "Dogs are descended from wolves.",
    "The Loch Ness Monster is a real creature.",
    "The pyramids were built as energy sources by ancient civilizations.",
    "Time travel is possible.",
    "Parallel universes exist."
]

conspanswers = [
    # Science and Technology
    True,
    True,
    False,
    False,
    True,
    False,
    False,
    False,

    # History and Events
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,

    # Health and Medicine
    True,
    True,
    True,
    True,
    False,
    False,
    False,
    False,

    # Society and Culture
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,

    # Miscellaneous
    True,
    False,
    True,
    True,
    False,
    False,
    False,
    False,
]


video_game_statements = [
    # Positive statements
    "Video games improve cognitive skills.",  # True
    "Multiplayer games foster teamwork and communication.",  # True
    "Speedrunning enhances problem-solving abilities.",  # True
    "Exploring open-world games stimulates creativity.",  # True
    "Gaming can reduce stress and anxiety.",  # True
    "Achievement hunting adds replay value to games.",  # True
    "Game soundtracks contribute to the overall experience.",  # True
    "E-sports require dedication and skill.",  # True
    "Mods enhance gameplay in many PC games.",  # True
    "Game developers often include Easter eggs.",  # True
    "Playing retro games invokes nostalgia.",  # True
    "Video game music can be emotionally powerful.",  # True
    "Gaming communities provide a sense of belonging.",  # True
    "Game design involves balancing challenge and fun.",  # True
    "Exploring virtual worlds is an adventure.",  # True
    "Video games encourage persistence and resilience.",  # True
    "Local co-op games strengthen friendships.",  # True
    "Game graphics have evolved significantly over time.",  # True
    "Game narratives can be as impactful as books or movies.",  # True
    "Game speedruns showcase impressive skills.",  # True

    # Negative statements
    "Graphics and visual effects significantly impact gameplay.",  # False
    "Console gaming is more popular than PC gaming.",  # False
    "Video games cause violence in real life.",  # False
    "Game developers always meet release deadlines.",  # False
    "Mobile games lack depth compared to PC/console games.",  # False
    "Quick-time events (QTEs) are universally loved.",  # False
    "Microtransactions improve the gaming experience.",  # False
    "All gamers prefer competitive PvP over cooperative PvE.",  # False
    "Single-player games are becoming obsolete.",  # False
    "Gaming addiction affects only a small percentage of players."  # False
]

# Corresponding boolean answers
video_games_answers = [True, True, True, True, True, True, True, True, True, True,
                   True, True, True, True, True, True, True, True, True, True,
                   False, False, False, False, False, False, False, False, False, False]

sportquestions = [
    "Basketball was invented in Canada.",
    "The FIFA World Cup is held every two years.",
    "The first modern Olympic Games were held in Athens, Greece, in 1896.",
    "The Super Bowl is the championship game of the National Football League (NFL).",
    "Tennis is played with a shuttlecock.",
    "The Tour de France is a famous cycling race.",
    "The sport of judo originated in Japan.",
    "The term 'Hat trick' refers to scoring three goals in soccer.",
    "The Rugby World Cup is held every four years.",
    "The sport of cricket originated in England.",
    "The first Wimbledon tennis championship was held in 1877.",
    "Muhammad Ali was a famous boxer.",
    "The New York Yankees are a baseball team.",
    "The Olympic Games have never been held in Africa.",
    "The Stanley Cup is awarded to the winner of the NHL playoffs.",
    "The sport of golf originated in Scotland.",
    "The Indianapolis 500 is a famous auto race.",
    "Michael Phelps is a famous swimmer.",
    "The term 'touchdown' is used in American football.",
    "The FIFA Women's World Cup is held every four years.",
    "The Boston Celtics are a basketball team.",
    "The sport of volleyball was invented in the United States.",
    "The first modern Olympic Games included only summer sports.",
    "Roger Federer is a professional tennis player.",
    "The sport of rugby originated in England.",
    "The Green Bay Packers are a football team.",
    "The sport of surfing originated in Hawaii.",
    "The UEFA Champions League is an annual soccer tournament.",
    "The term 'ace' is used in tennis.",
    "The NBA Draft is an event where teams select college basketball players."
]

# List of corresponding True or False answers
sportanswers = [
    False, False, True, True, False, True, False, True, True, False,
    True, True, False, False, True, True, True, True, True, True,
    False, True, True, False, False, False, True, True, True, True
]