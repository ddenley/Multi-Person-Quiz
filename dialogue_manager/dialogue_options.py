import random


def question_options(options: list, multipleChoices: bool) -> str:
    """
    Return a random question string from the list available.
    This chooses a random start and end phrase to create a large number of unique question formulations.
    """
    if multipleChoices:
        middle = f"Is this the flag of {options[0]}, {options[1]}, {options[2]} or {options[3]}?"
    else:
        middle = ''
    return f"{__questions[random.randint(0, len(__questions) - 1)]} {middle} " \
           f"{__end_phrase[random.randint(0, len(__end_phrase) - 1)]}"


__end_phrase = [
        "Discuss it with your quiz team and give me your best guess.",
        "Discuss it with your quiz team and give me the country you think it is.",
        "Let's hear your team's prediction on which country it might be.",
        "After some deliberation, I want to know your team's estimation of the country.",
        "It's time to huddle up and come up with your most informed guess on the country.",
        "Talk amongst yourselves and then share your team's country selection.",
        "Collaborate and give me the name of the country that you think it is.",
        "After some discussion, I want to hear your team's best guess on the country.",
        "Take a few moments to confer with your team and offer the name of the country you think it is.",
        "Let's hear your team's most confident country guess after some collaboration.",
        "It's time to put your heads together and come up with a country name that you think fits.",
        "Work together to come up with your team's most informed country selection.",
        "After some deliberation, I want to hear your team's most accurate country guess.",
        "Take a moment to discuss with your team and share the country you think it is.",
        "It's time to collaborate and give me your team's best guess on the country.",
        "Discuss it with your quiz team and offer the name of the country you think it is.",
        "Let's hear your team's most educated guess on the country after some deliberation.",
        "After some discussion, I want to know your team's most confident country estimation.",
        "Take a few moments to confer with your team and offer your most accurate country guess.",
        "It's time to put your heads together and come up with your most informed country selection.",
        "Work together to give me the name of the country that you think it is.",
        "After some deliberation, I want to hear your team's best country guess.",
        "Collaborate and give me the country name that you think it is.",
        "Discuss it with your quiz team and share your most well-reasoned country selection.",
        "Let's hear your team's most calculated guess on the country after some collaboration.",
        "After some discussion, I want to know your team's most thoughtful country estimation.",
        "It's time to huddle up and come up with your most confident guess on the country.",
        "Take a few moments to confer with your team and offer your most well-informed country guess.",
        "Work together and give me the name of the country that you think it is.",
        "After some deliberation, I want to hear your team's most accurate estimation of the country.",
        "Collaborate and give me your team's most informed country guess.",
        "Discuss it with your quiz team and give me your most educated country selection.",
        "Let's hear your team's most calculated country guess after some collaboration.",
        "After some discussion, I want to know your team's most thoughtful country estimation.",
        "It's time to put your heads together and come up with your most confident country selection.",
        "Work together and give me the name of the country that you think it is.",
        "After some deliberation, I want to hear your team's most well-reasoned country guess.",
        "Collaborate and offer your team's most thoughtful country selection.",
        "Discuss it with your quiz team and give me your most informed guess on the country.",
        "Let's hear your team's most accurate country selection after some collaboration.",
        "After some discussion, I want to know your team's most confident estimation of the country.",
        "It's time to put your heads together and come up with a well-informed guess.",
        "I want to hear your team's guess after some discussion and collaboration.",
        "Take a moment to discuss with your team before offering your most thoughtful guess.",
        "Let's hear your team's prediction after a little bit of brainstorming.",
        "Work together to come up with your best guess and share it with me.",
        "I want to hear your team's most calculated guess after some discussion.",
        "It's time to collaborate and come to a consensus before making your guess.",
        "Take a few moments to discuss with your team before offering your most confident guess.",
        "It's time to combine your knowledge and make your best collective guess.",
        "After some deliberation, I want to hear your team's most informed guess.",
        "Work together to make your most accurate guess and share it with me.",
        "Let's hear your team's most well-reasoned guess after some collaboration.",
        "I want to know your team's prediction after a little bit of group discussion.",
        "It's time to put your heads together and come up with a thoughtful guess.",
        "After some deliberation, I want to hear your team's most calculated guess.",
        "Take a few moments to confer with your team and offer your most confident guess.",
        "It's time to collaborate and come up with a well-informed guess.",
        "Now is the time to work together and make your best guess.",
        "Talk amongst yourselves and then share your team's most educated guess.",
        "After a little bit of brainstorming, I want to hear your team's prediction.",
        "It's time to combine your knowledge and make your best collective guess.",
    ]

