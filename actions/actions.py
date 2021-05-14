# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from random import randint
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet # used to set slots
from rasa_sdk.forms import FormAction #to create form actions
from weather import Weather
from entertain import EntertainUser, News_Provider


class ActionFacilitySearch(Action):

    def name(self) -> Text: # name of the action used when creating training stories
        return "action_facility_search"

     # the run fuction defines what the custom action does
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        facility = tracker.get_slot("facility_type")
        #address = "300 Hyde St, San Francisco"
        #dispatcher.utter_message(text = "Here is the address of the {}:{}".format(facility_type, address))
        dispatcher.utter_message(text = "I'm sorry, there are no {} in your area".format(facility))
        
#class FacilityForm(FormAction):
    
    # def name(self):
    #     return facility_form

    # def required_slots(tracker: Tracker):
    #     return ["facility_type","location"]

    # def slot_mappings(self):
    #     return {"facility_type":self.from_entity(entity="facility_type", 
    #                                             intent=["inform","search_provider"]),
                                                
    #             "location":self.from_entity(entity="location",
    #                                         intent=["inform","search_provider"])}


class NewsForm(FormAction):
    
    def name(self):
        return "news_form"

    @staticmethod
    def required_slots(tracker: Tracker):
        #print("required_slots(tracker:Tracker)")
        return ["news_channel", "news_category"]

    def submit(self, 
               dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text, Any]
               ) -> List[Dict]:

               channel = tracker.get_slot('news_channel')
               category = tracker.get_slot('news_category')

               results = News_Provider(channel=channel, category=category)
               news_line = results[randint(0,25)]
               title = news_line["title"]
               url = news_line["url"]

               dispatcher.utter_message(response="utter_entertainment_news", url=url, title=title)
               return []

    def slot_mappings(self):
        return {"news_channel":self.from_entity(entity="news_channel", 
                                                intent=["news_updates"]),
                                                
                "news_category":self.from_entity(entity="news_category",
                                            intent=["news_updates"])}

        #return await super().submit(dispatcher, tracker, domain)




class ActionEntertain(Action):
    def name(self):
        return "entertain_user"
    
    def run(self, dispatcher:CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]):

            func = EntertainUser()
            news_line = func[randint(0,25)]
            title = news_line["title"]
            url = news_line["url"]

            dispatcher.utter_template("utter_entertainment_news", tracker, title=title, url=url)

# class ActionProvideNews(Action):
#     def name(self):
#         return "provide_news"

#     def run(self, dispatcher:CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]):

#             cat = tracker.latest_message['text']
#             chan = tracker.latest_message['text']

#             func_cat = News_Category(cat)
#             func_chan = News_Channel(chan)

#             cat_line = func_cat[randint(0,25)]
#             news_title = cat_line["title"]
#             news_url = news_line["url"]




class ActionWeatherSearch(Action):
    def name(self):
        return "action_weather"

    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

            city = tracker.latest_message['text']
            temp = int(Weather(city)['temp'] - 273)

            dispatcher.utter_template("utter_temp", tracker, temp=temp)
            #return []
