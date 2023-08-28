from flask import Blueprint, request, jsonify
from ..utils.insights_tools.sql_insights import Sqlinsights, Visualinsights
from ..utils.insights_tools.bigquery import get_table_schema
from flasgger import swag_from
from ..utils.misc.swagger_docs import insights_doc, schema_doc
from ..utils.decorators.header_dec import require_headers
import json
import logging


insights_bp = Blueprint('insights_bp', __name__)

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

@insights_bp.route('/query-insight/associate', methods=['POST'])
@swag_from(insights_doc)
@require_headers
def insights():
    try:
        # request data to json
        data = request.get_json()
        project = data.get('project', None)
        dataset = data.get('dataset', None)
        table = data.get('table', None)
        input_query = data.get('input', None)
        show_query = data.get("query", False)
        code_temp = data.get("codeTemp", 0.1)
        text_temp = data.get('textTempt', 0.3)
        user_role = data.get('userRole', "no specific role")
        model = data.get('model', 'vertex')
        visual_data = data.get('visualData', False)

        # check if all required arguments exist
        if None in [project, dataset, table, input_query]:
            logger.warning("Some required arguments are missing.")
            return jsonify({'error': "missing required arguments"}), 400
        
        # initialize insight
        query_object = Visualinsights(project, dataset, table, input_query, code_temp=code_temp , text_temp=text_temp, user_role=user_role, model=model)

        # determine correct method
        initial_response = None
        if visual_data == True:
            initial_response = query_object.get_visual()
        else: 
            initial_response = query_object.get_insights()

        result = initial_response.get('result')
        response = {"result": result}
        
        # Log processed insights
        logger.info(f"Processed insights for project: {project}, dataset: {dataset}, table: {table}")

        # show query if set
        if show_query == True:
            response['query'] = query_object.sql_getter()

        # add visual data if visual is true:
        if visual_data == True:
            try:
                data = initial_response.get('data')
                response['visual'] = json.loads(data)
            except Exception as e:
                response['visual'] = {'error':str(e)}

        return jsonify(response), 200
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": {"message": str(e), "query": query_object.sql_getter()}}), 500

@insights_bp.route('/table-schema', methods=['GET'])
@swag_from(schema_doc)
@require_headers
def schema():  
    try:
        # request data to json
        project = request.args.get('project', None)
        dataset = request.args.get('dataset', None)
        table = request.args.get('table', None)

        # check if all required arguments exist
        if None in [project, dataset, table]:
            return jsonify({'error': "missing required arguments"}), 400
        
        # initialize insight
        query_object = get_table_schema(project, dataset, table)
        # Create a dictionary to store the schema information
        schema_dict = {}
        for index, field in enumerate(query_object):
            schema_dict[f'column {index}'] = {
                "name": field.name,
                "field_type": field.field_type,
                "mode": field.mode,
                "description": field.description,
            }


        return jsonify(schema_dict), 200
    except Exception as e:
        logging.error(f'An error occorred with the server: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
