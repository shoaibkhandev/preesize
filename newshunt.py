from __future__ import absolute_import
from flask import Flask, request, render_template, jsonify, Response
from flask_cors import CORS
from googleapiclient import discovery
from newspaper import Article
from summa import summarizer
from nltk import sent_tokenize
import operator
import json
import pymysql.cursors
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
import time

app = Flask(__name__)
CORS(app)


@app.route('/')
def my_form():
    return render_template('/index.html')


@app.route('/summary')
def my_form1():
    return render_template('/summary.html')


@app.route('/sentiment')
def my_form2():
    return render_template('/sentiment.html')


@app.route('/deep_analyze')
def my_form3():
    return render_template('/deep_analyze.html')


@app.route('/cron_job')
def cron_job():

    connection = pymysql.connect(host='localhost',
                                 user='newshunt',
                                 password='MEgBT5ebeYqOAvscRF8S',
                                 db='newshunt_newsHunt',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        sql = "SELECT id,url FROM `news` where id > 207564  and description like '%a%' and summary IS NULL"
        cursor.execute(sql)
        text = cursor.fetchall()
        for dict in text:

            id = str(dict['id'])
            article = Article(dict['url'])
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            summ = article.summary
            summ = summ.replace('"', '')
            summ = summ.replace("'", '')
            sql = "UPDATE news SET summary = '''" + summ + "'''  WHERE id= " + id
            cursor.execute(sql)
            connection.commit()

    except:
        pass
    finally:
        connection.close()

    return "Done"

@app.route('/newshunt_summary', methods=['GET'])
def newshunt_summary():
    summ = ""
    text = request.args.get('text')
    summ = summarizer.summarize(text, ratio=0.4)

    return summ

@app.route('/newshunt_senti', methods=['GET'])
def newshunt_sentiment():
    sents = ""
    possents = ""
    negsents = ""
    neusents = ""
    pos = ""
    neg = ""
    neu = ""
    vspos = 0
    vsneg = 0
    vsneu = 0
    tot = 0
    status = ""
    text = request.args.get('text')
    sentences = sent_tokenize(text)
    analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        if vs['compound'] >= 0.05:
            vspos = vspos + 1
            sents = sents + "<span class=\"positive_class\">" + sentence + "</span>"
            possents = possents + "<span class=\"positive_class\">" + sentence + "</span>"
        elif (vs['compound'] > -0.05 and vs['compound'] < 0.05):
            vsneu = vsneu + 1
            sents = sents + "<span class=\"neutral_class\">" + sentence + "</span>"
            neusents = neusents + "<span class=\"neutral_class\">" + sentence + "</span>"
        elif vs['compound'] <= -0.05:
            vsneg = vsneg + 1
            sents = sents + "<span class=\"negative_class\">" + sentence + "</span>"
            negsents = negsents + "<span class=\"negative_class\">" + sentence + "</span>"
    tot = len(sentences)
    pos = round((vspos / tot) * 100, 1)
    neg = round((vsneg / tot) * 100, 1)
    neu = round((vsneu / tot) * 100, 1)

    if pos > neg and pos > neu:
        status = "positive"
    elif neg > pos and neg > neu:
        status = "negative"
    else:
        status = "neutral"

    return jsonify(sentences=sents,possentences=possents,negsentences=negsents,neusentences=neusents,Pos=pos,Neg=neg,Neu=neu,status=status)
    
@app.route('/newshunt_deep', methods=['GET'])
def newshunt_deepAnalyze():
    scores = {}
    scores2 = {}
    sents = ""
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
    tot = 0
    status = ""
    API_KEY = 'AIzaSyD_FybbgQ7QPuQzUOt6vYunV-kwFsdu1MU'
    service = discovery.build('commentanalyzer',
                              'v1alpha1',
                              cache_discovery=False,
                              developerKey=API_KEY)

    text = request.args.get('text')
    sentences = sent_tokenize(text)
    for sentence in sentences:
        time.sleep(1)
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
                'SEVERE_TOXICITY': {},
            }
        }
        response = service.comments().analyze(
            body=analyze_request).execute()
        for i in response.values():
            for j, k in i.items():
                for l in k.values():
                    for m in l:
                        for n, o in m.items():
                            if n == 'score':
                                for x in o.values():
                                    scores2[j] = x
                                    break
                        break
                    break
            break

        for i, j in scores2.items():
            if i == 'INSULT':
                insult = str(round(j * 100, 2))
            if i == 'TOXICITY':
                toxicity = str(round(j * 100, 2))
            if i == 'PROFANITY':
                profanity = str(round(j * 100, 2))
            if i == 'SEXUALLY_EXPLICIT':
                sexually = str(round(j * 100, 2))
            if i == 'IDENTITY_ATTACK':
                identity = str(round(j * 100, 2))
            if i == 'FLIRTATION':
                flirt = str(round(j * 100, 2))
            if i == 'THREAT':
                threat = str(round(j * 100, 2))
            if i == 'SEVERE_TOXICITY':
                severetoxicity = str(round(j * 100, 2))

        category = max(insult, toxicity, profanity, sexually, identity,
                        flirt, threat, severetoxicity)
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
            SEVERETOXICITY.append(severetoxicity)

        if category == 'insult':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            insultsents = insultsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'toxicity':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            toxicsents = toxicsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'profanity':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            profsents = profsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'sexuality_explict':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            sexsents = sexsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'identity_attack':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            identsents = identsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'flirtation':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            flirtsents = flirtsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'threat':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"
            threatsents = threatsents + "<span class=" + category + ">" + sentence + "</span>"
        elif category == 'severe_toxicity':
            sents = sents + "<span class=" + category + ">" + sentence + "</span>"

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

    return jsonify(sentences=sents,
                   inputtext=text,
                   insult=insultperc,
                   toxicity=toxicperc,
                   profanity=profperc,
                   sexual=sexperc,
                   identity=identperc,
                   flirt=flirtperc,
                   threat=threatperc,
                   severe=severetoxicityperc,
                   status=status
                   )
    

