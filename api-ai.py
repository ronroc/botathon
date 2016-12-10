import apiai
import json
import requests
#print apiai.__version__
CLIENT_ACCESS_TOKEN=""
brand=None
type=None
price=None


def handle_query(query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'
    request.query = query
    response = request.getresponse()
    return (json.loads(response.read()))
def saveType(t):
    global type
    type=t

def saveBrand(b):
    global brand
    brand=b

def searchCata(brand,type,price):
    l_price=float(price)-1000

    r_url='http://localhost:8000/about/?brand='+brand+'&price='+str(l_price)+'-'+price
    r=requests.get(r_url)

    if r.text:
        res=json.loads(r.text)
        #print res
        return ['model\t'+' price']+[t['title']+'\t'+str(t['mrp']) for t in res[:3]]
    else:
        return ['Sorry we dont have such a mobile']

def savePrice(p):
    global price
    price=p

def main():
    user_input = ''
    cata_flag=True
	#loop the queries to API.AI so we can have a conversation client-side
    while user_input != 'exit':


        user_input  = raw_input("me: ")
		#query the console with the user input, retrieve the response
        if not brand or not type or not price :
            response = handle_query(user_input)
            #parse the response
            result = response['result']
            fulfillment = result['fulfillment']

            print 'bot: ' + fulfillment['speech']

            #if an action is deteted, fire the appropriate function
            if result['action'] == 'saveType':
                saveType(user_input)
            if result['action'] == 'saveBrand':
                saveBrand(user_input)
            if result['action'] == 'savePrice':
                savePrice(user_input)
        global brand
        global price
        global type
        if brand and type and price and cata_flag:
            print 'we have following options for you \n'+'\n'.join(searchCata(brand,type,price)) +'\n'+ 'Select some'

            cata_flag = False
            #print 'bot: ' +'Hey please confirm you want a '+type+' '+brand+' mobile phone under '+price
        #print brand,price,type


#if __name__ == "__main__":
main()
#print brand,type,price
