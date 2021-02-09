# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:33:06 2020

@author: Adrian Gallo
"""

import tweepy
import json
import csv
from textblob import TextBlob
import pandas as pd
from unidecode import unidecode
import os

class TweetsListener(tweepy.StreamListener):
    def on_connect(self):
        print("Estoy conectado")
        
    def on_data(self, data):
        #print(json.dumps(status._json, indent=2))
        #print(data)
        global index
        global totalpos 
        global totalneg
        global totalneu
        try: 
            data = json.loads(data)
        # # try:
        #     if hasattr(data,'retweeted_status'):
        #         if hasattr(data['retweeted_status'], 'extended_tweet'):
        #             print('retweeted: ' + data['retweeted_status']['extended_tweet']['full_text'])
        #         else:
        #              print('retweeted: ' + data['retweeted_status']['text'])
        #     else:
        #         if hasattr(data, 'extended_tweet'):
        #             print('extended_tweet: ' + data['extended_tweet']['full_text'])
        #         else:
        #             print('text: ' + data['text'])
        #     print()
        #     print()
        #     print()
        #     # except AttributeError:
        #     #     print('attribute error: ' + data['text'])
            
                    
            try:
                location = data['user']['location']
            except TypeError:
                location = ''
            
            tweet_sentiment = TextBlob(unidecode(data['text']))
            
            if tweet_sentiment.sentiment.polarity > 0:
                sentimentStr = 'Positive'
                totalpos += 1
            elif tweet_sentiment.sentiment.polarity < 0:
                sentimentStr = 'Negative'
                totalneg += 1
            else:
                sentimentStr = 'Neutral'
                totalneu += 1
            
            tweet_info = {
                "ID":index,
                "name": data['user']['name'],
                "scname": data['user']['screen_name'],
                "tweet": unidecode(data['text']),
                "date": data['created_at'],
                "location": location,
                "time":data['timestamp_ms'],
                "sentiment": tweet_sentiment.sentiment.polarity,
                "sentimentStr": sentimentStr,
                "TotalPos": totalpos,
                "TotalNeg": totalneg,
                "TotalNeu": totalneu
                }
            #df = pd.DataFrame(columns = ['Name', 'Screen_Name', 'Tweet', 'Date', 'Location', 'Time','Sentiment','Sentiment', 'Positives', 'Negatives', 'Neutrals'])
            df = pd.DataFrame.from_dict([tweet_info])
    
            
            #df.loc[len(df)] = [name, scname, tweet, date, location, sentiment]
            #print(df)
            df.to_csv('./abortion.csv', mode='a', index=False, header=False)
            index+=1
            
            #print(name, scname, tweet, date, time_ms, location)
            
        except KeyError as e:
            print(str(e))
            
        return(True)
        
        
    def on_error(self, status_code):
        print("Error", status_code)

def main():
    
    #Declaramos las keys par pedir acceso a las API's de twitter
    consumer_key="f2S3RkFBIz8YSey9UiFjwjAqZ"
    consumer_key_secret="we8EfdVqvfSEdYgxj8ocKS9gLCYOwumKlVRkoUe9IDjhh4v5gj"
    access_token="1297961226018881542-HJtqFjFAsonEh4548VHTm337H9sxHW"
    access_token_secret="ceWxdMeYChQueIdBMKRot43fDPJg5xCgzWaSkx6k5tIFZ"
    
    #solicita permisos a twitter
    auth= tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    
    #Obtiene mi informacion
    #data = api.me()
    #print (json.dumps(data._json, indent=2))
    
    #obtiene informacion de otro usuario
    #data = api.get_user("pam86975372")
    #print (json.dumps(data._json, indent=2))
    
    #obtener los followers de un usuario 
    
    #data = api.followers(screen_name="nike")
    
    #for user in data:
    #    print (json.dumps(user._json, indent=2))
    
    #print (len(data))
    
    #Obtener followers de un usuario con Cursor 
    #for user in tweepy.Cursor(api.followers, screen_name="nike").items(100):
     #   print (json.dumps(user._json, indent=2))
    
    #Obtener timeline 
    #for tweet in tweepy.Cursor(api.user_timeline, screen_name="nike", tweet_mode="extended").items(1):
    #    print (json.dumps(tweet._json,indent=2))
        
    
    #for tweet in tweepy.Cursor(api.search, q="Drogas", tweet_mode="extended").items(1):
    #    print (json.dumps(tweet._json,indent=2))
    #    print (tweet._json["full_text"])
    
    stream = TweetsListener()
    streamingApi = tweepy.Stream(api.auth,stream)
    diccionario = ['aborto', 'legalización del aborto', 'aborto legal', 'aborto gratuito', 'aborto seguro', 'proaborto', 'embrio', 'penalizar el aborto', 'embarazo no deseado', 'cria', 'feto', 'abortion','legal abortion','free abortion', 'safe abortion', 'pro-abortion', 'embryo','fetus']
    streamingApi.filter(#Define los filtros del streaming
        #follow=["1297961226018881542"]#Filtro de ususario de id"1297961226018881542"
        track=diccionario,#Filtro por palabras clave
        #track=['aborto']
        languages=['es', 'en']#idiomas
        #locations=[-102.87417653,21.62226634,-101.83528942,22.45958955] #Segun coordenadas https://boundingbox.klokantech.com/
    )

if __name__ == '__main__':
    
    #datos = pd.read_csv('abortion.csv')
    if os.path.isfile('abortion.csv'):
        datos = pd.read_csv('abortion.csv')
        #print(datos['Positives'])
        index = datos.at[datos.index[-1],'ID'] + 1
        totalpos = datos.at[datos.index[-1],'Positives']
        totalneg = datos.at[datos.index[-1],'Negatives']
        totalneu = datos.at[datos.index[-1],'Neutrals']
    else:
        df = pd.DataFrame(columns = ['ID','Name', 'Screen_Name', 'Tweet', 'Date', 'Location', 'Time','Sentiment','Sentiment', 'Positives', 'Negatives', 'Neutrals'])
        df.to_csv('./abortion.csv', mode='a', index=False)
        index = 0
        totalpos = 0
        totalneg = 0
        totalneu = 0
    #columns = ['Name', 'Screen_Name', 'Tweet', 'Date', 'Location', 'Time','Sentiment','Sentiment', 'Positives', 'Negatives', 'Neutrals']
    main()
    