@app.route('/summary_from_url', methods=['POST'])
def my_form_post():
    summ = ""
    text = ""
    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        url = data.get('url')
        method = data.get('method')
        if method == 1:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            summ = article.summary
            text = article.text

        elif method == 2:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            summ = summarizer.summarize(str(text))

    return jsonify(summary=summ, inputtext=text)


@app.route('/summary_from_file', methods=['POST'])
def my_form_post1():
    summ = ""
    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        text = data.get('fileText')
        method = data.get('method')
        if method == 1:
            summ = summarizer.summarize(text)
        elif method == 2:
            summ = summarizer.summarize(text, ratio=0.4)

    return Response(summ)


@app.route('/sentiment_from_url', methods=['POST'])
def my_form_post2():
    sents = ""
    possents = ""
    negsents = ""
    neusents = ""
    pos = ""
    neg = ""
    neu = ""
    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        url = data.get('url')
        method = data.get('method')

        if method == 1:
            vspos = 0
            vsneg = 0
            vsneu = 0
            tot = 0
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            sentences = sent_tokenize(text)
            analyzer = SentimentIntensityAnalyzer()
            for sentence in sentences:
                vs = analyzer.polarity_scores(sentence)
                if vs['compound'] >= 0.05:
                    vspos = vspos + 1
                    sents = sents + "<span class=\"positive_class\">" + sentence + "</span>"
                    possents = possents + "<span class=\"positive_class\">" + sentence + "</span>"
                elif (vs['compound'] > -0.05 and vs['compound'] < 0.05):
                    vsneu = vsneu + 1
                    sents = sents + "<span class=\"neutral_class\">" + sentence + "</span>"
                    neusents = neusents + "<span class=\"neutral_class\">" + sentence + "</span>"
                elif vs['compound'] <= -0.05:
                    vsneg = vsneg + 1
                    sents = sents + "<span class=\"negative_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"negative_class\">" + sentence + "</span>"
            tot = len(sentences)
            pos = round((vspos / tot) * 100, 1)
            neg = round((vsneg / tot) * 100, 1)
            neu = round((vsneu / tot) * 100, 1)

        elif method == 2:
            tbpos = 0
            tbneg = 0
            tbneu = 0
            tot = 0
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            sentences = sent_tokenize(text)
            for sentence in sentences:
                tb = TextBlob(sentence).sentiment

                if tb.polarity > 0:
                    tbpos = tbpos + 1
                    sents = sents + "<span class=\"positive_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"positive_class\">" + sentence + "</span>"
                elif tb.polarity == 0:
                    tbneu = tbneu + 1
                    sents = sents + "<span class=\"neutral_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"neutral_class\">" + sentence + "</span>"
                elif tb.polarity < 0:
                    tbneg = tbneg + 1
                    sents = sents + "<span class=\"negative_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"negative_class\">" + sentence + "</span>"

            tot = len(sentences)
            pos = round((tbpos / tot) * 100, 1)
            neg = round((tbneg / tot) * 100, 1)
            neu = round((tbneu / tot) * 100, 1)

    return jsonify(sentences=sents,
                   possentences=possents,
                   negsentences=negsents,
                   neusentences=neusents,
                   Pos=pos,
                   Neg=neg,
                   Neu=neu,
                   inputtext=text)


