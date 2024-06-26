from IPython.display import Markdown

PROJECT_ID = "ceep-394706"  # @param {type:"string"}
LOCATION = "europe-west4"  # @param {type:"string"}
ADV_RESULT = False

# Initialize Vertex AI
import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)
    
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)

text_model = GenerativeModel("gemini-1.0-pro")
multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

import pandas as pd
text_metadata_df_2 = pd.read_csv('dataframes/text_metadata_df.csv')
image_metadata_df_2 = pd.read_csv('dataframes/image_metadata_df.csv')

# Convert the columns to lists using eval()
text_metadata_df_2["text_embedding_page"] = text_metadata_df_2["text_embedding_page"].apply(eval)
text_metadata_df_2["text_embedding_chunk"] = text_metadata_df_2["text_embedding_chunk"].apply(eval)

# Convert the columns to lists using eval()
image_metadata_df_2["mm_embedding_from_img_only"] = image_metadata_df_2["mm_embedding_from_img_only"].apply(eval)
image_metadata_df_2["text_embedding_from_image_description"] = image_metadata_df_2["text_embedding_from_image_description"].apply(eval)

from utils.intro_multimodal_rag_utils import (
    get_similar_text_from_query,
    print_text_to_text_citation,
    get_similar_image_from_query,
    print_text_to_image_citation,
    get_gemini_response,
    display_images,
)

def context_text(query):

    # Retrieve relevant chunks of text based on the query
    matching_results_chunks_data = get_similar_text_from_query(
        query,
        text_metadata_df_2,
        column_name="text_embedding_chunk",
        top_n=10,
        chunk_text=True,
    )

    # combine all the selected relevant text chunks
    context_text = []
    for key, value in matching_results_chunks_data.items():
        context_text.append(value["chunk_text"])
    final_context_text = "\n".join(context_text)

    return matching_results_chunks_data, final_context_text

def context_image(query):
    # Get all relevant images based on user query
    matching_results_image_fromdescription_data = get_similar_image_from_query(
        text_metadata_df_2,
        image_metadata_df_2,
        query=query,
        column_name="text_embedding_from_image_description",
        image_emb=False,
        top_n=10,
        embedding_size=1408,
    )

    # combine all the relevant images and their description generated by Gemini
    context_images = []
    for key, value in matching_results_image_fromdescription_data.items():
        context_images.extend(
            ["Image: ", value["image_object"], "Caption: ", value["image_description"]]
        )
    return matching_results_image_fromdescription_data, context_images


def adv_results(matching_results_image_fromdescription_data, matching_results_chunks_data):
    print("---------------Matched Images------------------\n")
    display_images(
        [
            matching_results_image_fromdescription_data[0]["img_path"],
            matching_results_image_fromdescription_data[1]["img_path"],
            matching_results_image_fromdescription_data[2]["img_path"],
            matching_results_image_fromdescription_data[3]["img_path"],
        ],
        resize_ratio=0.5,
    )

    # Image citations. You can check how Gemini generated metadata helped in grounding the answer.

    print_text_to_image_citation(
        matching_results_image_fromdescription_data, print_top=False
    )

    # Text citations

    print_text_to_text_citation(
        matching_results_chunks_data,
        print_top=False,
        chunk_text=True,
    )

def ask(query):

    #Contexto de texto
    matching_results_chunks_data, final_context_text = context_text(query)

    #Contexto de imagenes
    matching_results_image_fromdescription_data, context_images = context_image(query)
    
    #Definición del prompt
    prompt = f""" Eres un asistente virtual experto en las plataformas DocSupport, DataQuality y DataQuality GenAI.
    Tu objetivo es responer todas las preguntas que te hagan con alto nivel de detalle.
    Compara las imagenes y el texto definidos como Contexto: para responder cualquier pregunta que tenga el usuario, definida como Query:
    Asegúrate de pensar en profundidad antes de responder cualquier pregunta.
    Si no estás seguro de la respuesta, responde "No tengo suficiente contexto para responder."
    Puedes

    Contexto:
    - Contexto de texto:
    {final_context_text}
    - Contexto de imagenes:
    {context_images}
    
    Query:
    - {query}

    Respuesta:
    """


    print(prompt)

    print("\n\nDocSupport:\n")
    # Respuesta de Gemini
    # Markdown(
    return get_gemini_response( multimodal_model, model_input=[prompt], stream=True, generation_config=GenerationConfig(temperature=0.4, max_output_tokens=2048))

    #if ADV_RESULT:
    #    adv_results(matching_results_image_fromdescription_data, matching_results_chunks_data)
    