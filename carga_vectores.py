
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = "ceep-394706"
LOCATION = "europe-west4"
vertexai.init(project=PROJECT_ID, location=LOCATION)

from utils.intro_multimodal_rag_utils import get_document_metadata

# Load Models
text_model = GenerativeModel("gemini-1.0-pro")
multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

# Specify the PDF folder with multiple PDF
pdf_folder_path = "data/"  # if running in Vertex AI Workbench.

# Specify the image description prompt. Change it
image_description_prompt = """Explica los contenidos de la imagen.
Si es una tabla, extrae todos los elementos de ella.
Si es un grafo, explica las conclusiones de este.
No incluyas números ni datos que no estén incluidos en la imagen.
"""

# Extract text and image metadata from the PDF document
text_metadata_df, image_metadata_df = get_document_metadata(
    multimodal_model,  # we are passing gemini 1.0 pro vision model
    pdf_folder_path,
    image_save_dir="images",
    image_description_prompt=image_description_prompt,
    embedding_size=1408,
    add_sleep_after_page = True, # Uncomment this if you are running into API quota issues
    # sleep_time_after_page = 5,
    # generation_config = # see next cell
    # safety_settings =  # see next cell
)

print("\n\n --- Completed processing. ---")

text_metadata_df.to_csv('dataframes/text_metadata_df.csv', index=False)
image_metadata_df.to_csv('dataframes/image_metadata_df.csv', index=False)