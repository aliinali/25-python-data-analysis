
import json

def serialize_to_json(data):
    data = json.dumps(data, indent=2, ensure_ascii=True)
    return data

data = eval(input())
print(serialize_to_json(data))



import pickle


def get_sorted_keys_values(file_path):
    lis = [[],[]]
    with open(file_path,'r') as file:
        data = pickle.load(file)
        sorted_lis = sorted(data.items(),key = lambda x:x[0], reverse= False)
        for name,number in sorted_lis:
            lis[0].append(name)
            lis[1].append(number)
        return lis
    

    