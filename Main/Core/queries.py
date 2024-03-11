from Main.Core.apis import DataHub, TOPICS
import streamlit as st
from openai import OpenAI

from Main.assets.TextInformation import AV_overview

client = OpenAI(
    # This is the default and can be omitted
    api_key=st.session_state.get("OPENAI_API_KEY"),
)

@st.cache_data(show_spinner=False)
def init_chatbot():
    return Chatbot()


class Chatbot:
    def __init__(self):
        self.datahub = DataHub()

    def topic_identifier(self, Query):
        """
        get query and return all relevant topics to extract data from
        :param Query:
        :return:
        """
        messages = [
            {"role": "system",
             "content": "You are a topic Identifier, You will be given a query and you'll return a list of topics we need to query to answer that query."
                        f"pick from the following topics: {TOPICS.keys()}, this is their description: {TOPICS}  "
             },
            {"role": "user", "content": "How many people entered today from the front gate?"},
            {"role": "assistant", "content": "people_count, gates"},
            {"role": "user", "content": f"question: {Query}"}
        ]
        # f"some key topics to cover are {topics.keys()} described as follows {topics}."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0,
        )
        answer = ""
        for choice in response.choices:
            answer += choice.message.content

        return answer.split(',')

    def query(self, Query: str):
        """
        get query, check if data required, return answer
        :param Query: str
        :return: str
        """
        # run identifier
        Topics = self.topic_identifier(Query)
        data = []
        if len(Topics) > 0:
            data = self.datahub.getData(Query, Topics)
        # answer the following question using the following data
        messages = [
            {"role": "system",
             "content": "Create a final answer to the given questions using the provided document excerpts(in no particular order) as references. \n"
                        f"The website explains Azkavision as follows: {AV_overview} \n"
                        f"These are data extracted from the the backend that is deemed useful to answering the question: {data}"
             },
            {"role": "user", "content": f"question: {Query}"}
        ]
        # f"some key topics to cover are {topics.keys()} described as follows {topics}."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        answer = ""
        for choice in response.choices:
            answer += choice.message.content
        answer = ""

        return answer
