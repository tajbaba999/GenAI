from langchain.tools import tool

@tool  #decorator for creating tool 
def get_greeting(name : str) -> str: #type hints
    """Generate a greeting message to user""" #docstring
    return f"Hello {name}, from get_greeting tools"

result = get_greeting.invoke({"name" : "Taj"})
print(result)

print("Greeting")

print("Name : ",get_greeting.name)
print("Description : ",get_greeting.description)
print( "Args : ",get_greeting.args)