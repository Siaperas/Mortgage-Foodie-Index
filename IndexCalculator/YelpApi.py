from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
# declarative base class to create table to add in our sqlalchemy database
class London_Restaurants(Base):

    __tablename__ = 'London_Restaurants'
    name = Column(String, primary_key=True)
    postal = Column(String, primary_key=True)
    rating = Column(Float)
    area=Column(String)
    def __getitem__(self, name):
        return getattr(self, name)
    def __getitem__(self, postal):
        return getattr(self, postal)
    def __getitem__(self, area):
        return getattr(self, area)

if __name__ == "__main__":
# Yelp api authenticator
    auth = Oauth1Authenticator(
        consumer_key="####",
        consumer_secret="####",
        token="####",
        token_secret="####"
    )

    client = Client(auth)
    #Create the database
    engine = create_engine('sqlite:///london_restaurants.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        # Yelp allows only up to 1000 items per category.
        categories = [ "thai", "turkish","cafes","cafeteria", "cajun", "cambodian", "caribbean","cheesesteaks"
            ,"chickenshop","chicken_wings","cantonese","dimsum","chinese","creperies","cuban","czech"
            ,"delis","diners","dinnertheater","ethiopian","hotdogs","filipino","fondue","fishnchips","food_court"
            ,"foodstands","french","gastropubs","german","gluten_free","greek"
            , "guamanian", "halal", "hawaiian", "himalayan", "hotdog", "hungarian", "indpak"
            , "indonesian", "irish", "italian", "japanese", "kebab", "korean", "kosher", "laotian", "latin"
            , "raw_food", "malaysian", "mexican", "mediterranean", "mideastern", "modern_european", "mongolian"
            , "moroccan", "noodles", "pakistani", "panasian", "persian", "peruvian", "pizza", "polish"
            , "popuprestaurants", "portuguese", "russian", "salad", "sandwiches", "scandinavian", "scottish"
            , "seafood", "singaporean", "soulfood", "soup", "southern", "spanish", "srilankan", "steak"
            ,  "sushi", "syrian", "taiwanese", "tapas", "tapasmallplates", "tex-mex", "thai"
            , "turkish", "ukrainian", "vegan", "vegetarian", "vietnamese", "waffles"
            ,"popcorn","macarons","chocolate", "candy","cakeshop","juicebars","cheese"
            ,"importedfood","icecream","farmersmarket","donuts","desserts","customcakes","cupcakes"
            ,"coffeeroasteries","bubbletea","beer_and_wine","bagels"
            ,"afghani", "african", "newamerican", "arabian", "argentine"
            , "austrian", "bangladeshi", "bbq", "basque", "brasseries", "british", "tradamerican"
            , "asianfusion", "australian", "belgian", "brazilian", "breakfast_brunch", "buffets", "burgers"
            , "burmese","pubs"]
        # Attempt to find food connected shops for each London area
        for category in categories:
            offset = 0
            print category
            total = client.search(location="London", category_filter=category, offset=offset).total
            print total
            while 1000 > offset < total:
                businesses = client.search(location="London", category_filter=category, offset=offset).businesses
                for biz in businesses:
                    area=None
                    if (biz.location.postal_code != None):
                        if(biz.location.postal_code[:2] == "EC"):
                            area="EC"
                        elif (biz.location.postal_code[:2] == "WC"):
                            area="WC"
                        elif (biz.location.postal_code[:2] != "EC" and biz.location.postal_code[0] == "E"):
                            area="E"
                        elif (biz.location.postal_code[:2] == "SE"):
                            area="SE"
                        elif (biz.location.postal_code[:2] == "SW"):
                            area="SW"
                        elif (biz.location.postal_code[:2] != "WC" and biz.location.postal_code[0] == "W"):
                            area="W"
                        elif (biz.location.postal_code[:2] == "NW"):
                            area="NW"
                        elif (biz.location.postal_code[:2] != "NW" and biz.location.postal_code[0] == "N"):
                            area="N"
                    # Retrieving the name, the rating, the postcode and the area of the shop
                    record = London_Restaurants(**{
                    'name': biz.name,
                    'rating': biz.rating,
                    'postal':biz.location.postal_code,
                    'area':area
                    })
                    check=s.query(London_Restaurants).filter_by(name=record['name'],postal=record['postal']).first()
                    if not check and record['name']!=None and record['postal']!=None and record['area']!=None and record['rating']!=None:
                        s.add(record)
                offset = offset + 20
        s.commit() #Attempt to commit all the records
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection

