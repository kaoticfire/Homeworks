from bs4 import BeautifulSoup
from requests import HTTPError, get as rget

IDEAS = {'tacos': ['ground beef', 'lettuce', 'tortillas', 'taco shells', 'cheese', 'tomatoes', 'taco seasoning'],
         'meatloaf': ['ground beef', ],
         'burgers': ['ground beef or hamburger patties', 'lettuce', 'cheese', 'tomatoes', 'fries', 'condiments'],
         'biscuits and gravy': ['sausage', 'biscuits', 'country gravy'],
         'lasagna': ['ground beef', 'lasagna noodles', 'spaghetti sauce', 'cheese'],
         'hamburger helper': ['hamburger helper', 'ground beef'],
         'steak and eggs': ['steak', 'eggs'],
         'pizza': ['pizza'],
         'wings': ['chicken wings', 'wings sauce'],
         'salad': ['lettuce', 'cheese', 'salad dressing', 'bacon bits', 'tomatoes', 'cucumbers', 'jalapenos'],
         'chicken alfredo': ['chicken', 'alfredo sauce', 'noddles', 'Parmesan cheese'],
         'enchiladas': ['beef or chicken', 'cheese', 'corn tortillas', 'enchilada sauce', 'jalapenos'],
         'barbeque meat cups': ['ground beef', 'cheese', 'barbeque sauce', 'biscuit dough'],
         'fish sticks and fries': ['fish sticks', 'fries'],
         'chicken nuggets': ['chicken nuggets', ' a vegetable'],
         'hot dogs': ['hot dogs'],
         'mac and cheese with pigs-in-a-blanket': []
         }


def get_ingredients(url: str) -> list:
    """ This function scrapes the website provided for the ingredients of a particular dish.

    Args:
        url: the website to scrape. At this time the scraping works only with
        Allrecipes.com.
    Return:
        The list of ingredients.
    Raises:
         HTTPError: raises exception if trouble connecting to webpage or cannot find html elemnets.
    """
    try:
        source = rget(url).text
        soup = BeautifulSoup(source, 'lxml')
        ingredients = []
        for item in soup.find_all('li', class_="ingredients-item"):  # .li.label.span.span.text
            ingredient = item.label.span.span.text
            ingredients.append(ingredient)
    except HTTPError as exception:
        print(exception)
        return []
    return ingredients
