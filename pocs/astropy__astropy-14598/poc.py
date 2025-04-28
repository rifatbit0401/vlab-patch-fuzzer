from astropy.io import fits

for n in range(60, 80):
    value = "x" * n + "''"
    card = fits.Card('TESTKEY', value)

    card_str = str(card)
    reconstructed_card = fits.Card.fromstring(card_str)

    # Assert that original and reconstructed values are identical
    assert card.value == reconstructed_card.value, (
        f"Mismatch at length {n}!\n"
        f"Original:      {repr(card.value)}\n"
        f"Reconstructed: {repr(reconstructed_card.value)}\n"
        f"Card String:   {card_str}"
    )
