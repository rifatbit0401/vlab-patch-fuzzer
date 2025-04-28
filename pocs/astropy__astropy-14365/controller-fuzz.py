import atheris
import sys
import random
import json
from io import StringIO
from astropy.io import ascii


def mutate_case(word):
    return ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in word)


def random_word(fdp, min_len=3, max_len=7):
    length = fdp.ConsumeIntInRange(min_len, max_len)
    return fdp.ConsumeUnicodeNoSurrogates(length).replace('\n', '').replace(' ', '')[:max_len]


VALID_ERROR_TYPES = ["READ", "SERR", "TERRA", "AERR", "TERR", "NONE"]

def mutate_from_seed(fdp, seed_words):
    base = fdp.PickValueInList(seed_words)
    mutated = list(base)

    # Mutate some characters randomly
    for i in range(len(mutated)):
        if fdp.ConsumeBool():
            mutated[i] = chr(fdp.ConsumeIntInRange(65, 90))  # Uppercase ASCII

    # Optionally delete or insert a character
    if fdp.ConsumeBool() and len(mutated) > 2:
        del mutated[fdp.ConsumeIntInRange(0, len(mutated)-1)]
    if fdp.ConsumeBool():
        mutated.insert(fdp.ConsumeIntInRange(0, len(mutated)), chr(fdp.ConsumeIntInRange(65, 90)))

    return ''.join(mutated)


def generate_fully_fuzzed_command_line(fdp):
    word1 = mutate_case(mutate_from_seed(fdp, VALID_ERROR_TYPES))  # Freeform command prefix
    word2 = mutate_case(mutate_from_seed(fdp, VALID_ERROR_TYPES))  # Seeded mutation
    col1 = str(fdp.ConsumeIntInRange(1, 5))
    col2 = str(fdp.ConsumeIntInRange(1, 5))
    return f"{word1} {word2} {col1} {col2}"


def generate_valid_qdp_rows(fdp):
    tokens = []
    for _ in range(50):
        val = fdp.ConsumeFloat()
        tokens.append(f"{val:.2f}")
    rows = []
    for i in range(0, len(tokens) - 4, 5):  # 5 columns: X Y1 Y1_err Y2 Y2_err
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
        result["input"] = qdp_content

        output = ascii.read(qdp_content, format="qdp")

        result["output"] = "\n".join(output.pformat())
        result["exception"] = 0

        print("=== QDP INPUT ===")
        print(qdp_content)
        print("=== PARSED TABLE ===")
        print(output)

    except Exception as e:
        result["exception"] = 1
        result["error"] = str(e)
        print("exception")
    with open("results.jsonl", "a") as f:
        f.write(json.dumps(result) + "\n")


def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
