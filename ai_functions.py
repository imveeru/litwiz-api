##################### Vertext AI & PaLM API initialization #####################

import json
# import google.generativeai as palm
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
import vertexai

# config = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"] #for deploying    
config ='''{
  "type": "service_account",
  "project_id": "optimal-route-suggestion",
  "private_key_id": "19b0edee0b5acd92fd2068e84dec0c68d06eac6c",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdBicLKZ6Bs/wj\\nAdo9UNmvPRE2dL3cZS3uIQeK4tx0Vvy3l0b56HdoLu0QMwTWgOWe+YWXfAUwGB7q\\n+0pm8w1+MOkqC0V2IBVJl5/c4CEx3u+24kVHi6bnC90IgReJwC0xwN1HaCJatESA\\n4fCJYnN1qRKXU1gx3KFGxl9UX3+sWG+TPoWATVfKlf5poLrzZJ9E9QglkMl+slpm\\nRjdb3M4f2pFmL1/190bilxfokLT3+LqC3GaIIPQY7lWlWACXt+ldvqsTiIMo/z+Z\\nGwoSJ4xwd+O3JtUHhh+KSRY6Oc43OIhJhKcqsXsuuRl4LWu//uImrt2oilcXguYU\\nJRSrvU8bAgMBAAECggEARCGrRzijwftqZ3YiT4CJM3P3x/0XdE2ihDRopWaR6Rjl\\nRnOpJD4tsVLLIcBBVSFQgI4b3QK+7YNJxwOJ4OmM7Tgjs054sSxykB/uCVRmktD8\\nignbrZN2s8F+Anag0/BCq9fXK2iPn3OgVZuzVqkVF/RoUKilF913TNI+Asn9B7YZ\\nkeoUqSNUUN5fjIgKNWMEvolKZu+TdYobxV9GOevX8FwTx87qmF9Ue8P1RxzyAD3X\\nMBjm5ohZufg6zctN0vxK2OXGvV9lc/qfsxtHhtRoyS3F0Da2NZIXSndl3Arh0Bcb\\nq8b9eo85yjcy+oGVwo00gytpJBk2k445EtwWW0p7oQKBgQDLU5Ux9N9hCT6p1f4N\\n0ngaihCxjxnGu4ZPR3tIiqG5JWN+0vr0obVr9A5m3LU7/AG9Bmm85MlQi6FmuoDw\\neqQY85nImx5z3i55CTx9HOOTpA2pbTIHNqZ8aPLxZI0he1Pnvu6qpiRH3d51Nby4\\nJ4Qbi+Wd+CmAy6jHib3yNL+eTQKBgQDFs9XGv/gfsparX1DMoAfU1v97WkXxUruI\\nxCmSlUpVb4kmDs4gk8x9GJcokvxEr5+iJUPkzwexW/LBaulAdJB3dR8phvGBqvag\\nMe04IkeKVuOXwTgM1QMZmbIvLL3fA546dgksXK5vZ5qal+N3GK/dLhIPQk7zo1nO\\nuy/Y5otnBwKBgQCjCBj4HpXCU8xYF8sGwD0nYo8yIEEV1aVDCljy+J3mO/GEbp1k\\n7AjxT5cAqXX0bAPk0jCUkopNODipi1/58wyDKUikzqRjWcK/sEU9OJ3N81w0/uZ/\\nXDWwSeKK5go3z5CeoLz0PhWXPnKyXu08aAsIn2r0+Fgm+qYRoQOaIuuGfQKBgCWy\\nNIDA+b6RfskOU4mwuc2LcQtEGzH4ZGmffY3FiXbg3XW0PPlZNRRlK+1AmXk/Q2DX\\nWiq2jvDyZ0cZ63+uuh0M5/QzFrlyr7O70U9yudFW3+5/mQBZXU30UFVOYqWzOuhK\\nuVUMFvaG+qOfcm+y9VVnA2qFaihqbSVN68Gfs9ThAoGAacSC7rPBXrYbWJaHpwcc\\nb0b/AODiz03HS/YPWpG778mJXueH7l05RYMCHmfQlLsCUia7j87MaVppok7lb7HY\\nH0fPt0y9fmPB/YT3rX/jsFrBDzuJynd2pYZqgjwWLjWfMRjlg1SdOpzdeK81yVCw\\nHCs87atWEc87lcaIVCzItbg=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "langchainapps@optimal-route-suggestion.iam.gserviceaccount.com",
  "client_id": "103157086402886138790",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/langchainapps%40optimal-route-suggestion.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
''' #for testing(cd dependencies; zip ../aws_lambda_artifact.zip -r .)
service_account_info=json.loads(config)
service_account_info["private_key"]=service_account_info["private_key"].replace("\\n","\n")
# st.write(service_account_info)
my_credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)
aiplatform.init(
    credentials=my_credentials,
)
project_id = service_account_info["project_id"]
vertexai.init(project=project_id, location="us-central1")

##################### Serper Request to fetch URL #####################

import os
import json
import requests
# from dotenv import find_dotenv,load_dotenv

