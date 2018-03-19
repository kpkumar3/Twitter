
# coding: utf-8

import csv
import html
import re
import string
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lm = WordNetLemmatizer()


import gensim
from gensim import corpora, models

import wordcloud
from wordcloud import WordCloud, STOPWORDS


get_ipython().magic('matplotlib inline')
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import random


#File headers
fieldnames=['Data Source','ID','User_Id','Screen_Name','User_Name','Original Source','Language','Time','Date','Time_Zone','Location','City','State','Country','Share_Count','Favorite_Count','Comment_Count','URL','Description','Headlines','Text','CleanedText','Hashtags']

#Write the headers to o/p file
with open('TwitterCleanedOp.csv','w') as op:
    writer = csv.DictWriter(op,fieldnames=fieldnames,lineterminator='\n')
    writer.writeheader()


# In[8]:

def FileProcess(filename):
    with open(filename,'r') as inp:
        data = csv.DictReader(inp)
        for row in data:
            text=row['Text']
            #print( text)
            
            #unescape any html characters
            text=html.unescape(text)
            
            #Remove any white space characters 
            #####text=' '.join(re.findall("[^ \t\n\r\f\v]+", text)) 
            #####text = ' '.join(re.findall("[\S]+", text))  #this is same as above
            text=re.sub(r'\\n',r'',text)
            text=re.sub(r'\\t',r'',text)
            text=re.sub(r'\\r',r'',text)
            text=re.sub(r'\\f',r'',text)
            text=re.sub(r'\\v',r'',text)
            
            #remove the "RT @username" from tweet
            #print(re.findall('(?:RT @[\w_:]+)' ,text))
            text=re.sub(r'(?:RT @[\w_:]+) ',r'',text)
            
            #remove the URLs from tweets
            #####print(re.findall('(?:RT @[\w_:]+)' ,text))
            text=re.sub('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',r'',text)
            
            #print(re.findall((r'x[0-9a-fA-F ]+'),text,re.I))
            hashtags=' '.join(set([re.sub(r"#+", "#", k) for k in set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in text.split() if i.startswith("#")])])]))            
            #hashtags=''
            #####append the emojis to a separate column before replacing them with spaces.
            text=re.sub(r'(\\x[0-9A-Fa-f]+)',r'', text)
            #print(''.join(tokens_re.findall(text)))
            
            #join all the words again to form a sentence - cleaned text.
            text=' '.join(re.findall("[\w]+", text))[2:]
            
            row['CleanedText'] = text
            row['Hashtags'] = hashtags
            with open('TwitterCleanedOp.csv','a') as op:
                writer = csv.DictWriter(op,fieldnames=fieldnames,lineterminator='\n')
                writer.writerow(row)

            text=text.translate(string.punctuation).lower()
            tokens=gensim.utils.simple_preprocess(text, deacc=True, min_len=3)
            non_stop_tokens = [w for w tokens if w not in stopwords.words('english')]
            docs=[lm.lemmatize(w) for w in non_stop_tokens]
            yield docs


docs = []
for tweet_text in FileProcess('TwitterCleaned.csv'):
    docs.append(tweet_text)

#print(docs)
#len(docs)

dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(text) for text in docs]


###########################################################################################################################
###########################################################################################################################
#################################                        LDA MODEL                          ###############################
###########################################################################################################################
###########################################################################################################################


##########################################
#Building a model with num_topics = 30   #
##########################################
#ldamodel30 = gensim.models.ldamodel.LdaModel(corpus, num_topics=30, id2word = dictionary, passes = 50)


# In[62]:

#ldatopics30=ldamodel50.show_topics(num_topics=30, num_words=10,formatted=False)


# In[17]:

def CreateModels(corpus,num_topics,dictionary,num_passes):
    return gensim.models.ldamodel.LdaModel(corpus=corpus,num_topics=num_topics,id2word=dictionary,passes=num_passes)