@app.route('/sentiment_from_file', methods=['POST'])
def my_form_post3():
    sents = ""
    possents = ""
    negsents = ""
    neusents = ""
    pos = ""
    neg = ""
    neu = ""
    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        text = data.get('fileText')
        method = data.get('method')

        if method == 1:
            vspos = 0
            vsneg = 0
            vsneu = 0
            tot = 0
            sentences = sent_tokenize(text)
            analyzer = SentimentIntensityAnalyzer()
            for sentence in sentences:
                vs = analyzer.polarity_scores(sentence)
                if vs['compound'] >= 0.05:
                    vspos = vspos + 1
                    sents = sents + "<span class=\"positive_class\">" + sentence + "</span>"
                    possents = possents + "<span class=\"positive_class\">" + sentence + "</span>"
                elif (vs['compound'] > -0.05 and vs['compound'] < 0.05):
                    vsneu = vsneu + 1
                    sents = sents + "<span class=\"neutral_class\">" + sentence + "</span>"
                    neusents = neusents + "<span class=\"neutral_class\">" + sentence + "</span>"
                elif vs['compound'] <= -0.05:
                    vsneg = vsneg + 1
                    sents = sents + "<span class=\"negative_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"negative_class\">" + sentence + "</span>"
            tot = len(sentences)
            pos = round((vspos / tot) * 100, 1)
            neg = round((vsneg / tot) * 100, 1)
            neu = round((vsneu / tot) * 100, 1)

        elif method == 2:
            tbpos = 0
            tbneg = 0
            tbneu = 0
            tot = 0
            sentences = sent_tokenize(text)
            for sentence in sentences:
                tb = TextBlob(sentence).sentiment

                if tb.polarity > 0:
                    tbpos = tbpos + 1
                    sents = sents + "<span class=\"positive_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"positive_class\">" + sentence + "</span>"
                elif tb.polarity == 0:
                    tbneu = tbneu + 1
                    sents = sents + "<span class=\"neutral_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"neutral_class\">" + sentence + "</span>"
                elif tb.polarity < 0:
                    tbneg = tbneg + 1
                    sents = sents + "<span class=\"negative_class\">" + sentence + "</span>"
                    negsents = negsents + "<span class=\"negative_class\">" + sentence + "</span>"

            tot = len(sentences)
            pos = round((tbpos / tot) * 100, 1)
            neg = round((tbneg / tot) * 100, 1)
            neu = round((tbneu / tot) * 100, 1)

    return jsonify(sentences=sents,
                   possentences=possents,
                   negsentences=negsents,
                   neusentences=neusents,
                   Pos=pos,
                   Neg=neg,
                   Neu=neu)


@app.route('/perspective_from_url', methods=['POST'])
def my_form_post4():
    scores = {}
    scores2 = {}
    sents = ""
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
    tot = 0
    API_KEY = 'AIzaSyD_FybbgQ7QPuQzUOt6vYunV-kwFsdu1MU'
    service = discovery.build('commentanalyzer',
                              'v1alpha1',
                              cache_discovery=False,
                              developerKey=API_KEY)

    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        url = data.get('url')
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        sentences = sent_tokenize(text)
        for sentence in sentences:
            time.sleep(1)
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
                    'SEVERE_TOXICITY': {},
                }
            }
            response = service.comments().analyze(
                body=analyze_request).execute()
            for i in response.values():
                for j, k in i.items():
                    for l in k.values():
                        for m in l:
                            for n, o in m.items():
                                if n == 'score':
                                    for x in o.values():
                                        scores2[j] = x
                                        break
                            break
                        break
                break

            for i, j in scores2.items():
                if i == 'INSULT':
                    insult = str(round(j * 100, 2))
                if i == 'TOXICITY':
                    toxicity = str(round(j * 100, 2))
                if i == 'PROFANITY':
                    profanity = str(round(j * 100, 2))
                if i == 'SEXUALLY_EXPLICIT':
                    sexually = str(round(j * 100, 2))
                if i == 'IDENTITY_ATTACK':
                    identity = str(round(j * 100, 2))
                if i == 'FLIRTATION':
                    flirt = str(round(j * 100, 2))
                if i == 'THREAT':
                    threat = str(round(j * 100, 2))
                if i == 'SEVERE_TOXICITY':
                    severetoxicity = str(round(j * 100, 2))

            category = max(insult, toxicity, profanity, sexually, identity,
                           flirt, threat, severetoxicity)
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
                SEVERETOXICITY.append(severetoxicity)

            if category == 'insult':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                insultsents = insultsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'toxicity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                toxicsents = toxicsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'profanity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                profsents = profsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'sexuality_explict':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                sexsents = sexsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'identity_attack':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                identsents = identsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'flirtation':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                flirtsents = flirtsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'threat':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                threatsents = threatsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'severe_toxicity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"

    tot = len(sentences)
    insultperc = round(((insultperc/tot)*100),2)
    threatperc = round(((threatperc/tot)*100),2)
    flirtperc = round(((flirtperc/tot)*100),2)
    toxicperc = round(((toxicperc/tot)*100),2)
    profperc = round(((profperc/tot)*100),2)
    sexperc = round(((sexperc/tot)*100),2)
    identperc = round(((identperc/tot)*100),2)
    severetoxicityperc = round(((severetoxicityperc/tot)*100),2)

    return jsonify(sentences=sents,
                   inputtext=text,
                   insultsents=insultsents,
                   toxicsents=toxicsents,
                   profsents=profsents,
                   sexsents=sexsents,
                   identsents=identsents,
                   flirtssents=flirtsents,
                   threatsents=threatsents,
                   insult=insultperc,
                   toxicity=toxicperc,
                   profanity=profperc,
                   sexual=sexperc,
                   identity=identperc,
                   flirt=flirtperc,
                   threat=threatperc,
                   severe=severetoxicityperc
                   )


