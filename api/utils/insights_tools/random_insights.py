from langchain.llms import VertexAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.vertexai import VertexAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import google.auth
from .bigquery import query_bigquery, query_bigquery_w_wc, query_bigquery_sql, get_table_schema, get_example_row
import sys
from ..templates.prompt_templates import prompt_templates
from ..templates.query_templates import data_templates
from dotenv import load_dotenv


import os

# load openai api key from env files if not set on machine. set env variables as OPENAI_API_KEY.
load_dotenv()

# Get your google cloud credentials. Set up with Gcloud if needed
credentials, project_id = google.auth.default()

# setting project for google bigquery
projectid = project_id

# deprecated/old class without embeddings


class GenInsights:
    """ custom class to generate insights for Ingram Micro using lllm and langhchain

    Attributes:
        project : this is the google project that you have set - do not need to set default project
        prompt (string) : this is the prompt that you would like to feed into the llm
        data (list) : this is the data returned from the bigquery query
    """

    def __init__(self, project, prompt, data):
        self.project = project
        self.prompt = prompt
        self.data = query_bigquery_w_wc(data)

    def vectorize(self):
        # optional progress update
        print('generating embeddings and vectorstore...')
        print("-"*30)

        # chunk up the result returned from the query
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(str(self.data))
        if not chunks:
            return "Error: No chunks found."

        # text embeddings
        embeddings = VertexAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

        # optional progress update
        print('finalized vectorstore')
        print("-"*30)

        return VectorStore

    def generate_insights(self, platform='vertex', model='text-bison', temp=0.5):
        """generate the insights (or just answer if using generic prompt over dataset).
        Args:
            patform (string): llmn platform you are using.
            model (string): specific model from the platform.

        Returns:
            (string): result of your prompt over the dataset from the query.

        """
        VectorStore = self.vectorize()
        try:
            # optional progress update
            print('generating insights...')
            print("-"*30)

            if not VectorStore:
                return 'Error'
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True)

            # Set platform and model (Vertex or OpenAI)
            if platform == 'vertex':
                llm_model = VertexAI(
                    project=self.project, model_name=model, temperature=temp, max_output_tokens=1000)
            elif platform == 'openai':
                llm_model = ChatOpenAI(model_name=model, temperature=temp)
            insights_qa = ConversationalRetrievalChain.from_llm(
                llm_model,
                VectorStore.as_retriever(),
                memory=memory,
            )

            # return result and clean as you wish
            result = insights_qa({"question": str(self.prompt)})
            answer = result["answer"]
            cleaned_answer = answer.replace("*", " ")
            return cleaned_answer

        except Exception as e:
            return str(e)


# instantiate your result object and set the prompt and data
instance_prompt = prompt_templates['order_prompts'][0]['order_prompt_one']
instance_data = data_templates['order_data'][0]['order_one']

# instantiate insights object
# insights_gen = GenInsights(project=project_id, prompt=instance_prompt, data=instance_data)

# call insights with vertex ai
# print(insights_gen.generate_insights(temp=0.9, model='text-bison'))

