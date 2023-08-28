swagger_config = {
    "headers": [],
    "specs": [
        {
            "version": "1.1.0",
            "title": "I&R Generative AI Chat Insights API",
            "description": """This API harnesses the power of generative AI to create unique insights for Ingram Micro. It leverages advanced techniques in both code and text generation. Users supply a project, dataset, table, and question to the API. 
                              Our generative models then construct and execute SQL queries on the given dataset. This data is interpreted and transformed into clear, human-readable insights. Whether you're trying to find patterns in your data or make predictions for the future, our API can help you get the insights you need.""",
            "endpoint": 'v1',
            "route": '/v1/docs.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "swagger_ui": True,
    "static_url_path": "/flasgger_static",
    "swagger_ui_bundle_js": "/flasgger_static/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "/flasgger_static/swagger-ui-standalone-preset.js",
}


insights_doc = {
    "tags": ["Insights"],
    "description": "Runs a SQL query on the provided project, dataset, and table",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "Insights",
                "required": ["project", "dataset", "table", "input"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "The name of the project"
                    },
                    "dataset": {
                        "type": "string",
                        "description": "The name of the dataset"
                    },
                    "table": {
                        "type": "string",
                        "description": "The name of the table"
                    },
                    "input": {
                        "type": "string",
                        "description": "The question to be asked about the data"
                    },
                    "query": {
                        "type": "boolean",
                        "description": "Show the executed SQL query in the response",
                        "default": False
                    },
                    "codeTemp": {
                        "type": "number",
                        "description": "Code temperature parameter",
                        "default": 0.1
                    },
                    "textTempt": {
                        "type": "number",
                        "description": "Text temperature parameter",
                        "default": 0.3
                    },
                    "userRole": {
                        "type": "string",
                        "description": "The user role that is asking the question on the data parameter",
                        "default": "no specific role"
                    },
                    "model": {
                        "type": "string",
                        "description": "The large language model platform what will be used",
                        "default": "vertex"
                    }, 
                    "visualData": {
                        "type": "boolean",
                        "description": "Whether to attempt to generate results for visual data",
                        "default": False
                    }
                },
                "example": {
                    "project": "imgcp-20220315135638",
                    "dataset": "ChatPOC",
                    "table": "Sales",
                    "input": "Give me the top 5 products ranked by the total number of orders",
                    "query": True,
                    "codeTemp": 0.1,
                    "textTempt": 0.3,
                    "userRole": "Sales Associate",
                    "model": "vertex", 
                    "visualData":True
                }
            }
        },
        {
            "name": "IM-SenderID",
            "in": "header",
            "required": True,
            "type": "string",
            "description": "The Sender ID header", 
            "example": "IMAEP",
            "default": "IMAEP"

        },
        {
            "name": "IM-MicroFrontendID",
            "in": "header",
            "required": True,
            "type": "string",
            "description": "The MicroFrontend ID header",
            "example": "MF123", 
            "default": "MF123"
        },
        {
            "name": "IM-CorrelationID",
            "in": "header",
            "required": True,
            "type": "string",
            "description": "The Correlation ID header", 
            "example": "M123", 
            "default": "M123"
        },
        {
            "name": "IM-SiteCode",
            "in": "header",
            "required": True,
            "type": "string",
            "description": "The Site Code header",
            "example": "M123", 
            "default": "M123"
        },
        {
            "name": "IM-UserID",
            "in": "header",
            "required": True,
            "type": "string",
            "description": "The User ID header",
            "example": "{ee67fa14-19e8-4858-b31c-bd86c3d0380d}", 
            "default": "{ee67fa14-19e8-4858-b31c-bd86c3d0380d}"
        }
    ],
    "responses": {
        "200": {
            "description": "The query was successful",
            "schema": {
                "id": "Resp",
                "properties": {
                    "response": {
                        "type": "object",
                        "properties": {
                            "result": {
                                "type": "object",
                                "description": "The result of the query"
                            },
                            "query": {
                                "type": "string",
                                "description": "The executed SQL query"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Bad Request - Required parameters are missing or an error occurred while generating insights",
            "schema": {
                "id": "ErrorResp",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message describing the issue"
                    },
                    "query": {
                        "type": "string",
                        "description": "The executed SQL query (if available)"
                    }
                }
            }
        },
        "500": {
            "description": "An error occurred while executing the query"
        }
    }
}


# Add the new route's documentation to the existing insights_doc
schema_doc = {
    "tags": ["Insights"],
    "description": "Get the schema of a BigQuery table",
    "parameters": [
        {
            "name": "project",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "The name of the project"
        },
        {
            "name": "dataset",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "The name of the dataset"
        },
        {
            "name": "table",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "The name of the table"
        }
    ],
    "responses": {
        "200": {
            "description": "The schema was retrieved successfully",
            "schema": {
                "id": "SchemaResp",
                "properties": {
                    "response": {
                        "type": "object",
                        "properties": {
                            "column 0": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the column"
                                    },
                                    "field_type": {
                                        "type": "string",
                                        "description": "The field type of the column"
                                    },
                                    "mode": {
                                        "type": "string",
                                        "description": "The mode of the column"
                                    }
                                }
                            },
                            # Add more columns as needed based on the actual number of columns in the table
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Required parameters are missing"
        },
        "500": {
            "description": "An error occurred while retrieving the schema"
        }
    },
    "example": {
        "project": "imgcp-20220210133450",
        "dataset": "PIMCOREPROD",
        "table": "DESCRIPTION"
    }
}
