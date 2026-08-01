from langchain.tools import tool

@tool
def get_greeting(name : str) -> str:
    """Generate a greeting message to user"""
    return f"Hello {name}, from get_greeting tools"

result = get_greeting.invoke({"name" : "Taj"})
print(result)

print("Greeting")

print("Name : ",get_greeting.name)
print("Description : ",get_greeting.description)
print( "Args : ",get_greeting.args)