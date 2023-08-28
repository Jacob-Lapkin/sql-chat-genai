from langchain.llms import VertexAI, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.vertexai import VertexAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import google.auth
from .bigquery import query_bigquery_sql, get_table_schema, get_example_row
import sys
from ..templates.prompt_templates import prompt_templates
from ..templates.query_templates import data_templates
from dotenv import load_dotenv
import json


# defining custom error class
class SqlInsightsError(Exception):
    pass


import os

# load openai api key from env files if not set on machine. set env variables as OPENAI_API_KEY.
load_dotenv()

# Get your google cloud credentials. Set up with Gcloud if needed
credentials, project_id = google.auth.default()

# setting project for google bigquery
projectid = project_id

# deprecated/old class without embeddings



class Sqlinsights:
    """
    A class used to generate insights from specific BigQuery datatable contexts 
    using the Langchain and VertexAI models.
    """
    
    def __init__(self, project, dataset, table, question, code_temp=.1,text_temp=.2, user_role='no specific role', model='vertex'):
        self.project = project
        self.dataset = dataset
        self.table = table
        self.question = question
        self._sql = None
        self._sql_result = None
        self.code_temp = code_temp
        self.text_temp = text_temp
        self.user_role = user_role
        self.model = model
    def sql_getter(self):
        return self._sql
    
    def sql_result_getter(self):
        return self._sql_result 
    
    def formulate_prompt(self):
        template = """
                Given the following project_id: {project},
                the following dataset: {dataset},
                the following table name: {table},
                the following BigQuery table schema: 
                {table_schema}
                the following example row from the table: 
                {example_row}
                

                Generate a Bigquery SQL query for the task provided below. Ensure the following criteria are met:
                1. Include the project ID and dataset in the query.
                2. Maintain and ensure consistent capitalization as provided in the schema.
                3. Use Lower for all columns that are string data types.
                4. Write sql with spelling that you think is correct if input from the user is believed to be slightly incorrect. Use your best judgement to fix 
                spelling errors that are entered from the user!
                5. MOST IMPORTANTLY, ONLY RETURN THE RESPONSE WITH THE SQL CODE. DO NOT RESPONSE WITH ANY INTRODUCTORY TEXT OR ACKNOWLEDGE THE QUESTION AT ALL.
                    DO NOT INCLUDE ANY ESCAPE CHARACTERS OR ANYTHING NOT RELEVANT TO THE EXACT BIGQUERY SQL CODE

                Task: {question}
                """

        prompt_temmplate = PromptTemplate(template=template, input_variables=[
                                        "project", "dataset", "table", "table_schema", 'question', 'example_row'])
        self.prompt_template = prompt_temmplate
        return prompt_temmplate

    def formulate_query(self):
        # save question
        table_schema = get_table_schema(self.project, self.dataset, self.table)
        prompt = self.formulate_prompt()


        llm_model = VertexAI(project=projectid, model_name='code-bison',
                            temperature=self.code_temp, max_output_tokens=1000)
        if self.model == 'openai':
            llm_model = ChatOpenAI(model_name='gpt-3.5-turbo',
                            temperature=self.code_temp)
        llm_chain = LLMChain(prompt=prompt, llm=llm_model, verbose=False)

        # get an example row for the prompt
        example_row = get_example_row(self.project, self.dataset, self.table)
        # return result and clean as you wish
        result = llm_chain.run({'project': self.project, 'dataset': self.dataset, 'table': self.table,
                            'table_schema': table_schema, "question": self.question, "example_row": example_row})
        cleaned_result = result.replace("sql", "").strip('```')

        # save sql statement
        self._sql = cleaned_result

        return cleaned_result
    
    def generate_query_result(self):
        query = self.formulate_query()

        bigquery_result = query_bigquery_sql(query)

        # save sql result
        self._sql_result = bigquery_result


        return bigquery_result

    def interpret_results(self):
        query_results = self.generate_query_result()
        template = """
                    Given the following question to to help generate sql code on a table: {question},
                    The following SQL that was generated: {sql}
                    The results obtained from the SQL statement that was generated: {sql_result}
                    The company role of the user that prompted the question: {user_role}
                    
                    Interpret the results and give a response that is phrased relevant to the user role. The response should be
                    descriptive and includes all of the data that is in the sql results. Do not forget any data. All data is important so include data from each and every 
                    column in the sql result. Do not return the actual sql result. Just interpret the data and return all qualitative and 
                    quantitative values in the result. 
                    """
        prompt_template = PromptTemplate(template=template, input_variables=[
                                        "question", "sql", "sql_result", "user_role"])

        llm_model = VertexAI(project=projectid, model_name='text-bison',
                            temperature=self.text_temp, max_output_tokens=1000)

        llm_chain = LLMChain(prompt=prompt_template,
                            llm=llm_model, verbose=False)
        result = llm_chain.run(
            {'question': self.question, 'sql': self._sql, 'sql_result': str(self._sql_result), 'user_role':self.user_role})
        response_dic = {
        "result":result,
        "query":str(self._sql)
    }
        return response_dic

    def get_insights(self):
        try:
            response = self.interpret_results()
            return response
        except SqlInsightsError as e:
            return {"error": str(e)}


class Visualinsights(Sqlinsights):
    def __init__(self, project, dataset, table, question, code_temp, text_temp, user_role, model):
        super().__init__(project, dataset, table, question, code_temp, text_temp, user_role, model)
    
    
    def generate_visual(self):
        try:
            base_response = super().get_insights()
            json_string = None
            result = self._sql_result
            if self._sql_result is not None:
                json_string = result.to_json(orient='records')

            base_response['data'] = json_string
            return base_response
        except Exception as e:
            raise SqlInsightsError(f"Error in generate_visual: {str(e)}")
    def get_visual(self):
        try:
            response = self.generate_visual()
            return response
        except SqlInsightsError as e:
            return {"error":str(e)}