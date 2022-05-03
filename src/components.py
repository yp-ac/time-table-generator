import streamlit as st
from typing import Callable, Iterable
from utils import *


def get_input(placeholders: List[str], on_click_processor: Callable, key=None):
    cols = st.columns([*(len(placeholders) * [2]), 1])

    outputs = [None] * len(placeholders)

    cols[-1].write("\n\n")
    for idx, placeholder in enumerate(placeholders):
        outputs[idx] = cols[idx].text_input("", placeholder=placeholder, key=f"{key}{idx}")

    if cols[-1].button("Add", key=key):
        print(f"adding {outputs}")
        on_click_processor(outputs)


def display_list_with_input_options(values: Iterable, inputs: Iterable, processor: Callable, to_string: Callable = str, key=None):
    container = st.empty()

    get_input(inputs, processor, key=key)

    with container.container():
        for value in values:
            to_string(value)

