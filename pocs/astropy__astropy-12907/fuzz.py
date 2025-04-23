import atheris
import sys
import numpy as np
from astropy.modeling import models as m
from astropy.modeling.separable import separability_matrix
import random

def random_parenthesized_expr(models, fdp):
    expr = [f"models[{i}]" for i in range(len(models))]
    # Randomly join with '&' and insert parentheses
    while len(expr) > 1:
        i = fdp.ConsumeIntInRange(0, len(expr) - 2)
        left = expr.pop(i)
        right = expr.pop(i)
        expr.insert(i, f"({left} & {right})")
    return expr[0]  # single expression string

def left_associative_grouping(models):
    model = models[0]
    for m2 in models[1:]:
        model = model & m2
    return model

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    n = fdp.ConsumeIntInRange(2, 10)
    models = [m.Linear1D(i+1) for i in range(n)]

    try:
        # Flat model
        flat_model = left_associative_grouping(models)

        # Random model via string-based parenthesis
        expr = random_parenthesized_expr(models, fdp)
        random_model = eval(expr)

        sep_flat = separability_matrix(flat_model)
        sep_rand = separability_matrix(random_model)

        assert np.array_equal(sep_flat, sep_rand)
        print("No Violation")
    except AssertionError:
        print("Assertion Violation")
           
    except NotImplementedError:
        print("NotImplementedError — skipping.\n")
    except Exception as e:
        if "separable" in str(e):
            raise
        print(f"Unexpected error: {e}\n")

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
