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
    if test_indices is None:
        selected_cases = test_cases
    else:
        selected_cases = [test_cases[i] for i in test_indices if i < len(test_cases)]

    for case in selected_cases:
        conversation_result = []
        try:
            for step in case['dialog']:
                chat_response = fetch_chatbot_response(api_url, step['utterance'])
                chat_vec = get_sentence_embedding(chat_response)
                threshold = step.get('threshold', 0.75)  # Default threshold
                valid_response_found = False

                for valid_response in step['valid_responses']:
                    valid_vec = get_sentence_embedding(valid_response)
                    similarity = cosine_similarity(chat_vec, valid_vec)
                    if similarity >= threshold:
                        valid_response_found = True
                        conversation_result.append((step['utterance'], chat_response, True, similarity))
                        break
                
                if not valid_response_found:
                    conversation_result.append((step['utterance'], chat_response, False, 0))
                    break  # Stop the test if any response fails to meet the threshold

        except Exception as e:
            conversation_result.append((step['utterance'], str(e), False, 0))
        
        results.append(conversation_result)
    return results

def main(test_indices=None):
    api_url = 'http://localhost:5001/chatbot'
    test_results = run_multi_turn_test_cases(test_cases, api_url, test_indices)

    for dialog_result in test_results:
        for result in dialog_result:
            print("Utterance:", result[0])
            print("Response:", result[1])
            print("Passed:", "Yes" if result[2] else "No")
            print("Similarity Score:", f"{result[3]:.2f}")
            print("------")

if __name__ == "__main__":
    # Example of running specific test cases: main([0]) to run the first test case only
    # To run all test cases, just call main() or main([])
    main([2])
