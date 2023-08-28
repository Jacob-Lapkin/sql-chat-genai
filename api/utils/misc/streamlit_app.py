from main import Sqlinsights
import streamlit as st
from bigquery import get_table_schema


def stream_app():
    # Title
    st.title('Ingram Micro Insights QA chat')
    col1, col2, col3 = st.columns(3)
    # define columns and input
    with col1:
        project_input = st.text_input(label='input project', value='imgcp-20220210133450')
    with col2:
        dataset_input = st.text_input(label='input dataset', value='PIMCOREPROD')
    with col3:
        table_input = st.text_input(label='input table', value='DESCRIPTION')


    # initialize user input
    user_input = st.chat_input("Your message", key='chat_input')

    # get table schema 
    if st.button('Get table schema'):
        st.write(get_table_schema(project_input, dataset_input, table_input))

    show_visual = st.checkbox('show visual', value=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Run the agent chain
        try:
            with st.spinner('Processing your question...'):
                query = Sqlinsights(project_input, dataset_input, table_input, user_input)
                query_result = query.interpret_results()
                output = query_result[0]
                chart = query_result[1]

                # Display bot message
                with st.chat_message("assistant"):
                    st.write(output)
                    if show_visual == True:
                        try:
                            st.bar_chart(chart)
                        except Exception as e:
                            print(e)
        except Exception as e:
            with st.chat_message("assistant"):
                st.write(f"Sorry, I encountered an error: {str(e)}")

stream_app()

# stream_app("imgcp-20220210133450", "PIMCOREPROD", "CROSSSELL_MD")