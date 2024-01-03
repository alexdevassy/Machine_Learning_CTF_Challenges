import argparse
from langchain_experimental.pal_chain import PALChain
from langchain import OpenAI

parser = argparse.ArgumentParser(description="A simple script to accept user input via flags.")
# Add a command line argument for user input
parser.add_argument('--user_input', type=str, help='prompt')
parser.add_argument('--api_key', type=str, help='openai api key')
# Parse the command line arguments
args = parser.parse_args()
openaiapikey = args.api_key
llm = OpenAI(temperature=0, openai_api_key=openaiapikey)
pal_chain = PALChain.from_math_prompt(llm, verbose=True)

# Check if the 'user_input' flag is provided
try:
    if args.user_input:
        result = pal_chain.run(args.user_input)
        print(result)
        #print(f"User input: {args.user_input}")
    else:
        print("No user input provided.")
except Exception as e:
    print("Exception Occured")
