NUM_OF_STEPS = 5

REPORT_TEMPLATE = """Report

We have made {total} observations from tossing a coin: {tails} of them were tails and {heads} of
them were heads. The probabilities are {tails_percentage:.2f}% and {heads_percentage:.2f}%, respectively. Our
forecast is that in the next {steps} observations we will have: {predicted_tails} tail and {predicted_heads} heads."""