@app.route('/perspective_from_file', methods=['POST'])
def my_form_post5():
    scores = {}
    scores2 = {}
    sents = ""
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
    tot = 0
    API_KEY = 'AIzaSyD_FybbgQ7QPuQzUOt6vYunV-kwFsdu1MU'
    service = discovery.build('commentanalyzer',
                              'v1alpha1',
                              cache_discovery=False,
                              developerKey=API_KEY)

    if len(request.get_json(silent=True)) > 0:
        data = request.get_json(silent=True)
        text = data.get('fileText')
        sentences = sent_tokenize(text)
        logging.info(len(sentences))
        for sentence in sentences:
            time.sleep(1)
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
                    'SEVERE_TOXICITY': {},
                }
            }
            response = service.comments().analyze(
                body=analyze_request).execute()
            for i in response.values():
                for j, k in i.items():
                    for l in k.values():
                        for m in l:
                            for n, o in m.items():
                                if n == 'score':
                                    for x in o.values():
                                        scores2[j] = x
                                        break
                            break
                        break
                break

            for i, j in scores2.items():
                if i == 'INSULT':
                    insult = str(round(j * 100, 2))
                if i == 'TOXICITY':
                    toxicity = str(round(j * 100, 2))
                if i == 'PROFANITY':
                    profanity = str(round(j * 100, 2))
                if i == 'SEXUALLY_EXPLICIT':
                    sexually = str(round(j * 100, 2))
                if i == 'IDENTITY_ATTACK':
                    identity = str(round(j * 100, 2))
                if i == 'FLIRTATION':
                    flirt = str(round(j * 100, 2))
                if i == 'THREAT':
                    threat = str(round(j * 100, 2))
                if i == 'SEVERE_TOXICITY':
                    severetoxicity = str(round(j * 100, 2))

            category = max(insult, toxicity, profanity, sexually, identity,
                           flirt, threat, severetoxicity)
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
                SEVERETOXICITY.append(severetoxicity)

            if category == 'insult':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                insultsents = insultsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'toxicity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                toxicsents = toxicsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'profanity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                profsents = profsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'sexuality_explict':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                sexsents = sexsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'identity_attack':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                identsents = identsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'flirtation':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                flirtsents = flirtsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'threat':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"
                threatsents = threatsents + "<span class=" + category + ">" + sentence + "</span>"
            elif category == 'severe_toxicity':
                sents = sents + "<span class=" + category + ">" + sentence + "</span>"

    tot = len(sentences)
    insultperc = round(((insultperc/tot)*100),2)
    threatperc = round(((threatperc/tot)*100),2)
    flirtperc = round(((flirtperc/tot)*100),2)
    toxicperc = round(((toxicperc/tot)*100),2)
    profperc = round(((profperc/tot)*100),2)
    sexperc = round(((sexperc/tot)*100),2)
    identperc = round(((identperc/tot)*100),2)
    severetoxicityperc = round(((severetoxicityperc/tot)*100),2)

    return jsonify(sentences=sents,
                   inputtext=text,
                   insultsents=insultsents,
                   toxicsents=toxicsents,
                   profsents=profsents,
                   sexsents=sexsents,
                   identsents=identsents,
                   flirtssents=flirtsents,
                   threatsents=threatsents,
                   insult=insultperc,
                   toxicity=toxicperc,
                   profanity=profperc,
                   sexual=sexperc,
                   identity=identperc,
                   flirt=flirtperc,
                   threat=threatperc,
                   severe=severetoxicityperc
                   )


if __name__ == '__main__':
    app.run(debug=True)
