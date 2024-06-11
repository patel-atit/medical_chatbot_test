import requests
from transformers import BertModel, BertTokenizer
import torch

def get_model_and_tokenizer():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
    return model, tokenizer

def get_sentence_embedding(text, model, tokenizer):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**encoded_input)
    hidden_states = outputs.hidden_states
    sentence_embedding = torch.mean(hidden_states[-1], dim=1).squeeze()
    return sentence_embedding

def cosine_similarity(vec1, vec2):
    cosine_sim = torch.nn.functional.cosine_similarity(vec1, vec2, dim=0)
    return cosine_sim.item()

def fetch_chatbot_response(api_url, message):
    response = requests.post(api_url, json={'message': message})
    if response.status_code == 200:
        return response.json()['response']
    else:
        raise Exception(f"Failed to fetch data from chatbot API. Status code: {response.status_code}")

def main():
    text1 = "We offer Semaglutide & Tirzepatide all over the US! Is there one you are more interested in learning about? And what state do you reside in? That way we can make sure to give you accurate pricing!"
    api_url = 'http://localhost:5001/chatbot'
    
    try:
        text2 = fetch_chatbot_response(api_url, 'What services do you offer?')
        model, tokenizer = get_model_and_tokenizer()
        vec1 = get_sentence_embedding(text1, model, tokenizer)
        vec2 = get_sentence_embedding(text2, model, tokenizer)

        similarity = cosine_similarity(vec1, vec2)

        # Assert similarity score with custom error message if below threshold
        if similarity < 0.75:
            raise AssertionError(f"ERROR: Response similarity too low: {similarity:.2f}")

        # Print similarity score with two decimal places
        print(f"Similarity score: {similarity:.2f}")

    except AssertionError as e:
        print(str(e))
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
