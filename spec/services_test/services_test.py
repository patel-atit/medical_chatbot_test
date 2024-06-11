import requests
import difflib

def get_similarity_score(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def test_conversational_ai():
    url = 'http://localhost:5001/chatbot'
    data = {'message': 'What services do you offer?'}
    expected_response = 'We offer Semaglutide & Tirzepatide all over the US! Is there one you are more interested in learning about? And what state do you reside in? That way we can make sure to give you accurate pricing!'

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
