
from ..api.utils.insights_tools.sql_insights import Sqlinsights
from langchain.prompts import PromptTemplate

project = "imgcp-20220315135638"
dataset = "ChatPOC"
table = "Sales"
input = "how many products have anything to do with ram or cpu or any other important computer components in them?"
query = True
model = "vertex"

test_object = Sqlinsights(project=project, dataset=dataset, table=table, question=input, model=model)


def test_form_prompt():
    result = test_object.formulate_prompt()
    assert type(result) == PromptTemplate

def test_form_query():
    result = test_object.formulate_query()
    cloud_check = True
    if all(item in result for item in [project, dataset, table]):
        cloud_check  = True
    assert type(result) == str
    assert "select" in result.lower()
    assert cloud_check


