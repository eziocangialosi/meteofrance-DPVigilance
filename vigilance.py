from request import Request

class MeteoFranceVigilance(object):
    
    def __init__(self):
        self.requester = Request()
        
    def getDepartement(self, dep):
        response = self.obtainJson()
        self.parseData(dep,response)
        
    def obtainJson(self):
        return self.requester.obtainData('https://public-api.meteofrance.fr/public/DPVigilance/v1/textesvigilance/encours', 'GET').json();
        
    def parseData(self, dep, jsonData):
        flag = True
        i = 0
        while flag:
            if(jsonData['product']['text_bloc_items'][i]['domain_id'] == dep):
                flag = False
            else:
                if(i == len(jsonData['product']['text_bloc_items'])-1):
                    return False
                else:
                    i+=1
                
        print(jsonData['product']['text_bloc_items'][i])
        
    #def parseVigilanceLevel(self,):

API = MeteoFranceVigilance()
API.getDepartement("12")
