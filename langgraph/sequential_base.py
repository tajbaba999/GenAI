import os
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
#Sequential workflow of the project

# Let's create the state first

class Pipelinestate(TypedDict):
    raw_input : str
    edited_text : str
    script_text : str
    final_output : str

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

llm.with_structured_output

def editor_node(state : Pipelinestate) -> dict:
    """Stage 1: Cleans up grammer, removes typos, and redfines the tone."""
    # print("\n--- [Stage 2] Executing Editor Node ---")

    prompt = (
        "You are an expert copyeditor. Clean up the following raw text. "
        "Fix any grammatical errors, spelling mistakes, and smooth out the transition flow "
        "while keeping the core message intact. Return only the edited text.\n\n"
        f"Text:\n{state['raw_input']}"
    )

    response = llm.invoke(prompt)
    return {"edited_text" : response.content.strip()}

def scriptwriter_node(state: Pipelinestate) -> dict:
     """Stage 2: Formats the clean text into an engaging video script style."""
    #  print("\n--- [Stage 2] Executing Scriptwriter Node ---")

     prompt = (
         "You are a charismatic YouTube content creator. Take this edited text and transform "
        "it into a highly engaging, punchy, conversational video script hook. Make it sound "
        "like a real person speaking passionately. Return only the script content.\n\n"
        f"Edited Text:\n{state['edited_text']}"
     )

     response = llm.invoke(prompt)
     return {"script_text" : response.content.strip()}

def translator_node(state: Pipelinestate) -> dict:
    """Stage 3: Translates the script into natural flowing Hinglish."""
    # print("\n--- [Stage 3] Executing Hinglish Translator Node ---")

    prompt = (
        "You are an expert content localizer for the Indian market. Take the following script "
        "and convert it into natural, flowing 'Hinglish'. Do not simply translate it sentence-by-sentence "
        "or repeat information. Alternating comfortably between Hindi and English phrases just like "
        "an intellectual tech educator would speak naturally on a live stream. Keep the energy high! "
        "Return only the final Hinglish text.\n\n"
        f"Script:\n{state['script_text']}"
    )

    response = llm.invoke(prompt)
    return {"final_output" : response.content.strip()}

#now your state and nodes are ready and now it is time to create the graph 
#and for creating the graph you have to connect tese nodes and for that you have 
#to use the edges 
#edges are very important to create the workflows 


from langgraph.graph import StateGraph, START, END

#create th graph
graph = StateGraph(Pipelinestate)

# add the nodes in graph 
graph.add_node("editor",  editor_node)
graph.add_node("scriptwriter", scriptwriter_node)
graph.add_node("translator", translator_node)


#Add edges (sequential - one after another)

graph.add_edge(START, "editor")
graph.add_edge("editor", "scriptwriter")
graph.add_edge("scriptwriter", "translator")
graph.add_edge("translator", END)

#compile the graph
app = graph.compile()

result = app.invoke({
    "raw_input" : "AI agents are the future of tech. They can think, plan, and act on their own. LangGraph helps you build these agents with proper control and memory."
})

#ouput
# print("Your result : - \n\n")
# print(result['final_output'])

from pprint import pprint

initial_state = {
    "raw_input": (
        "AI agents are the future of tech. "
        "They can think, plan, and act on their own. "
        "LangGraph helps you build these agents with proper control and memory."
    )
}

print("\n========= STREAMING STATE =========\n")

final_state = None

for step, state in enumerate(app.stream(initial_state, stream_mode="values"), start=1):
    print(f"\n{'='*50}")
    print(f"STEP {step}")
    print(f"{'='*50}")

    pprint(state)

    final_state = state

print("\n========= FINAL OUTPUT =========\n")
print(final_state["final_output"])    

