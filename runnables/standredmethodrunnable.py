from langchain_core.runnables import RunnableLambda

import random

def add_one(x : int) -> int:
    return x + 1

def bubby_double(y: int) -> int:
    """Buggy code that will fail 70% of the time"""
    if random.random() > 0.3:
        print('This code failed, and will probably be retried!')
        raise ValueError('Triggered buggy code')
    return y * 2


sequene = (
    RunnableLambda(add_one) |
    RunnableLambda(bubby_double).with_retry(
        stop_after_attempt=10,
        wait_exponential_jitter=False
    )
)

print(sequene.input_schema.model_json_schema())
print(sequene.output_schema.model_json_schema())
print(sequene.invoke(2))