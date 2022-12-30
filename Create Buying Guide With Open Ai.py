import base64
import requests



def wph2(text):
    code = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
    return code

def wpara(text):
    code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return code

def ai_ans(prompt):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    import openai
    openai.api_key = os.getenv('API_KEY')
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    output = response.get('choices')[0].get('text')
    return output

keyword = input("Enter your Key: ")
prompt = f'write four questions about {keyword}'
content = wpara(ai_ans(f'write short intro about {keyword}').strip().strip('\n')) 
questions = ai_ans(prompt)
ques_list = questions.strip().split('\n')
endline = 'write a paragraph about it'


qs = {}
for qr in ques_list:
    commands = f'{qr} {endline}'
    answers = ai_ans(commands).strip().strip('\n')
    qs[qr] = answers


user = 'manik'
seckey = 'vzCG iG6C ewBN K2fF tSB4 eoca' 
credential = f'{user}:{seckey}'
token = base64.b64encode(credential.encode())
headers = {'Authorization': f'Basic {token.decode("utf-8")}'}


title = f'buying guide about {keyword}'

data = {
    'title': title.title(),
    'content' : content,
    'slug': keyword.replace(' ', '-')

}

for key, value in qs.items():
    ques = wph2(key)
    value = wpara(value)
    temp = ques+ value
    content += temp
    
print(content)


api_url = 'https://testsite.local/wp-json/wp/v2/posts'
r = requests.post(api_url, data = data, headers=headers, verify = False)
print(r.json())

