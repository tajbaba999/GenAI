from langchain_core.runnables import RunnableLambda, RunnableParallel

sequence = RunnableLambda(lambda x: x +1) | RunnableLambda(lambda x: x * 2)

result1 = sequence.invoke(1)
print(result1)

result2 = sequence.batch([4, 5, 6])
print(result2)

parallel = RunnableParallel(
    mul_2=RunnableLambda(lambda x: x * 2),
    mul_5=RunnableLambda(lambda x: x * 5)
)

result = parallel.invoke(1)

print(f"Parallel runnable with one sequence {result}")