__questions = [
        f"Which country's flag is about to be displayed?",
        f"Can you identify the upcoming flag?",
        f"What is the flag that will be shown next?",
        f"Do you recognize the flag that is about to be revealed?",
        f"Which nation's banner will be shown next?",
        f"What's the next country flag that will be displayed?",
        f"Which national flag is coming up next?",
        f"Which flag is about to be unveiled?",
        f"Can you predict the next flag to be shown?",
        f"Which flag is scheduled to be displayed next?",
        f"What flag is next in line to be shown?",
        f"Do you know the flag that will be displayed next?",
        f"Which nation's banner will be displayed next?",
        f"What country's flag will be shown next?",
        f"Which flag will be raised next?",
        f"What is the upcoming flag?",
        f"Can you identify the flag that will be displayed next?",
        f"What is the next country's flag to be shown?",
        f"Which flag will be on display next?",
        f"What is the next flag in the queue?",
        f"What flag is next to be raised?",
        f"Which flag is next in the sequence?",
        f"What flag is coming up next in the lineup?",
        f"Which flag is next on the list?",
        f"What flag will be raised next?",
        f"What is the flag that will be shown immediately after this?",
        f"Which country's flag is next on the list?",
        f"Which flag will be unveiled after this one?",
        f"Can you guess the next flag that will be shown?",
        f"Which flag will be up next?",
        f"What flag will be displayed next in the lineup?",
        f"Which country's banner is up next?",
        f"Which flag is the next to be revealed?",
        f"What flag will be shown after this one?",
        f"What is the flag that will be displayed immediately following this?",
        f"Which country's flag comes after this one?",
        f"What is the next flag that will be raised up?",
        f"Which flag will be displayed after this one is taken down?",
        f"What is the upcoming flag to be displayed?",
        f"Can you identify the flag that will be shown after this?",
        f"Which flag will be up right after this one?",
        f"Which flag is next in the order?",
        f"What is the next national flag to be displayed?",
        f"What is the next flag that will be unveiled?",
        f"Which country's banner will be raised next?",
        f"What is the flag that is coming up next?",
        f"Can you guess the flag that will be displayed immediately after this one?",
        f"Which flag is next in the lineup?",
        f"What is the next flag that will be raised up?",
        f"Which national flag is scheduled to be shown next?",
    ]

def greeting_options():
    """Provide some randomisation of the greeting at the start of the quiz."""
    return __greetings[random.randint(0, len(__greetings) - 1)]


__greetings = [
    "Up for a team challenge? Let's see if you can match each flag to its country!",
    "Fancy a cooperative game? Put your knowledge to the test by associating each flag with its country!",
    "Care to join in? Match the flag with its respective country and let's see how you do!",
    "Are you game for a game? Show us your skills by matching the flag to its country.",
    "Feeling up for a group game? See if you can identify the country by the flag!",
    "Care to take a shot? Try to connect each flag with the right nation!",
    "Shall we give it a go? Pick which country each flag represents!",
    "Up for a game? See if you can match the flag to the country it belongs to!",
    "Shall we start? See if your knowledge is up to par by matching each flag to its home nation!",
    "Do you think you can do it? Connect the flag with the correct country!",
    "Ready to play? Let's test your knowledge by matching the flag to the nation!",
    "Want to give it a shot? Link each flag with its corresponding country!",
    "Would you like to take a chance? Can you identify the country by the flag?",
    "Would you be daring enough to try? Uncover the nation hidden behind the flag!",
    "Are you ready? See if you can recognize the country from the flag!",
    "Are you game? See if you can identify the flag's country of origin!",
    "Would you like to play? Match the flag with the corresponding country to complete the puzzle!",
    "Up for a challenge? Try to recognize each flag's country!",
    "Would you like to try a game? See if you figure out the country of each flag.",
    "Are you ready? See if you can connect the flag to its home nation!",
]


