import openai
import os

openai.api_key = '<OPEN AI API KEY>'

def generate_domains(number_of_domains):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Generate a set of {number_of_domains} domains of risk "\
        "for which a language model could be misused to directly or indirectly generate hazards. "\
        "These domains should be high level.\n\nOutput Format: Provide the output as a list of comma-separated values."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        max_tokens=number_of_domains * 10
    )

    domains_list = response.choices[0].message.content.strip().split(',')
    domains_list = [domain.strip() for domain in domains_list if domain.strip()]
    return domains_list

def save_to_file(filename, domains_list):
    if os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        filename = f"{base}_{i}{ext}"

    with open(filename, 'w') as file:
        for domain in domains_list:
            file.write(domain + '\n')

domains = generate_domains(100)
save_to_file('domains.txt', domains)
