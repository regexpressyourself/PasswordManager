from pymongo import MongoClient
# need to pull this from an environment variable
client = MongoClient('mongodb://passman:passman@ds161640.mlab.com:61640/passman')

db = client.passman

collection = db.main_collection

userName = ""

def setDBUsername(username):
    global userName 
    userName = username

def existsDuplicateUser(name, pw):
    user = collection.find_one({"name": name})
    if (user): return True
    else: return False




def addUser(name, pw):
    '''
    Adds a user to the database. This should only be called once 
    locally, unless the user wants to have multiple accounts on 
    their system. 

    This function creates a new Mongo 'Document' in the 
    main collection. The Document will contain all user data.
    '''

    if existsDuplicateUser(name, pw):
        return False

    result = collection.insert_one({
        'name': name,
        'password': pw,
        'data': []
        })

    if result: return True
    else: return False

def checkUserCredentials(name, pw):
    user = collection.find_one({"name": name, "password": pw})
    if (user): return True
    else: return False

def getAllServices():
    '''
    Returns an array of all the services for the current user.

    Return value contains the data as it is stored in the database. We
    can run through the array and clean it up a bit too - just need to 
    see the implementation of our list function in order to do so.
    '''

    serviceArray = collection.find_one({"name": userName})
    serviceArray = serviceArray['data'] if serviceArray else serviceArray
    if serviceArray: return serviceArray
    else: return False

def checkIfServiceExists(name):
    '''
    Checks if a given service name is in the database already.

    This should probably be called 'client side,' but I have
    the addService method checking it as well.
    '''

    serviceArray = getAllServices()
    if not serviceArray:
        return False

    found = False
    for service in serviceArray:
        if service['service'] == name:
            found = True
    return found

def addService(name, pw, serviceUrl="", serviceUserName=""):
    '''
    Add a service to the document for current user.

    Checks if service name already exists before adding. 
    Prints an error message if service name already exists.
    '''

    found = checkIfServiceExists(name)
    if not found:
        result = collection.find_one_and_update({'name': userName},{'$push':{
            'data': {
                'service': name,
                'servicePassword': pw,
                'serviceUrl': serviceUrl,
                'serviceUserName': serviceUserName
            }
        }
        })

        if result: return True
        else: return False

    else:
        print("\nERROR: Database already contains service " + name+"\n")

def removeService(name):
    '''
    Remove a service from an account.
    '''

    result = collection.update({'name': userName},
            {'$pull':{ 'data': {'service' : name}}})

    if result: return True
    else: return False

def updateService(oldName, newName, pw, serviceUrl="", serviceUserName=""):
    '''
    Updates a service to a new set of data. Be sure to provide the entire
    fingerprint of the new data, not just what changed. This includes any url,
    username, etc. even if they have not been changed
    '''
    removeService(oldName)
    addService(newName, pw, serviceUrl, serviceUserName)

def getServiceByName(name):
    '''
    Returns a given service for the current user.
    '''
    serviceArray = getAllServices()

    for serviceDict in serviceArray:
        if serviceDict["service"] == name:
            service = serviceDict

    return service
