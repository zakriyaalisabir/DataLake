def createEventTrigger(event):
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "message": "This is the dummy message in a JSON object."
        })
    }
    return response
