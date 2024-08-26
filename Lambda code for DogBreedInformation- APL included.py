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
        breed_info, images = fetch_dog_breed_info(dog_breed)
        if breed_info and images:
            return build_response_with_apl(breed_info, images, dog_breed)
        else:
            return build_response(f"Sorry, I couldn't find any information about {dog_breed}.")
    else:
        return build_response("Sorry, I didn't get that. You can ask for information about any dog breed.")

def fetch_dog_breed_info(dog_breed):
    url = f"https://dog.ceo/api/breed/{dog_breed.lower()}/images"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            images = data['message'][:3]  # Get first 3 images
            breed_info = f"Here are some images of {dog_breed}."
            return breed_info, images
        else:
            return None, None
    else:
        return None, None

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

def build_response_with_apl(breed_info, images, dog_breed):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': breed_info
            },
            'directives': [
                {
                    'type': 'Alexa.Presentation.APL.RenderDocument',
                    'token': 'dogBreedToken',
                    'document': {
                        'type': 'APL',
                        'version': '1.5',
                        'mainTemplate': {
                            'items': [
                                {
                                    'type': 'Container',
                                    'items': [
                                        {
                                            'type': 'Text',
                                            'text': f"Dog Breed: {dog_breed.capitalize()}",
                                            'fontSize': '30dp',
                                            'fontWeight': 'bold',
                                            'color': '#FFFFFF'
                                        },
                                        {
                                            'type': 'Image',
                                            'source': images[0],
                                            'width': '100%',
                                            'height': '30vh',
                                            'scale': 'best-fill'
                                        },
                                        {
                                            'type': 'Image',
                                            'source': images[1],
                                            'width': '100%',
                                            'height': '30vh',
                                            'scale': 'best-fill'
                                        },
                                        {
                                            'type': 'Image',
                                            'source': images[2],
                                            'width': '100%',
                                            'height': '30vh',
                                            'scale': 'best-fill'
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            ],
            'shouldEndSession': True
        }
    }
