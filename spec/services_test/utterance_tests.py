import requests
from transformers import BertModel, BertTokenizer
import torch

# Load the model and tokenizer globally
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

def get_sentence_embedding(text):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**encoded_input)
    hidden_states = outputs.hidden_states
    sentence_embedding = torch.mean(hidden_states[-1], dim=1).squeeze()
    return sentence_embedding

def cosine_similarity(vec1, vec2):
    return torch.nn.functional.cosine_similarity(vec1, vec2, dim=0).item()

def fetch_chatbot_response(api_url, message):
    response = requests.post(api_url, json={'message': message})
    if response.status_code == 200:
        return response.json()['response']
    else:
        raise Exception(f"Failed to fetch data from chatbot API. Status code: {response.status_code}")

def run_test_cases(test_cases, api_url, test_indices=None):
    results = []
    if test_indices is None:
        selected_cases = test_cases
    else:
        selected_cases = [test_cases[i] for i in test_indices if i < len(test_cases)]

    for case in selected_cases:
        threshold = case.get('threshold', 0.75)  # Default threshold is 75%
        try:
            chat_response = fetch_chatbot_response(api_url, case['utterance'])
            chat_vec = get_sentence_embedding(chat_response)
            matched = False
            for valid_response in case['valid_responses']:
                valid_vec = get_sentence_embedding(valid_response)
                similarity = cosine_similarity(chat_vec, valid_vec)
                if similarity >= threshold:
                    matched = True
                    results.append((case['utterance'], chat_response, True, similarity))
                    break
            if not matched:
                results.append((case['utterance'], chat_response, False, 0))
        except Exception as e:
            results.append((case['utterance'], str(e), False, 0))
    return results

def main(test_indices=None):
    test_cases = [
        {
            "utterance": "How can I book an appointment?",
            "valid_responses": [
              "Yes. Can you please provide a phone number so one of our team members can reach out to you to see if you qualify and schedule an appointment?",
              "You can book an appointment with one of our dedicated team members or you can book through our website online! https://ivologistweightlosscenter.myaestheticrecord.com/book/appointments?user_id=1RrxnwGZpW3Vz7vZYqmDokN05va4Q6",
              "You can book online by visiting this link https://ivologistweightlosscenter.myaestheticrecord.com/book/appointments?user_id=1RrxnwGZpW3Vz7vZYqmDokN05va4Q6",
              "If you can provide a phone number we can have one of our team members call you to confirm eligibility and schedule an appointment"
            ],
            "threshold": 0.80
        },
        {
            "utterance": "What services do you offer?",
            "valid_responses": [
                "We offer Semaglutide & Tirzepatide all over the US! Is there one you are more interested in learning about? And what state do you reside in? That way we can make sure to give you accurate pricing!"
            ],
            "threshold": 0.80
        },
        {
            "utterance": "How much for a 2.5mg program in Texas Sema?",
            "valid_responses": [
                "For a 2.5mg program of Semaglutide in Texas, the price is $499. This program includes a vial size of 5ml with a dosage of 100 units over 5 weeks. If you are interested in longer programs for the 2.5mg please let us know. Would you like to book an appointment or need further assistance?"
            ],
            "threshold": 0.80
        },
        {
            "utterance": "How much for a 2.5mg program in Texas for Tirzepatide?",
            "valid_responses": [
                "For a 5mg program of Tirzepatide in Texas, the price is $599. This program includes a vial size of 3ml with a dosage of 300 units over 8 weeks. If you are interested in longer programs for the 5mg please let us know. Would you like to book an appointment or need further assistance?"
            ],
            "threshold": 0.95
        }
    ]

    api_url = 'http://localhost:5001/chatbot'
    test_results = run_test_cases(test_cases, api_url, test_indices)

    for result in test_results:
        print("Utterance:", result[0])
        print("Response:", result[1])
        print("Passed:", "Yes" if result[2] else "No")
        if result[2]:
            print("Similarity Score:", f"{result[3]:.2f}")
        print("------")

if __name__ == "__main__":
    # Example of running specific test cases: main([0]) to run the first test case only
    # To run all test cases, just call main() or main([])
    main([3])
