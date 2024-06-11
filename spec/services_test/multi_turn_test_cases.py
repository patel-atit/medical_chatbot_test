test_cases = [
    {
        "dialog" : [{
            "utterance": "How can I book an appointment?",
            "valid_responses": [
              "Yes. Can you please provide a phone number so one of our team members can reach out to you to see if you qualify and schedule an appointment?",
              "You can book an appointment with one of our dedicated team members or you can book through our website online! https://ivologistweightlosscenter.myaestheticrecord.com/book/appointments?user_id=1RrxnwGZpW3Vz7vZYqmDokN05va4Q6",
              "You can book online by visiting this link https://ivologistweightlosscenter.myaestheticrecord.com/book/appointments?user_id=1RrxnwGZpW3Vz7vZYqmDokN05va4Q6",
              "If you can provide a phone number we can have one of our team members call you to confirm eligibility and schedule an appointment"
            ],
            "threshold": 0.80
            }]
    },
    {
        "dialog" : [{
            "utterance": "What services do you offer?",
            "valid_responses": [
                "We offer Semaglutide & Tirzepatide all over the US! Is there one you are more interested in learning about? And what state do you reside in? That way we can make sure to give you accurate pricing!"
            ],
            "threshold": 0.80
        }]
    },
    {
        "dialog" : [{
            "utterance": "How much for a 2.5mg program for Sema?",
            "valid_responses": [
                "Could you please let me know which state you are in so I can provide you with accurate pricing"
            ],
            "threshold": 0.80
            },{
            "utterance": "I am in Texas",
            "valid_responses": [
            "For a 2.5mg program of Semaglutide in Texas, the price is $499. This program includes a vial size of 5ml with a dosage of 100 units over 5 weeks. If you are interested in longer programs for the 2.5mg please let us kno    w. Would you like to book an appointment or need further assistance?"
            ],
            "threshold": 0.80
            }
        ]
    },
    {
        "dialog" : [{
            "utterance": "How much for a 2.5mg program in Texas for Tirzepatide?",
            "valid_responses": [
                "For a 5mg program of Tirzepatide in Texas, the price is $599. This program includes a vial size of 3ml with a dosage of 300 units over 8 weeks. If you are interested in longer programs for the 5mg please let us know. Would you like to book an appointment or need further assistance?"
            ],
            "threshold": 0.95
        }]
    }
]

