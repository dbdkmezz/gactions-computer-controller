import json
import pprint

from django.http import HttpResponse, JsonResponse
from .messenger import Messenger


def index(request):
    with open("/home/paul/loggy/log", "w") as f:
        f.write("\n\n{}\n".format(request))
        f.write("{}\n".format(pprint.pformat(request.body.decode('utf-8'))))

        try:
            j = json.loads(request.body.decode('utf-8'))
        except:
            f.write("can't load json")
            j = None
        if True:  # j and "user" in j:
            try:
                input = j['inputs'][0]
                f.write(pprint.pformat(input))
                if 'arguments' not in input:
                    return googleResponse("What would you like to play?", final=False)
                else:
                    query = input['arguments'][0]['textValue'].lower()
                    # query = j['inputs'][0]['rawInputs'][0]['query'].lower()
                    f.write("\nquery {}".format(query))
                    if 'blue' in query:
                        f.write("BLUE")
                        Messenger.open_website('https://www.bbc.co.uk/iplayer/episodes/p04tjbtx')
                        return googleResponse("OK! Opening Blue Planet, on iPlayer.")
                    if 'rick' in query or 'morty' in query:
                        f.write("\nRICK")
                        # Messenger.open_video('/media/paul/e9dfc73a-25f7-4831-80da-1f5319e4893d/paul/Downloads/rm01.mkv')
                        return googleResponse("Great! Playing Rick and Morty")

                    return googleResponse(
                        "Sorry. I don't know how to {}. What would you like to play?".format(query),
                        final=False
                    )

            except Exception as e:
                f.write("{}".format(e))
    return HttpResponse("Hello, world. You're at the polls index.")


def googleResponse(text, final=True):
    if final:
        response = {
            "expectUserResponse": False,
            "finalResponse": {
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": text,
                            }
                        }
                    ]
                }
            },
            "isInSandbox": True,
        }
    else:
        response = {
            "expectUserResponse": True,
            "isInSandbox": True,
            "expectedInputs": {
                "inputPrompt": {
                    "richInitialPrompt": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": text,
                                }
                            }
                        ]
                    }
                },
                # "possibleIntents": [
                #     {
                #         object(ExpectedIntent)
                #     }
                # ],
            }
        }

    return JsonResponse(response)