num_topics=30
ldamodel30 = CreateModels(corpus,num_topics,dictionary,num_passes=50)
num_topics=60
ldamodel60 = CreateModels(corpus,num_topics,dictionary,num_passes=50)
num_topics=100
ldamodel100 = CreateModels(corpus,num_topics,dictionary,num_passes=50)
num_topics=150
ldamodel150 = CreateModels(corpus,num_topics,dictionary,num_passes=50)


ldatopics30=ldamodel30.show_topics(num_topics=30, num_words=10,formatted=False)
ldatopics60=ldamodel60.show_topics(num_topics=60, num_words=10,formatted=False)
ldatopics100=ldamodel100.show_topics(num_topics=100, num_words=10,formatted=False)
ldatopics150=ldamodel150.show_topics(num_topics=150, num_words=10,formatted=False)


################### Extracts topics from the topics in LDA topics from each model #############
#*****************Note: This is commonly used function to extract wordcloud text for topics for all models *************
def wordcloud_text(topics):
    wc_text=[]
    for i in range(len(topics)):
        wc_text.append(' '.join(topics[i][1]))
    return ' '.join(wc_text)


topics30 = [(tp[0], [wd[0] for wd in tp[1]]) for tp in ldatopics30]
wctext30=wordcloud_text(topics30)
topics60 = [(tp[0], [wd[0] for wd in tp[1]]) for tp in ldatopics60]
wctext60=wordcloud_text(topics60)
topics100 = [(tp[0], [wd[0] for wd in tp[1]]) for tp in ldatopics100]
wctext100=wordcloud_text(topics100)
topics150 = [(tp[0], [wd[0] for wd in tp[1]]) for tp in ldatopics150]
wctext150=wordcloud_text(topics150)


stopwords = set(STOPWORDS)
for text in [wctext30,wctext60,wctext100,wctext150]:
    wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(text)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()    


import pyLDAvis.gensim
pyLDAvis.enable_notebook()
pyLDAvis.gensim.prepare(ldamodel30, corpus, dictionary)


data=pyLDAvis.gensim.prepare(ldamodel30, corpus, dictionary)
data
pyLDAvis.save_html(data, 'lda_30topics.html')

#data=pyLDAvis.gensim.prepare(ldamodel60, corpus, dictionary)
#p = pyLDAvis.gensim.prepare(topic_model, corpus, dictionary)
##pyLDAvis.save_html(data, 'lda_60topics.html')
#
#data=pyLDAvis.gensim.prepare(ldamodel100, corpus, dictionary)
#p = pyLDAvis.gensim.prepare(topic_model, corpus, dictionary)
#pyLDAvis.save_html(data, 'lda_100.html')
#
#data=pyLDAvis.gensim.prepare(ldamodel150, corpus, dictionary)
#p = pyLDAvis.gensim.prepare(topic_model, corpus, dictionary)
#pyLDAvis.save_html(data, 'lda_150.html')


# In[39]:

data=pyLDAvis.gensim.prepare(ldamodel60, corpus, dictionary)
data


# In[40]:

data=pyLDAvis.gensim.prepare(ldamodel100, corpus, dictionary)
data


# In[41]:

data=pyLDAvis.gensim.prepare(ldamodel150, corpus, dictionary)
data



################## BUild a word cloud - 100 topics and 10 words in each topic ###########################
stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(wctext30)
                        #(#font_path='/Library/Fonts/Verdana.ttf',
                      #relative_scaling = 1.0,
                      #stopwords = stopwords # set or space-separated string
                      #).generate(text)
#wordcloud=WordCloud(width = 1000, height = 500,relative_scaling = 1.0).generate(text)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[ ]:

##########################################
#Building a model with num_topics = 300  #
##########################################
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=300, id2word = dictionary, passes = 20)


# In[23]:

#ldamodel


# In[34]:

########### BUild the model and assign topics to x.################
#print(ldamodel.print_topics(num_topics=50, num_words=5))
x=ldamodel.show_topics(num_topics=300, num_words=10,formatted=False)
topics = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]
#print(topics)


# In[83]:

################### Extracts topics from the topics in x #############
def wordcount_text(topics):
    wc_text=[]
    for i in range(len(topics)):
        wc_text.append(' '.join(topics[i][1]))
    return ' '.join(wc_text)

text=wordcount_text(topics)
#print(text)


# In[84]:

################## BUild a word cloud - 300 topics and 10 words in each topic ###########################
stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(text)
                        #(#font_path='/Library/Fonts/Verdana.ttf',
                      #relative_scaling = 1.0,
                      #stopwords = stopwords # set or space-separated string
                      #).generate(text)
#wordcloud=WordCloud(width = 1000, height = 500,relative_scaling = 1.0).generate(text)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[58]:

############################ Ran the LDA model with number of topics as 200 and words as 10 #####################
## to avoid rerunnng the model again, the final corpus of topics is assigned to text_200 
text_200 = '2017 boston atlanta bravesfam bravescountry elite 1996 sometimes foco nosso 10 6 american around african project best charlotte aye washington ill seeing tem missing fantastic healthcare grab awareness tired raise rain plan atlanta hand parece feelin vi character homie ion atlanta pop network grind cry register entertainment realized fitness contact atlanta em flight uma model conservative republican wtf allowed btw pretty writing bringing san showed sing atlanta towards antonio cowboy better atlanta houston hood looked rat never tuesday ceo cobb happy money act clean problem hoping tus watershed_ltd denisebrasse askwhatnext top honored waymo session pra dad telling republicday festivity str everything atlanta drive culture eat prepared filled alpine foles helen commercial atlanta waiting past wa olympics bombed clinic also lesbian excited medium atlanta kenya data 58 email info track website ucf delta wasnt returning anywhere peter corruption aire chatted filmmaker go atlanta open summer late interested filming michael fly offseason podcast annual 21 church follower history known finish celebrate hacen check service major mountain truck driver theyre customer cdl llc atlanta wait see cant good dont hear texas chance 55 yll sure atlanta outside talent havent hello though squad worst event set long hour atlanta alone scholarship complete selling 80 great atlanta metro station heard timberwolves smart professional atlantic within talk sport creating vision morehouse keller albuquerque new one may one last atlanta night two best day thank ever ive hate announces fine offer interview affordable pre leaving atlanta lied house kickoff cola coca organization philadelphia rise drink joining launch atlanta ever seen ive thing international bro cbs46 jackson airport want would start atlanta bring early wonder newest urban wing brave atlanta fun wan mascot system chief vibe board wahoo feb dallas atlanta newyork chicago 2018 19th 25th 24k usa next atlanta february migos change experience 6th close attend workshop community atlanta promo ft showing mark af discus four discount el de en con del al la inti titular cinturn scene shooting ol update 14th angelo demonio science proposal valid sale birthday forget dont atlanta celebration gm intern internship talib anyone ver writer wow recommend ranking brain aquarium size thru driving name crazy shoot photography atlanta account blow network wireless much lot feel atlanta eagle seattle building individual light nfc founder tim cnn prove nhl cad selfie gang mac swing bravo de ronald acu head atlanta upcoming deportes mlb bisbol georgia atlanta u location join public hundred teacher pull boi atlanta body country put police straight idea officer named wag 2018 take look atlanta soon tyler dropping 01 taste collection airport atlanta aim new billion world 11 busiest istanbul nashville usa atlanta hay hearing court meetup ahora closed gracias tape miss hop hip west 500 release atlanta author coast mixtape pick atlanta bad trying awesome claim bitch word draft contract night effort atlan match extra address atlanta arrested checking michigan keep atlanta turn queen pablo fit un mir barrabrava luchando ga atlanta job hiring manager assistant jobs4u service mall bistro mlk atlanta asking marketing orgy nasty night face party game two looking bar wanted away atlanta who sweet nick charge atlanta tv stage hotel savannah whats 50 wsb gig zoo live atlanta university clark style jersey pay priority due moore got atlanta picture ta si livehiphopdaily 24hrhiphopchannel photooftheday wit ask yes f research product wrong designer entire race platform atlanta said boy give lil singing atlanta round land mood specialist ready atlanta child blog grammys2018 deep mock thrive maga nearly based literally desde joe judge atlanta fish saludos attorney tank video atlanta youtube 11 liked season 10 episode housewife real 2 atlanta como tbt 1loveash pelo srio ator celtic 110 v atlanta used north nba minnesota sw fucking hawk success liberal carmona grateful atlanta colo carlos firm stoked united wanting atlanta as return lmao cause stay coach cap lying racist n fuck co atlanta reality wife fox important employee fuckin player war probably signed chopon hr alert atlanta rare auto immigration robot vinings tcot sandysprings atlantasciencefestival atlanta rednationrising pjnet notabot taking former door bitcoin option ajc pain atlanta kudos dodger energy combat beer force protect craft prayer exploring aspiring creo still pro safe living lo yeah atlanta interesting getaway australia atlanta workout buddy muscle hunk gym flexing conference gay playlist woman book fashion mini van dress worldwide 1999 spacious womensfashion work college labor post student job california moving listen sanfrancisco actor world winning female seeking strong field chill movement dance never could r mile pieza clave volante contencin hace diva agree yet bus doesnt medical wed shawnabner theory victoria viene lion including lead maybe atlanta brother chop retweeted tomahawk rid performance center travel restaurant technology poor lost master definitely architecture need already may career soul buck heading continue exposure reframed rhoa latest gone do killing 3rd esta mold retweet reminded tell run middle este ar main 53 atlanta sub to2 since casting begin construction 31 atlanta thescc intro lyric badgalashbree time black 100 available performing movie atlanta online purchase panther ser para con que e los le boca la tuvo love atlanta nigga amazing part little doctor town saint short make tomorrow song full instagram feature atlanta championship operator covering hiphop q rap sunday million driver sell atlanta pizza taylor march atlanta kid summit wednesday 14 suck featuring premiere presale life hit property save entrepreneur fast care atlanta incredible mondaymotivation tlanta saturday thursday lose mind production cost sleep bros boring right l number senior atlanta baseball become non 2015 analyst cod eva instead developer sr okay nene codworldleague retail jordan get man atla atlanta cover sooo maddux neilshyminsky chrisj5597 vols week atlanta tour 1st est huge dm dc sun plaza social yellow host leader step page global justice received swanson know he didnt future 9 aint 000 200 pass death friend also atlanta ricardoanayac second solo breaking called inc hijos atlanta fed economy quarter first anything see beautiful expanding percent new atlanta today rt read dream dropped carolina boat skiff la le su al mismo camargo tiempo dan cargo1393 jugador donald glover everyone atlanta cheese genius walking prepare complimentary flyultimateair girl atlanta m naked roster ibz tener barra hincha yep game atlanta cwl road hawk preview wolf twice largest journalist really say watching atlanta remember started agent depot line ashsaidit back atlanta na east heart havana took oh ooh half lol por atlanta te 23 southside taylorswift13 dec impact visitante atlanta tiger memphis headed loose morning muchos porque 103 cameron walk playing united ml atlanta starting rest moon includes package let atlanta wear supply bulk jail muslim inmate hijab linked team fan hope list retweet comment atlanta shared ground june added g gave columbus realize indianapolis atlanta rookie position boost 17 nfl proud per atlantafalcons smooth wouldnt atlanta clip surprised atlanta concert one legend bareback redbootyisback bigdick gaysex view journal home atlanta well meet finally site power using economic strategize via atlanta food youtube meeting htt detroit include fulton connection men nothing football washington done fbi julio gun easy expo 3 atlanta member family group pic side nostalgia biggest nye old 12 piece health bottom sex initiative channel victim slavery bravotv partner official jones league grammyparty laoutfit chipper swaggboutique along 5 4 winner special denver giveaway enjoy prize atlanta degree day atlanta different story raised rep voice utility battle born 30 austin 2nd pm reminder pas 00 org sur hoe dr market estate secret flame wide feed receiver atlanta riding date link office bio booking atlanta southern tom funk paris un use de trump hollywood legal atlanta executive cuando esto like atlanta yo wish person th drop license cleveland thinking im atlanta please ticket album atlanta_police hey tweet support enjoy falcon atlanta stadium paid rock across price riseup solid atlfalcons atlanta national ex lit final va girlfriend raw see card way hard small stand democrat atlanta missouri tribute activist atlsv schedule wont click counseling atlhawks apply atlanta worked curbedatlanta alleyesnorth went atlanta able believe dead 40 benz mercedes photographer reed season 2 grammys gambino childish atlanta year quick remembered outlook talented code lyft weather atlanta homedepot course wind zoot cloud welcome atlanta beat park ya aka county imagine test clayton star art share 0 sus half patriot qb simple atlanta atlanta find monday dude detail traffic must far sound tho month told spent role vo wsbtv eles clear thompson theater que en atlanta de eu mais ele ma otro garden 1 found something downtown tip store shop kennesaw week order year atlanta left p god everybody saying missed value alvaro_delgado weekend gon wwe cool exclusive adopt native htwh learned gift mayor atlanta human keishabottoms trafficking recently blooper speaking creative introduced w thank met atlanta actually nice baby praying confident arkansas young marta hav singer crash sad atlanta understand rich bra king film opening atlanta studio festival isnt southeast associate icymi atlanta 28 third adventure drug li di hoy send rate thing shit atlanta mean band tune tryna changing condition critical thats hot three red mix engineer behind wrote trap superbowl show atlanta photo 8 mi sent heck loud wrfg earlier youre training mad atlanta ja ano television village shirt ahead da e h program atlanta qu sua selena foi pq los york blue k angeles 2016 color driven blend putt episode single spot bill 13 takeover chicken governor asf fried super bowl break capo buying shes atlanta avec atlantahttps died tonight making atlanta kind prisoner appreciate grew booze kimstrassel starburst stop white getting john atlanta_monster atlanta marietta threat showcase school bts_twt iheartawards pa atlanta estoy et je army nunca bestfanarmy um america press eastside essa tanto obviously trail crosswalk amo come atl atlanta join buckhead present shine arena evening philip school high place atlanta twitter harlem dekalb team 50cent went watch atlanta especially israel demand boycott easily offended minded reject car thanks gas follow someone atlanta self neighborhood knowledge museum city coming atlanta club florida orlando reason guest tf soccer 7 20 15 came j 25 nyc mar atlanta losangeles de la atlanta en los para people campa semana hacer area business owner atlanta here fact hat peek sneak leading miami knew housing atlanta pt zip ftbtv serving nearby affluence free atlanta listening credit ride whole uber ok junto holy drscott_atlanta realdonaldtrump 18 development dog enough waffle age vote lance april dope st air transit vehicle fanta regional broad plug company visit saw buy atlanta working regular build required headquarters grammy 29 ht atlanta average brady stapleton 36 related 76ers first thought deal lady atlanta wild karaoke successful cancer breast think add officially atlanta modern choice lane dat nb sauce glad recruiting atlanta comedy yelp checked sold iii vip arthur peep security happen learning availability gu tasting intelligence atlanta noamnesty ensure bail secretaryacosta timechols watered kaseymcclurerom 4sarah inca unholy unholiest best http atlanta giving ad ago seems dinner 300 leave real atlanta housewife guy tea posted essence january recap bc e de atlanta o que com una justin traficantes ryan announce hold opportunity congratulation speak forever westside diego peace atlanta class sip paint lituation tried growth monster predicts atlanta tera_monique favorite police record son front stuff murder representative bet atlanta going atlanta artist play b tech moved spotify bank exactly news help atlanta report flu room hospital fired anchor memorial foot rapper atlanta industry en lista colocan intransferibles neck todo always hell atlanta watched might oscar tiene bohemio 2010 xxl atlanta maiores traficantes de every chris falta try true whether call made another end atlanta law campaign identity nazi organizer classic local level jan atlanta gold leadership happened political climate rule answer enemy ing subject administrative mccabe lolol atlantapregame kimstrassel music party spring atlanta camp inside prison alcohol investigative repo atlanta chicago move radio many near damn point jr played win state atlanta south trip escape atlairport 2 via wheretraveler even big atlanta amazon almost hq2 sense niece landry jarvis se temporada segunda de atlanta trend logo becoming trust tao c perform mom toronto perfect folk ny 2019 ha atlanta friday 16 congrats hall emory debut atlanta fame consultant council series talking ippe forward together booth popular gucci mic lesson type dick funny sum article atlanta hq thrilled consider software'


