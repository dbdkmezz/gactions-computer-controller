import json
import pprint
import logging

from django.http import HttpResponse, JsonResponse

from .models import VideoFolder
from .messenger import Messenger


logger = logging.getLogger('django')


def index(request):
    try:
        input = json.loads(request.body.decode('utf-8'))['inputs'][0]
    except json.JSONDecodeError:
        logger.warn("Unable to decode json")
        return HttpResponse("Hello, world. You're at the video_player index.")

    logger.info("Input: %s", pprint.pformat(input))
    if 'arguments' not in input:
        logger.debug("No arguments, falling back to asking for input")
        return googleResponse("What would you like to play?", final=False)
    else:
        query = input['arguments'][0]['textValue'].lower()
        video = VideoFolder.get_next_video_matching_query(query)
        if video:
            video.play()
            return googleResponse("OK! Playing {}".format(video.name))
        if any(s in query for s in ('play', 'pause', 'resume')):
            Messenger.play_pause_video()
            return googleResponse("On it!")
        if 'blue' in query:
            Messenger.open_website('https://www.bbc.co.uk/iplayer/episodes/p04tjbtx')
            return googleResponse("OK! Opening Blue Planet, on iPlayer.")
        logger.debug("Not sure what to do with the query '%s', asking again.", query)
        return googleResponse("Sorry. I don't know how to {}. What would you like to play?".format(query), final=False)


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
