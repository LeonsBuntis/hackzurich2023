from transformers import pipeline

c = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Lookup key by value
def lookup_key_by_value(target_value, dictionary):
    for key, value_list in dictionary.items():
        if target_value in value_list:
            return key
    return None

def get_relevat_instrument_from_news(text):
    instrumentDict = {
        'CSCO': ['Cisco', 'IT', 'Tech'],
        'PFE': ['Pfizer', 'Medicine', 'Healthcare', 'Pharma'],
        'SAN': ['Santander', 'Banking', 'Finance', 'Loan'],
        'ING': ['ING', 'Banking', 'Finance', 'Loan'],
        'NVDA': ['NVidia', 'Tech', 'Crypto', 'Gaming']
    }
    
    keywords = [value for sublist in instrumentDict.values() for value in sublist]
    result = c(text, keywords, multi_label=True)
    
    # print(result)
        
    output_dict = dict(zip(result['labels'], result['scores']))
    
    sorted_dict = {k: v for k, v in sorted(output_dict.items(), key=lambda item: item[1], reverse=True)}
    
    # print(sorted_dict)
    result = []
    
    for k, v in sorted_dict.items():
        if v > 0.7:
            inst = lookup_key_by_value(k, instrumentDict)
            result.append(inst)
    
    return result
    
    
def get_mood_for_news(text):
    result = c(text, ['sad', 'happy'])
    # print(f'moods: {result}')
    return result['scores'][0]