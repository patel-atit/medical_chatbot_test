import requests
from transformers import BertModel, BertTokenizer
import torch
from multi_turn_test_cases import test_cases

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

def run_multi_turn_test_cases(test_cases, api_url, test_indices=None):
    results = []
    for case in test_cases:
        for step in case['dialog']:
            chat_response = fetch_chatbot_response(api_url, step['utterance'])
            chat_vec = get_sentence_embedding(chat_response)
            highest_similarity = 0
            best_match_response = None

            for valid_response in step['valid_responses']:
                valid_vec = get_sentence_embedding(valid_response)
                similarity = cosine_similarity(chat_vec, valid_vec)
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match_response = valid_response  # Update the best match response

            results.append({
                'utterance': step['utterance'],
                'chat_response': chat_response,
                'expected_response': best_match_response,
                'similarity_score': highest_similarity,
                'passed': highest_similarity >= step.get('threshold', 0.75)
            })
    return results

def main():
    api_url = 'http://localhost:5001/chatbot'
    test_results = run_multi_turn_test_cases(test_cases, api_url)

    for result in test_results:
        print(f"Utterance: {result['utterance']}")
        print(f"Chat Response: {result['chat_response']}")
        print(f"Expected Response: {result['expected_response']}")
        print(f"Similarity Score: {result['similarity_score']:.2f}")
        print(f"Passed: {'Yes' if result['passed'] else 'No'}")
        print("------")

if __name__ == "__main__":
    main()

