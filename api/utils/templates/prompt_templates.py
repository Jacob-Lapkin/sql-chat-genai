
product_prompt = """
As a wizard in data analytics, your task is to extract 10 valuable statistical insights from the provided datatable.
The insights should be expressed in a lively and engaging tone, ensuring that each one is distinct and rich in quantitative detail.
Aim to weave in various elements from the datatable headers in your response.
Crucially, initiate every insight with a different phrase for variety.
Please remember to return 10 insights. Do not forget anything please!
Please avoid incorporating any text or data that isn't derived directly from the datatable.
"""


product_prompt_two = """
As a wizard in data analytics, your task is to extract 10 valuable statistical insights from the provided product catalog dataset.
The insights should be expressed in a lively and engaging tone, ensuring that each one is distinct and rich in quantitative detail.
Aim to weave in various elements from the datatable headers in your response.
DO NOT write insighst about data that is not in the dataset
Crucially, initiate every insight with a different phrase for variety.
Please write various insights for different products if they exist.
The insights do not only have to be about the product descriptions.
Do not create insights that are about prices.
In fact, avoid incorporating any text or data that isn't derived directly from the datatable.
"""

order_history = """
As a wizard in data analytics, your task is to extract 10 valuable statistical insights from the provided datatable for the customer EASTECH SYSTEMS LTD.
Each insight should be tailored as if you are engaging directly with the customer in a conversation.
The insights should be expressed in a lively and engaging tone, ensuring that each one is distinct and rich in quantitative detail.
Aim to weave in various elements from the datatable headers in your response.
Crucially, initiate every insight with a different phrase for variety.
Please avoid incorporating any text or data that isn't derived directly from the datatable.
"""

# feel free to add your data_queries here
prompt_templates = {
    'order_prompts': [
        {"order_prompt_one": order_history}
    ],
    'product_prompts': [
        {"product_prompt_one": product_prompt},
        {"product_prompt_two": product_prompt}
    ]
}
