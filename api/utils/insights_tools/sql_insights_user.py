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



class Sqlinsightsuser:
    """
    A class used to generate insights from specific BigQuery datatable contexts 
    using the Langchain and VertexAI models.

    ...

    Attributes
    ----------
    project : str
        The project id for the BigQuery dataset
    dataset : str
        The dataset name within the BigQuery project
    table : str
        The table name within the BigQuery dataset
    question : str
        The question to be interpreted by the AI models
    sql : str
        The SQL query generated (default is None)
    sql_result : str
        The result from executing the SQL query (default is None)
    code_temp : float
        Temperature parameter for the 'code-bison' model (default is .1)
    text_temp : float
        Temperature parameter for the 'text-bison' model (default is .2)

    Methods
    -------
    formulate_prompt():
        Creates a prompt for the AI model based on the provided attributes

    formulate_query():
        Formulates the SQL query using AI models

    generate_query_result():
        Executes the SQL query and stores the result

    interpret_results():
        Interprets the results obtained from the SQL statement
    """
    
    def __init__(self, project, dataset, table, question, code_temp=.1,text_temp=.2, user_role='no specific role', customer=""):
        self.project = project
        self.dataset = dataset
        self.table = table
        self.question = question
        self.sql = None
        self.sql_result = None
        self.code_temp = code_temp
        self.text_temp = text_temp
        self.user_role = user_role
        self.customer = customer
    def formulate_prompt(self):

        template = """
                    Given the following project_id: {project},
                    the following dataset: {dataset},
                    the following table name: {table},
                    the following BigQuery table schema: 
                    {table_schema}
                    the following example row from the table: 
                    {example_row}
                    most importantly the current CustomerId in context:
                    {customer}
                    

                    Generate an SQL query for the task provided below. Ensure the following criteria are met:
                    1. Include the project ID and dataset in the query.
                    2. Maintain and ensure consistent capitalization as provided in the content.
                    3. All queries related to the customer should have a WHERE condition. 
                    4. Keep in mind that the CustomerId is a string and not an integer
                    5. If the question asks for data that is not coming from {customer} then do not generate sql code.
                    6. Write code that takes into account all possibilities of capitalization (use LOWER in neccessary WHERE clauses).
                    7. Write sql with spelling that you think is correct if input from the user is believed to be slightly incorrect. Use your best judgement to fix 
                    spelling errors that are entered from the user!

                    Task: {question}
                    """
        prompt_temmplate = PromptTemplate(template=template, input_variables=[
                                          "project", "dataset", "table", "table_schema", 'question', 'example_row', 'customer'])
        return prompt_temmplate

    def formulate_query(self):
        # save question
        table_schema = get_table_schema(self.project, self.dataset, self.table)
        prompt = self.formulate_prompt()


        llm_model = VertexAI(project=projectid, model_name='code-bison',
                             temperature=self.code_temp, max_output_tokens=1000)
        llm_chain = LLMChain(prompt=prompt, llm=llm_model, verbose=False)

        # get an example row for the prompt
        example_row = get_example_row(self.project, self.dataset, self.table)
        # return result and clean as you wish
        result = llm_chain.run({'project': self.project, 'dataset': self.dataset, 'table': self.table,
                               'table_schema': table_schema, "question": self.question, "example_row": example_row, "customer":self.customer})
        cleaned_result = result.replace("sql", "").strip('```')
        print(cleaned_result)
        # save sql statement
        self.sql = cleaned_result

        return cleaned_result

    def generate_query_result(self):
        query = self.formulate_query()

        bigquery_result = query_bigquery_sql(query)

        # save sql result
        self.sql_result = str(bigquery_result)
        print(bigquery_result)

        return bigquery_result

    def interpret_results(self):
        query_results = self.generate_query_result()
        template = """
                    Given the following question to to help generate sql code on a table: {question},
                    The following SQL that was generated: {sql}
                    The results obtained from the SQL statement that was generated: {sql_result}
                    The company role of the user that prompted the question: {user_role}
                    the customer that is the current context: {customer}
                    
                    Interpret the results and give a response that is phrased relevant to the user role. The response should be
                    descriptive and includes all of the data that is in the sql results. Do not forget any data. All data is important so include data from each and every 
                    column in the sql result. Do not return the actual sql result. Just interpret the data and return all qualitative and 
                    quantitative values in the result. Remember, this is a customer that asked the question. If the customer that is in context does not match the customer in the sql query,
                    then please do not give a response! You should respond in the second person as if you are always talking to the customer.
                    """
        prompt_template = PromptTemplate(template=template, input_variables=[
                                         "question", "sql", "sql_result", "user_role", "customer"])

        llm_model = VertexAI(project=projectid, model_name='text-bison',
                             temperature=self.text_temp, max_output_tokens=1000)

        llm_chain = LLMChain(prompt=prompt_template,
                             llm=llm_model, verbose=False)
        print('--'*30)
        print("interpreting results")
        print('--'*30)
        result = llm_chain.run(
            {'question': self.question,'sql': self.sql, 'sql_result': self.sql_result, 'user_role':self.user_role, 'customer': self.customer})
        
        print(result)

        response_dic = {
            "result":result,
            "query":self.sql
        }
        return response_dic
