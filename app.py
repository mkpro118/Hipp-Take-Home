from flask import Flask, request, render_template
from flask_cors import CORS

import argparse
import os
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

api_key = os.environ.get('OpenAI_API_Key', None)

if api_key is None:
    raise EnvironmentError('OpenAI_API_Key environment variable is missing')

client = OpenAI(api_key=api_key)


def prompts():
    while True:
        yield lambda x, y, z: (
            f'Hello, I am looking for a new recipe to try.'
            f' I have the following ingredients: {x}.'
            f' I also have certain dietary preferences: {y}.'
            f' Can you suggest a recipe that can serve {z}?'
            f' I\'d appreciate if you could provide step-by-step instructions.'
        )

        yield lambda x, y, z: (
            f'Hello, I need your help in creating some recipes.'
            f' Here are the details: I have these specific ingredients at my disposal: {x}.'
            f' Furthermore, I have dietary preferences, {y} that need to be considered.'
            f' And finally, the recipes should be sufficient for {z}.'
            f'Can you prepare a custom recipe or even provide multiple recipes based on this input?'
        )


prompt_gen = prompts()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def gen_ideas():
    req = request.get_json()
    ingredients = req.get('ingredients')
    preferences = req.get('preferences')
    servings = req.get('servings')
    counts = int(req.get('counts') or 1)

    prompt = next(prompt_gen)(ingredients, preferences, servings)
    recipes = get_recipe(prompt, counts=counts)
    print(counts)
    return json.dumps(recipes)


def get_recipe(prompt, counts=1, model="gpt-4"):
    # Calling the ChatCompletion API
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        n=counts,
    )

    # Returning the extracted response
    return [choice.message.content for choice in response.choices]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVER_PORT', 5000))
    debug = bool(os.environ.get('FLASK_DEBUG', True))

    ps_host = os.environ.get('PROXYSERVER_HOST', 'localhost')
    ps_port = os.environ.get('PROXYSERVER_PORT', 8000)

    parser.add_argument('-fh', '--flask-hostname', type=str, default=host)
    parser.add_argument('-fp', '--flask-port', type=int, default=port)
    parser.add_argument('-fd', '--flask-debug',
                        action='store_true', default=debug)

    args = parser.parse_args()

    host = args.flask_hostname
    port = args.flask_port
    debug = args.flask_debug

    app.run(host=host, port=port, debug=debug)
