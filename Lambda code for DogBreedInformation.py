import json
import requests

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event)

def on_launch(event):
    return build_response("Welcome to Dog Breed Information. You can ask for information about any dog breed.")

def on_intent(event):
    intent_name = event['request']['intent']['name']
    
    if intent_name == "DogBreedInfoIntent":
        dog_breed = event['request']['intent']['slots']['dogBreed']['value']
        return get_dog_breed_info(dog_breed)
    else:
        return build_response("Sorry, I didn't get that. You can ask for information about any dog breed.")

def get_dog_breed_info(dog_breed):
    breed_info = fetch_dog_breed_info(dog_breed)
    
    if breed_info:
        return build_response(breed_info)
    else:
        return build_response(f"Sorry, I couldn't find any information about {dog_breed}.")

def fetch_dog_breed_info(dog_breed):
    url = f"https://dog.ceo/api/breed/{dog_breed.lower()}/images"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return f"Here are some images of {dog_breed}: {', '.join(data['message'][:3])}"
        else:
            return None
    else:
        return None

def build_response(output):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'shouldEndSession': True
        }
    }