# In[59]:

stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 3000, height = 2000,stopwords = stopwords).generate(text_200)
#wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(text_200)
                        #(#font_path='/Library/Fonts/Verdana.ttf',
                      #relative_scaling = 1.0,
                      #stopwords = stopwords # set or space-separated string
                      #).generate(text)
#plt.figure(figsize=(15,8))
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[24]:

hashtags=[]
with open('TwitterCleanedOp.csv','r') as ip:
    data=csv.DictReader(ip)
    for row in data:
        hashtags.append(row['Hashtags'])
#print(hashtags)


# In[35]:

text=re.sub(r'(\\x[0-9A-Fa-f]+)',r'', ' '.join(hashtags))
text=(" ".join(text.split())).replace("#"," ").lower()
print(text)


# In[47]:

stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 3000, height = 2000, relative_scaling = 0.5,collocations= False, stopwords = stopwords).generate(text)
                        #(#font_path='/Library/Fonts/Verdana.ttf',
                        #relative_scaling = 1.0,
                        #background_color : color value (default=”black”),
                        #stopwords = stopwords # set or space-separated string
                        #).generate(text)
#more parameters -> https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[48]:

#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=300, id2word = dictionary, passes = 20)
hdpmodel = gensim.models.HdpModel(corpus=corpus, id2word=dictionary)


