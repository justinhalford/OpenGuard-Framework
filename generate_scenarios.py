import openai
from tqdm import tqdm
import time
import os
import random

openai.api_key = '<OPEN AI API KEY>'

def generate_scenarios(domain, number_of_scenarios):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate {number_of_scenarios} detailed scenarios of {domain}"\
             "that demonstrate varying degrees of presented hazard, risk, or harms and which comprehensively"\
              "and robustly cover as large a swath of {domain} as precisely and universally as possible.\n\n"\
              "Here is an example scenarios for the domain of cybersecurity: A group of hackers successfully launches a ransomware attack on a major hospital's IT systems,"\
              "encrypting patient records and demanding a significant ransom, thereby disrupting medical services and putting patients at risk."\
              "Input Format: String ({domain})\nOutput Format: Provide the output as a list of comma-separated strings."}
        ],
        max_tokens=number_of_scenarios * 50
    )
    return response.choices[0].message.content.strip().split(',')

def save_to_file(directory, domain, scenarios_list):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{domain.replace(' ', '_')}_scenarios.txt")
    
    with open(file_path, 'w') as file:
        for scenario in scenarios_list:
            file.write(scenario.strip() + '\n')

def read_domains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_domains(file_path, number_of_scenarios_per_domain, done_file):
    domains = read_domains(file_path)
    random.shuffle(domains)
    for domain in tqdm(domains, desc="Generating scenarios"):
        scenarios = generate_scenarios(domain, number_of_scenarios_per_domain)
        save_to_file('scenarios', domain, scenarios)
        with open(done_file, 'a') as f:
            f.write(domain + '\n')
        time.sleep(15)

process_domains('domains.txt', 50, 'domains_done.txt')