# load_dotenv(find_dotenv())
# SERPAPI_API_KEY=os.getenv("SERPAPI_API_KEY")

##################### Search through web #####################

def search(input_query):
    
    url=f"https://api.semanticscholar.org/graph/v1/paper/search?query={input_query}&limit=3&fields=url,abstract,authors,tldr,year,title,citationStyles"
    response=requests.request("GET",url)
    response_data=response.json()

    return response_data if response_data["total"]>=1 else "No papers found!"
    

##################### Extract Paper & Make lit survey #####################

from langchain.llms import VertexAI
from langchain.chains import LLMChain
from langchain import PromptTemplate

def create_lit_survey(search_results,query):
    response_str=json.dumps(search_results)
    llm=VertexAI(max_output_tokens=1024,max_retries=6)
    
    # template='''
    # You are a world class researcher, you are extremely good at find most relevant papers to certain topic;
    # {response_str}
    # Above is the list of search results for the query {query}.
    # Please choose the best 5 papers from the list, return ONLY an array of the PaperID, do not include anything else; retun ONLY an array of the PaperID, do not include anything else.
    # '''
    
    template='''
    You are a world class researcher, you are extremely good at writing literature surveys on certain topic by using the given papers;
    {response_str}
    Above is the list of search results for the query {query}.
    Please write a comprehensive literature survey for the topic {query} using the given search results.
    The literature survey must have a proper conclusion with mentioning a RESEARCH GAP. 
    If no papers are found, do not hallucinate and write a literature survey. Just output no relevant paper are found.
    Avoid multiple sub headings and bullet points.
    Compile the results of paper and find relation between its results and present them as PARAGRAPHS instead of points.
    Proper CITATIONS must be added in the survey by mentioning the author name along with the year.
    The output must be in ACADEMIC TONE.
    Return ONLY the literature survey, do not include anything else;Return ONLY the literature survey, do not include anything else;Return ONLY the literature survey, do not include anything else;
    '''
    
    prompt_template=PromptTemplate(
        input_variables=["response_str","query"],
        template=template
    )
    
    writer_chain=LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False
    )
    
    lit_survey=writer_chain.predict(response_str=response_str,query=query)
    # id_list=json.loads(ids)
    # print("LitSurvey",lit_survey)
    
    return lit_survey


##################### Extract Citations from results #####################
def get_citations(search_results):
    if search_results:
        paper_data=search_results["data"]
    else:
        return "No results found!"
    citations=""
    for paper in paper_data:
        citation_list=paper["citationStyles"]
        citation=citation_list["bibtex"]
        citations+="\n"+citation
    
    return citations

##################### Consolidated Function #####################
def get_lit_survey(query):
    search_results=search(query)
    lit_survey=create_lit_survey(search_results,query)
    citations=get_citations(search_results)
    
    return lit_survey,citations

# lit,cit=get_lit_survey("AI chatbots in education")
# print(lit)
# print(cit)

##################### Get Abstract #####################
def get_abstract(abs_query):
    llm=VertexAI(max_output_tokens=1024,max_retries=6)
    
    template='''
    You are a world class researcher, you are extremely good at writing abstract for research papers by giving you a brief of the work;
    {query}
    Above is the description of the work being done in the research paper.
    Please write a compelling abstract using the given description.
    The abstract must start by defining the existing work and few research gap based on the given description. 
    If no relevant content is found, do not hallucinate. Just output no relevant content is found.
    Avoid multiple sub headings and bullet points. Give the response as a single paragraph.
    Compile the all the content and output as a SINGLE PARAGRAPH of length less than 300.
    The output must be in ACADEMIC TONE.
    Return ONLY the abstract of the paper, do not include anything else;Return ONLY the abstract of the paper, do not include anything else;Return ONLY the abstract of the paper, do not include anything else;
    '''
    
    prompt_template=PromptTemplate(
        input_variables=["query"],
        template=template
    )
    
    writer_chain=LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False
    )
    
    abst=writer_chain.predict(query=abs_query)
    # id_list=json.loads(ids)
    # print("LitSurvey",lit_survey)
    
    return abst

##################### Get Title #####################
def get_title(title_query):
    llm=VertexAI(max_output_tokens=1024,max_retries=6)
    
    template='''
    You are a world class researcher, you are extremely good at suggesting title for research papers by giving you a brief of the work;
    {query}
    Above is the description of the work being done in the research paper.
    Please write a creative, inviting, convincible and suitable title for the research paper using the given description.
    The title must reflect the work done in the paper based on the given description. 
    The output must be in ACADEMIC TONE.
    Return ONLY a list of titles for the paper in markdown format, do not include anything else;Return ONLY a list of titles for the paper in markdown format, do not include anything else;Return ONLY a list of titles for the paper in markdown format, do not include anything else;
    '''
    
    prompt_template=PromptTemplate(
        input_variables=["query"],
        template=template
    )
    
    writer_chain=LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=False
    )
    
    title=writer_chain.predict(query=title_query)
    # id_list=json.loads(ids)
    # print("LitSurvey",lit_survey)
    
    return title