# In[49]:

hdptopics = hdpmodel.show_topics(formatted=False)


# In[50]:

#print(hdptopics)


# In[51]:

topics = [(tp[0], [wd[0] for wd in tp[1]]) for tp in hdptopics]
################### Extracts topics from the topics in x #############
def wordcount_text(topics):
    wc_text=[]
    for i in range(len(topics)):
        wc_text.append(' '.join(topics[i][1]))
    return ' '.join(wc_text)

hdptext=wordcount_text(topics)


# In[57]:

wordcloud = WordCloud(width = 3000, height = 2000, relative_scaling = 0.5,collocations= False, stopwords = stopwords).generate(hdptext)
                        #(#font_path='/Library/Fonts/Verdana.ttf',
                        #relative_scaling = 1.0,
                        #background_color : color value (default=”black”),
                        #stopwords = stopwords # set or space-separated string
                        #).generate(text)
#more parameters -> https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# In[65]:




# In[66]:




# In[67]:

pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[119]:

twt='Gotta set up for tomorrow, and tomorrow...#realestateagent... #MotivationMonday #atlanta #myagentleigh silly'
hashtags=' '.join(set([re.sub(r"#+", "#", k) for k in set([re.sub(r"(\W+)$", "", j, flags = re.UNICODE) for j in set([i for i in twt.split() if i.startswith("#")])])]))
#twt.split('#')
#[w for w in nltk.word_tokenize(twt) if w.startswith("#")]
#hashtags=', '.join([w for w in nltk.word_tokenize(twt) if w.startswith("#")])
print(hashtags)


# In[131]:

re.sub(".+"," ",twt)
#[i for i in twt.split()]


# In[68]:

hash_tag = ['smyrna', 'Smyrna', 'SMYRNA', 'ROSWELL', 'Roswell', 'roswell', 'JohnsCreek', 'johnscreek', 'johnsCreek', 'Johnscreek',
                'JOHNSCREEK', 'Johns Creek', 'johns creek', 'johns Creek', 'Johns creek','JOHNS CREEK',
                '#ChooseATL','#AtlantaIsNow','#GrowAtlanta','#InvestAtlanta','#SupplyChainCity','#IotATL']


# In[69]:

print(hash_tag)

