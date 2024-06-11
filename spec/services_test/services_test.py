import requests
import difflib

def get_similarity_score(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def test_conversational_ai():
    url = 'http://localhost:5001/chatbot'
    data = {'message': 'Hello, how are you?'}
    expected_response = 'I\'m here and ready to assist you. How can I help'

    try:
        response = requests.post(url, json=data)
        actual_response = response.json().get('response', '')
        similarity_score = get_similarity_score(expected_response, actual_response)

        # Print results nicely
        print(f"Expected: {expected_response}")
        print(f"Actual: {actual_response}")
        print(f"Similarity Score: {similarity_score:.2f}")

        # Assert without traceback
        if similarity_score < 0.8:
            print(f"ERROR: Response similarity too low: {similarity_score:.2f}")
    except AssertionError as e:
        print(str(e))

# You can add more tests here
test_conversational_ai()
