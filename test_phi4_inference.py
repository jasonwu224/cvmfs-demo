'''
Credit to microsoft for the original script which I abridged 
The original script can be downloaded using
curl https://raw.githubusercontent.com/microsoft/onnxruntime-genai/main/examples/python/phi3-qa.py -o phi3-qa.py
'''

import onnxruntime_genai as og
import time

def main():
    '''Running phi-4 mini on cpu. Please don't run it on cpu, it's so slow.'''

    start_time = time.time()  # record load time

    path = "/cvmfs/repo.jasonwu.org/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4"
    # path = "/Users/jasonwu/Downloads/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4"
    config = og.Config(path)
    config.clear_providers()
    model = og.Model(config)

    model_load_time = time.time() - start_time

    print("Model loaded")
    print(model_load_time)
    
    # tokenizer = og.Tokenizer(model)
    # tokenizer_stream = tokenizer.create_stream()
    # print("Tokenizer created")
    # print()
    # # can set options like temperature and top_k
    # search_options = {
    #     'max_length': 2048,
    # }
    
    # # Set the max length to something sensible by default, unless it is specified by the user,
    # # since otherwise it will be set to the entire context length
    # if 'max_length' not in search_options:
    #     search_options['max_length'] = 2048

    # chat_template = '<|user|>\n{input} <|end|>\n<|assistant|>'

    # params = og.GeneratorParams(model)
    # params.set_search_options(**search_options)
    # generator = og.Generator(model, params)

    # # Rather than use a loop, we will do just one response

    # prompt = "Please explain how CVMFS works"
    # print(f"Input: {prompt}")
    # prompt = f'{chat_template.format(input=prompt)}'

    # started_timestamp = time.time()  # record response time

    # input_tokens = tokenizer.encode(prompt)
    # generator.append_tokens(input_tokens)
    # print("Generator created")

    # print("Running generation loop ...")

    # first = True
    # new_tokens = []

    # print()
    # print("Output: ", end='', flush=True)

    # try:
    #     while not generator.is_done():
    #         generator.generate_next_token()
    #         if first:
    #             first_token_timestamp = time.time()
    #             first = False

    #         new_token = generator.get_next_tokens()[0]
    #         print(tokenizer_stream.decode(new_token), end='', flush=True)
    #         new_tokens.append(new_token)
    # except KeyboardInterrupt:
    #     print("  --control+c pressed, aborting generation--")
    
    # print("\n")
    
    # prompt_time = first_token_timestamp - started_timestamp
    # run_time = time.time() - first_token_timestamp
    # print(f"Summary\nLoad time: {model_load_time:.2f}s")
    # print(f"Prompt length: {len(input_tokens)} tokens\nNew tokens: {len(new_tokens)} tokens\nTime to first: {(prompt_time):.2f}s\nPrompt tokens per second: {len(input_tokens)/prompt_time:.2f} tps\nNew tokens per second: {len(new_tokens)/run_time:.2f} tps")

if __name__ == "__main__":
    main()
