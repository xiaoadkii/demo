from langchain_core.messages import HumanMessage
from typing import Dict, TypedDict, Optional
from langgraph.graph import START,END, StateGraph
from langgraph.config import get_stream_writer
from dotenv import load_dotenv
from langchain_qwq import ChatQwQ
from langfuse.langchain import CallbackHandler
import random

class State(TypedDict):
    user_prompt:str
    node_data: Optional[Dict[str, str]]

def node1(state: State):

    writer = get_stream_writer()
    writer(("key1", 'value'))
    state['user_prompt'] = state['user_prompt']  + 'node1'
    return state


def router(state: State):
    val = random.randint(1, 10)
    return 'node3' if val > 5 else 'node2'


def node2(state: State):

    model = ChatQwQ()

    messages = [
        HumanMessage(state.get('user_prompt', 'nihao'))
    ]

    model.invoke(messages)
    state['user_prompt'] = state['user_prompt']  + 'node2'
    return state

def node3(state: State):
    state['user_prompt'] = state['user_prompt']  + 'node3'
    return state

def create_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node('node1', node1)
    graph_builder.add_conditional_edges('node1', router, {
        "node3": 'node3',
        'node2': 'node2'
    })
    graph_builder.add_node('node2', node2)
    graph_builder.add_node('node3', node3)
    
    graph_builder.add_edge(START, 'node1')
    graph_builder.add_edge('node1', 'node2')
    graph_builder.add_edge('node2', END)
    graph_builder.add_edge('node3', END)

    graph = graph_builder.compile()
    return graph

langgraph_graph = create_graph()


if __name__ == '__main__':
    load_dotenv('./.env')
    graph = create_graph()
    main_content = ''
    langfuse_handler = CallbackHandler()
    config={"callbacks": [langfuse_handler]}

    for msg_type, chunk in graph.stream({"user_prompt":"Nihao"}, stream_mode=['updates', 'messages', 'custom'], config=config):
        if msg_type == 'messages':
            if chunk[0].content != '':
                print(chunk[0].content)
                main_content = main_content + chunk[0].content
        if msg_type == 'updates':
            print(chunk)
        
    print(main_content)