def provide_clue(country: str) -> str:
    """Provide a clue related to the given country name."""
    return __clues[country.casefold()]


clues = {
        "Afghanistan": "Landlocked country in South Central Asia",
        "Albania": "Country in Southeastern Europe",
        "Algeria": "Country bordering Libya and Tunisia in the southern Mediterranean coast of North Africa",
        "American Samoa": "Pacific Island group",
        "Andorra": "Tiny principality between France and Spain",
        "Angola": "Southern African country",
        "Anguilla": "British overseas territory in the Caribbean Sea",
        "Antarctica": "The world's southernmost continent",
        "Antigua and Barbuda": "Twin-island country in the Eastern Caribbean Sea",
        "Argentina": "South American country.",
        "Armenia": "Landlocked country in the Caucasus region",
        "Aruba": "Dutch Caribbean island in the Caribbean Sea",
        "Australia": "The world's smallest continent.",
        "Austria": "Central European country",
        "Azerbaijan": "Country in the Caucasus region, bordered by Russia and Iran",
        "The Bahamas": "Island country in the Caribbean Sea",
        "Bahrain": "Island nation in the Persian Gulf",
        "Bangladesh": "Asian country bordered by Myanmar",
        "Barbados": "Caribbean island in the Western Atlantic Ocean",
        "Belarus": "Landlocked nation in Eastern Europe",
        "Belgium": "Western European country bordered by France, Luxembourg and the Netherlands",
        "Belize": "Central American country bordered by Guatemala and Mexico",
        "Benin": "A West African country south of Niger.",
        "Bermuda": "Known for its pink sand beaches",
        "Bhutan": "Land of the Thunder Dragon",
        "Bolivia": "A South American country",
        "Bonaire": "Caribbean island off the coast of Venezuela",
        "Bosnia and Herzegovina": "A Balkans country",
        "Botswana": "Large African country bordering South Africa",
        "Bouvet Island": "The southernmost island of the world",
        "Brazil": "Large South American country",
        "British Indian Ocean Territory": "Islands in the Indian Ocean near the Maldives",
        "Brunei Darussalam": "A country in Southeast Asia",
        "Bulgaria": "Balkan country on the Black Sea",
        "Burkina Faso": "West African country",
        "Burundi": "East African country bordering Rwanda",
        "Cabo Verde": "Island nation off of the west coast of Africa.",
        "Cambodia": "Southeast Asian country.",
        "Cameroon": "Central African country.'",
        "Canada": "Largest country in the Americas",
        "The Cayman Islands": "Caribbean islands located south of Cuba",
        "The Central African Republic": "Centrally located in Africa",
        "Chad": "Large landlocked country in North Central Africa",
        "Chile": "South American country, home to the Atacama Desert",
        "China": "Most populous country in the world",
        "Christmas Island": "Island in the Indian Ocean that is part of Australia",
        "The Cocos Keeling Islands": "Islands in the Indian Ocean that is part of Australia",
        "Colombia": "South American country.",
        "Comoros": "Island nation off the east coast of Africa",
        "The Democratic Republic of The Congo": "Central African country.",
        "The Congo": "Central African country.",
        "Cook Islands": "Island group in the South Pacific",
        "Costa Rica": "Central American country.",
        "Croatia": "European nation located along the Adriatic Sea",
        "Cuba": "Famous Caribbean island.",
        "Curacao": "Caribbean island nation off the coast of Venezuela",
        "Cyprus": "Mediterranean island divided into two parts",
        "Czechia": "Landlocked between Germany and Poland",
        "Cote d'Ivoire": "Country on the Gulf of Guinea",
        "Denmark": "Scandinavian country",
        "Djibouti": "East African nation bordering the Red Sea",
        "Dominica": "Island nation in the Caribbean, not to be confused with the Dominican Republic",
        "The Dominican Republic": "Caribbean country sharing an island with Haiti",
        "Ecuador": "South American country on the Pacific Coast",
        "Egypt": "North African country on the Mediterranean.",
        "El Salvador": "Central American country, the smallest and most densely populated in the region",
        "Equatorial Guinea": "Central African nation bordered by Cameroon and Gabon",
        "Eritrea": "East African nation on the Red Sea",
        "Estonia": "Baltic country in Northern Europe",
        "Eswatini": "A landlocked country in Southern Africa, it is bordered by Mozambique.",
        "Ethiopia": "East African nation, home to the ancient city of Aksum.",
        "Falkland Islands": "Islands in the South Atlantic Ocean.",
        "Faroe Islands": "Islands in the North Atlantic Ocean.",
        "Fiji": "Islands in the South Pacific Ocean.",
        "Finland": "Northern European nation.",
        "France": "Western European country.",
        "French Guiana": "Overseas Department of France on the Caribbean coast of South America",
        "French Polynesia": "Islands in the South Pacific Ocean known for their blue-water lagoons",
        "French Southern Territories": "Territory of France in the Indian Ocean and Antarctica",
        "Gabon": "Central African nation on the Gulf of Guinea",
        "The Gambia": "Small West African nation bounded by the Atlantic Ocean on one side and Senegal on the other",
        "Georgia": "Country in the Caucasus region of Eurasia, bordering the Black Sea",
        "Germany": "Central European country.",
        "Ghana": "West African nation on the Gulf of Guinea.",
        "Gibraltar": "British Overseas Territory on the Iberian Peninsula",
        "Greece": "Mediterranean country, home to some of the oldest ruins in the world",
        "Greenland": "The world’s largest island.",
        "Grenada": "Island nation in the Caribbean.",
        "Guadeloupe": "Island group in the Caribbean, the largest island resembles a butterfly.",
        "Guam": "Island in the Western Pacific, an unincorporated territory of the United States",
        "Guatemala": "Central American nation on the Caribbean coast",
        "Guernsey": "Island in the English Channel, part of the Channel Islands",
        "Guinea": "West African nation on the Atlantic Ocean",
        "Guinea-Bissau": "West African nation on the Atlantic Ocean, formerly a colony of Portugal",
        "Guyana": "South American nation on the Northern coast of South America, formerly a British colony",
        "Haiti": "Caribbean nation, sharing an island with the Dominican Republic",
        "Heard Island and McDonald Islands": "Island group in the Southern Ocean owned by Australia",
        "The Holy See": "A small State within a State.",
        "Honduras": "Central American nation between Guatemala and Nicaragua",
        "Hong Kong": "Small island off the coast of China.",
        "Hungary": "Central European nation on the Danube River",
        "Iceland": "Northern European island nation, known for its stunning scenery",
        "India": "Large, South Asian nation",
        "Indonesia": "Southeast Asian island nation",
        "Iran": "Middle Eastern country known for its vibrant Persian culture",
        "Iraq": "Middle Eastern nation, home of the ancient city of Babylon",
        "Ireland": "Island nation off the western coast of Europe.",
        "Isle of Man": "Island in the Irish Sea, autonomous British Crown Dependency",
        "Israel": "Middle Eastern nation located on the eastern shore of the Mediterranean Sea",
        "Italy": "Southern European country, home to many famous works of art and architecture",
        "Jamaica": "Island nation in the Caribbean with a famous sporting heritage.",
        "Japan": "East Asian island nation",
        "Jersey": "Island in the English Channel, part of the Channel Islands",
        "Jordan": "Middle Eastern nation.",
        "Kazakhstan": "Central Asian nation, the world’s largest landlocked country",
        "Kenya": "East African nation on the Indian Ocean",
        "Kiribati": "Island nation in Micronesia, composed of numerous islands",
        "North Korea": "East Asian nation of two halves",
        "The Republic of Korea": "East Asian nation of two halves",
        "Kuwait": "Middle Eastern nation on the Persian Gulf",
        "Kyrgyzstan": "Central Asian nation, home to an ancient city on the Silk Road",
        "Lao People's Democratic Republic": "Southeast Asian nation, known as the Land of a Million Elephants",
        "Latvia": "Baltic nation, bordered by Estonia, Lithuania, and Russia",
        "Lebanon": "Middle Eastern nation on the Mediterranean",
        "Lesotho": "Country in Southern Africa, entirely surrounded by South Africa",
        "Liberia": "West African nation on the Atlantic coast, founded by freed American slaves",
        "Libya": "North African nation on the Mediterranean Sea.",
        "Liechtenstein": "Alpine microstate in Europe",
        "Lithuania": "Baltic nation in Northern Europe",
        "Luxembourg": "Grand Duchy in Western Europe",
        "Macao": "Special Administrative Region in China",
        "Madagascar": "Island nation off the coast of Africa",
        "Malawi": "Landlocked country in Africa",
        "Malaysia": "Southeast Asian country",
        "Maldives": "String of atolls in the Indian Ocean",
        "Mali": "West African nation",
        "Malta": "Island nation in the Mediterranean Sea",
        "Marshall Islands": "Micronesian nation in the Pacific Ocean",
        "Martinique": "Overseas department of France",
        "Mauritania": "Northwest African nation",
        "Mauritius": "Island nation east of Madagascar",
        "Mayotte": "Overseas region of France in the Indian Ocean",
        "Mexico": "North American country",
        "Micronesia": "Federated States in the Pacific Ocean",
        "Moldova": "East European nation",
        "Monaco": "City-state on the French Riviera",
        "Mongolia": "Landlocked Asian nation",
        "Montenegro": "Balkan nation",
        "Montserrat": "Caribbean island",
        "Morocco": "North African country",
        "Mozambique": "Southeastern African nation",
        "Myanmar": "Southeast Asian nation",
        "Namibia": "Southwest African nation",
        "Nauru": "Small island nation in the Pacific",
        "Nepal": "Landlocked Himalayan nation",
        "The Netherlands": "Low-lying European country",
        "New Caledonia": "French overseas collectivity in the Pacific",
        "New Zealand": "Island nation in the South Pacific",
        "Nicaragua": "Central American country",
        "The Niger": "West African nation",
        "Nigeria": "West African nation",
        "Niue": "Island state in the Pacific Ocean",
        "Norfolk Island": "Island in the South Pacific",
        "Northern Mariana Islands": "Commonwealth of the US",
        "Norway": "Scandinavian nation",
        "Oman": "Sultanate on the Arabian Peninsula",
        "Pakistan": "South Asian nation",
        "Palau": "Pacific Island nation",
        "Palestine": "Small Middle-Eastern country.",
        "Panama": "Central American nation",
        "Papua New Guinea": "Island nation in the South Pacific",
        "Paraguay": "Landlocked South American country",
        "Peru": "South American nation",
        "The Philippines": "Southeastern Asian nation",
        "Pitcairn": "Island territory of the UK",
        "Poland": "Central European nation",
        "Portugal": "West European nation",
        "Puerto Rico": "Caribbean island of the United States",
        "Qatar": "Peninsula nation on the Persian Gulf",
        "Republic of North Macedonia": "Balkan nation",
        "Romania": "East European nation",
        "Russia": "Largest nation in the world by area",
        "Rwanda": "East-Central African nation",
        "Reunion": "Overseas region of France in the Indian Ocean",
        "Saint Barthelemy": "A Northern Caribbean island",
        "Saint Helena Ascension and Tristanda Cunha": "Island group in the South Atlantic Ocean",
        "Saint Kitts and Nevis": "Caribbean twin-island nation",
        "Saint Lucia": "Caribbean island nation",
        "French Saint Martin": "Overseas French Island and outermost region of the EU",
        "Saint Pierre and Miquelon": "Small French archipelago off the coast of Canada.",
        "Saint Vincent and the Grenadines": "Caribbean nation South of Martinique.",
        "Samoa": "Polynesian country in the South Pacific",
        "San Marino": "Small European microstate",
        "Sao Tome and Principe": "Island nation off the coast of Africa",
        "Saudi Arabia": "This is a nation situated on the Arabian Peninsula",
        "Senegal": "This is a West African nation",
        "Serbia": "This is a Balkan nation",
        "Seychelles": "Island nation off the coast of Africa",
        "Sierra Leone": "This is a West African nation, South of Mali",
        "Singapore": "This city-state is located in Southeast Asia",
        "Dutch Sint Maarten": "This Caribbean island is a constituent country of the Kingdom of the Netherlands",
        "Slovakia": "A Central European country between Hungary and Poland",
        "Slovenia": "A small country on the Adriatic Sea.",
        "Solomon Islands": "This South Pacific archipelago is located east of the island of Papua New Guinea",
        "Somalia": "This country located in the Horn of Africa is bordered by the Gulf of Aden and the Indian Ocean",
        "South Africa": "This country is on the African continent",
        "South Georgia and the South Sandwich Islands": "This British Overseas Territory consists of an archipelago in the Southern Atlantic Ocean",
        "South Sudan": "This country located in east-central Africa gained its independence in 2011",
        "Spain": "This country with its capital in Madrid is located on the Iberian Peninsula in Europe",
        "Sri Lanka": "This island nation located in the Indian Ocean enjoys temperatures of 30 degrees celcius all year round.",
        "Sudan": "This country in Northeast Africa is the largest in the African continent",
        "Suriname": "This small South American country is bordered by Guyana, Brazil and French Guiana",
        "Svalbard and Jan Mayen": "This Arctic archipelago is part of Scandinavia and is situated in between mainland Norway and the North Pole",
        "Sweden": "This Scandinavian nation is known for its pop stars",
        "Switzerland": "This country is known for its mountainous terrain",
        "Syrian Arab Republic": "This country is in the Middle East",
        "Taiwan": "This island nation is located in Eastern Asia",
        "Tajikistan": "This landlocked country in Central Asia borders Afghanistan and China",
        "United Republic of Tanzania": "This East African country is home to the Serengeti National Park",
        "Thailand": "This Southeast Asian country is known for its monarchy.",
        "Timor-Leste": "This is a Southeast Asian island nation.",
        "Togo": "A small small country in West Africa between Ghana and Nigeria.",
        "Tokelau": "This remote archipelago of three tropical atolls is located in the South Pacific Ocean",
        "Tonga": "A South Pacific island nation.",
        "Trinidad and Tobago": "Islands located off the coast of Venezuela",
        "Tunisia": "This North African country is located on the Mediterranean Sea and is home to the ancient city of Carthage",
        "Turkey": "This country is located at the crossroads of Europe and Asia",
        "Turkmenistan": "This Central Asian country is known for its hot, desert climate.",
        "Turks and Caicos Islands": "Islands located South East of Miami.",
        "Tuvalu": "This small island nation is located near the equator in the Pacific Ocean",
        "Uganda": "This East African country includes part of Lake Victoria",
        "Ukraine": "This Eastern European country is bordered by seven other countries",
        "The United Arab Emirates": "Located on the Arabian Peninsula in the Persian Gulf",
        "United Kingdom": "This nation comprises of four countries",
        "United States Minor Outlying Islands": "This archipelago is composed of small islands and atolls",
        "United States of America": "This country is made up of 50 states.",
        "Uruguay": "This South American country is located on the Atlantic Ocean",
        "Uzbekistan": "This landlocked country is located in Central Asia and was once a part of the Soviet Union",
        "Vanuatu": "This small island nation is situated in the South Pacific Ocean, east of Australia",
        "Venezuela": "This South American country is located on the northern coast of the continent",
        "Vietnam": "This Southeast Asian country is bordered by Laos, Cambodia, and the South China Sea",
        "British Virgin Islands": "These Caribbean Islands are a popular tourist destination",
        "US Virgin Islands": "This territory is composed of a few large islands and several smaller ones",
        "Wallis and Futuna": "Islands located in the South Pacific Ocean, east of Fiji",
        "Western Sahara": "This territory is located in North Africa and is bordered by Morocco, Mauritania and Algeria",
        "Yemen": "This country located in the Arabian Peninsula is known for its deserts and Red Sea beaches",
        "Zambia": "This landlocked country in southern Africa boasts the Victoria Falls on its border",
        "Zimbabwe": "This country in southern Africa is bordered by South Africa, Botswana, Zambia and Mozambique",
        "Aland Islands": "This archipelago is located at the entrance to the Gulf of Bothnia in the Baltic Sea."
    }
# For case insensitivity
__clues = dict((key.casefold(), val) for key, val in clues.items())