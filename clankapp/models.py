import pymongo
import datetime
import os
import bcrypt
import datetime
from bson.objectid import ObjectId

mongo = os.environ.get("MONGO")

client = pymongo.MongoClient(mongo)

db = client['recipe_app']

users = db['users']
recipes = db['recipes']

# hashing models
def is_valid_signup(email, username, password, password2):
    if len(email) < 4:
        data={
             'message':'Email must be greater than 4 chars',
             'category':'error'
         }
        return data
    elif len(username) < 2:
        data={
             'message':'Username must be greater than 2 chars',
             'category':'error'
         }
        return data
    elif password != password2:
        data={
             'message':'Passwords must match',
             'category':'error'
         }
        return data
           
    elif len(password) < 8:
        data={
             'message':'Passwords must match',
             'category':'error'
         }
        return data
    else:
        data={
             'message':'Account created.',
             'category':'success'
         }
        return data

def is_valid_login(username, password):
    user = db.users.find_one({'username':username})
    if user:
        hashed_pw = user['password']
        do_pw_match = compare_password(password, hashed_pw)
        if do_pw_match == True:
            return True
        else:
            return False
    return False
        
            
# hashes and returns password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed_pw.decode('utf8')
#compares non hashed and hashed passwords
def compare_password(password, hashed_pw):
    if bcrypt.checkpw(password.encode('utf8'), hashed_pw.encode('utf8')):
        print("match")
        return True
    else:
        return False

# database models 
def add_user(username, email, password):
    hash_pw = hash_password(password)
    user_data = {
        'username': username,
        'email': email,
        'password': hash_pw,
        'upvoted': {}
    }
    return users.insert_one(user_data)


def add_recipe(recipe_name, category, ingredients, instructions, username, description):
    recipe_data = {
        'recipe_name': recipe_name,
        'category': category,
        'ingredients': ingredients,
        'instructions': instructions,
        'username': username,
        'description': description,
        'date_added': datetime.datetime.now(),
        'date_modified': datetime.datetime.now()
    }
    return recipes.insert_one(recipe_data)

def upvote(recipeID, rating, userID):
    recipe = recipes.find_one({'_id':recipeID})
    num_upvotes = recipe.get('upvotes')
    
    current_username = userID
    user = users.find_one({'username': userID})
    has_upvoted = 0
    '''
    if rating == None:
        query2 = {"username":current_username}
        upvoted_rec = {"upvoted": {recipeID: has_upvoted}}
        users.update_one(query2, upvoted_rec)
    '''
    if num_upvotes:
        if rating == True:
            num_upvotes +=1
            has_upvoted = 1
        else:
            num_upvotes -=1
            has_upvoted = -1
    else:
        if rating == True:
            num_upvotes =1
            has_upvoted = 1
        else:
            num_upvotes =-1
            has_upvoted = -1

    query = {"_id":recipeID}
    upvotes ={"$set":{'upvotes': num_upvotes}}

    query2 = {"username":userID}
    upvoted_rec = {"$set":{"upvoted":{recipeID: has_upvoted}}}
    print(upvoted_rec)
    x = users.update_one(query2, upvoted_rec)

    return recipes.update_one(query, upvotes)
    