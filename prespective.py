from googleapiclient import discovery
import json
from nltk import sent_tokenize

API_KEY = 'AIzaSyD_FybbgQ7QPuQzUOt6vYunV-kwFsdu1MU'

scores = {}
insult = ""
toxicity = ""
profanity = ""
sexually = ""
identity = ""
flirt = ""
threat = ""
severetoxicity = ""
category = ""
INSULT = []
TOXICITY = []
PROFANITY = []
SEXUALLY = []
IDENTITY = []
FLIRT = []
THREAT = []
SEVERETOXICITY = []
sents = ""
insultsents = ""
threatsents = ""
flirtsents = ""
toxicsents = ""
profsents = ""
sexsents = ""
identsents = ""
insultperc = 0
threatperc = 0
flirtperc = 0
toxicperc = 0
profperc = 0
sexperc = 0
identperc = 0
severetoxicityperc = 0
tot = 0,
status = ""
text = 'GURUGRAM: While everyone was rooting for Roger Federer in the breathtaking classic of a Wimbledon final, Diksha Dagar was pumping her fist for Novak Djokovic. "I love his attitude. There are times when he gets so angry when he is playing badly, hes all about I want to win this tournament."The 18-year-old was speaking for herself too, as she begins the Hero Womens Indian Open on Thursday'
sentences = sent_tokenize(text)
for sentence in sentences:
    # Generates API client object dynamically based on service name and version.
    service = discovery.build('commentanalyzer',
                              'v1alpha1',
                              developerKey=API_KEY)

    analyze_request = {
        'comment': {
            'text': sentence
        },
        'requestedAttributes': {
            'TOXICITY': {},
            'INSULT': {},
            'THREAT': {},
            'PROFANITY': {},
            'FLIRTATION': {},
            'IDENTITY_ATTACK': {},
            'SEXUALLY_EXPLICIT': {},
            'SEVERE_TOXICITY' : {},
        }
    }

    response = service.comments().analyze(body=analyze_request).execute()
    for i in response.values():
        for j, k in i.items():
            for l in k.values():
                for m in l:
                    for n, o in m.items():
                        if n == 'score':
                            for x in o.values():
                                scores[j] = x
                                break
                    break
                break
        break
    for i, j in scores.items():
        if i == 'INSULT':
            insult = j
        if i == 'TOXICITY':
            toxicity = j
        if i == 'PROFANITY':
            profanity = j
        if i == 'SEXUALLY_EXPLICIT':
            sexually = j
        if i == 'IDENTITY_ATTACK':
            identity = j
        if i == 'FLIRTATION':
            flirt = j
        if i == 'THREAT':
            threat = j
        if i == 'SEVERE_TOXICITY':
            severetoxicity = j

    category = max(insult, toxicity, profanity, sexually, identity, flirt,
                   threat, severetoxicity)

    if category == insult:
        insultperc += 1
        category = 'insult'
        INSULT.append(insult)
    elif category == toxicity:
        toxicperc += 1
        category = 'toxicity'
        TOXICITY.append(toxicity)
    elif category == profanity:
        profperc += 1
        category = 'profanity'
        PROFANITY.append(profanity)
    elif category == sexually:
        sexperc += 1
        category = 'sexuality_explict'
        SEXUALLY.append(sexually)
    elif category == identity:
        identperc += 1
        category = 'identity_attack'
        IDENTITY.append(identity)
    elif category == flirt:
        flirtperc += 1
        category = 'flirtation'
        FLIRT.append(flirt)
    elif category == threat:
        threatperc += 1
        category = 'threat'
        THREAT.append(threat)
    elif category == severetoxicity:
        severetoxicityperc += 1
        category = 'severe_toxicity'
        SEVERETOXICITY.append(threat)

    if category == 'insult':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        insultsents = insultsents + "<span class=" + category + ">" + sentence + "</span>"
        print("insult: ",insultsents)
    elif category == 'toxicity':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        toxicsents = toxicsents + "<span class=" + category + ">" + sentence + "</span>"
        print("toxicity: ",toxicsents)
    elif category == 'profanity':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        profsents = profsents + "<span class=" + category + ">" + sentence + "</span>"
        print("profanity: ",profsents)
    elif category == 'sexuality_explict':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        sexsents = sexsents + "<span class=" + category + ">" + sentence + "</span>"
        print("sexuality explict: ",sexsents)
    elif category == 'identity_attack':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        identsents = identsents + "<span class=" + category + ">" + sentence + "</span>"
        print("identity attack: ",identsents)
    elif category == 'flirtation':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        flirtsents = flirtsents + "<span class=" + category + ">" + sentence + "</span>"
        print("flirtation: ",flirtsents)
    elif category == 'threat':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        threatsents = threatsents + "<span class=" + category + ">" + sentence + "</span>"
        print("threat: ",threatsents)
    elif category == 'severe_toxicity':
        sents = sents + "<span class=" + category + ">" + sentence + "</span>"
        print("threat: ",threatsents)

tot = len(sentences)
insultperc = round(((insultperc/tot)*100),2)
threatperc = round(((threatperc/tot)*100),2)
flirtperc = round(((flirtperc/tot)*100),2)
toxicperc = round(((toxicperc/tot)*100),2)
profperc = round(((profperc/tot)*100),2)
sexperc = round(((sexperc/tot)*100),2)
identperc = round(((identperc/tot)*100),2)
severetoxicityperc = round(((severetoxicityperc/tot)*100),2)

if insultperc >= threatperc and insultperc >= flirtperc and insultperc >= toxicperc and insultperc >= profperc and insultperc >= sexperc and insultperc >= identperc:
    status = "insult"
elif threatperc >= insultperc and threatperc >= flirtperc and threatperc >= toxicperc and threatperc >= profperc and threatperc >= sexperc and threatperc >= identperc:
    status = "threat"
elif flirtperc >= insultperc and flirtperc >= threatperc and flirtperc >= toxicperc and flirtperc >= profperc and flirtperc >= sexperc and flirtperc >= identperc:
    status = "flirt"
elif toxicperc >= insultperc and toxicperc >= threatperc and toxicperc >= flirtperc and toxicperc >= profperc and toxicperc >= sexperc and toxicperc >= identperc:
    status = "toxicity"
elif profperc >= insultperc and profperc >= threatperc and profperc >= toxicperc and profperc >= flirtperc and profperc >= sexperc and profperc >= identperc:
    status = "profanity"
elif sexperc >= insultperc and sexperc >= threatperc and sexperc >= toxicperc and sexperc >= profperc and sexperc >= flirtperc and sexperc >= identperc:
    status = "sexual"
elif identperc >= insultperc and sexperc >= threatperc and sexperc >= toxicperc and sexperc >= profperc and sexperc >= flirtperc and sexperc >= identperc:
    status = "identity"
else:
    status = "severe toxicity"

print("insult: ",insultperc)
print("threat",threatperc)
print("flirtation",flirtperc)
print("toxicity: ",toxicperc)
print("profanity: ",profperc)
print("sexuality explict",sexperc)
print("identity attack",identperc)
print("severe toxicity",severetoxicityperc)
print("status: ",status)
