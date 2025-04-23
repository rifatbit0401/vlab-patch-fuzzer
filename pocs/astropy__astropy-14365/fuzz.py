import atheris
import sys
import random
from io import StringIO
from astropy.io import ascii
import json


def mutate_case(word):
    return ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in word)


def random_word(fdp, min_len=3, max_len=7):
    length = fdp.ConsumeIntInRange(min_len, max_len)
    return fdp.ConsumeUnicodeNoSurrogates(length).replace('\n', '').replace(' ', '')[:max_len]


def generate_fully_fuzzed_command_line(fdp):
    word1 = random_word(fdp)
    word2 = random_word(fdp)
    col1 = str(fdp.ConsumeIntInRange(1, 5))
    col2 = str(fdp.ConsumeIntInRange(1, 5))
    return f"{mutate_case(word1)} {mutate_case(word2)} {col1} {col2}"


def generate_valid_qdp_rows(fdp):
    tokens = []
    for _ in range(50):  # Enough tokens to form 10 rows
        val = fdp.ConsumeFloat()
        tokens.append(f"{val:.2f}")
    rows = []
    for i in range(0, len(tokens) - 4, 5):  # 5 columns per row
        rows.append(" ".join(tokens[i:i+5]))
    return "\n".join(rows)


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    result = {}
    try:
        header_line = generate_fully_fuzzed_command_line(fdp)
        no_line = "NO NO NO NO"
        data_rows = generate_valid_qdp_rows(fdp)

        qdp_content = f"{header_line}\n{no_line}\n{data_rows}"
        # print("=== QDP INPUT ===")
        # print(qdp_content)
        result["input"] = qdp_content
        
        output = ascii.read(qdp_content, format="qdp")

        print("=== QDP INPUT ===")
        print(qdp_content)
        # result["input"] = qdp_content
        

        print("=== PARSED TABLE ===")
        print(output)
        result["output"] = "\n".join(output.pformat())
        result["exception"] = 0

    except Exception as e:
        result["exception"] = 1
    
    with open("results.jsonl","a") as f:
        f.write(json.dumps(result)+"\n");    


def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()

