import vertexai
from utils.intro_multimodal_rag_utils import get_document_metadata
from vertexai.generative_models import GenerativeModel

def main(cloud_event):
  print(cloud_event)
  # Initialize Vertex AI
  PROJECT_ID = os.getenv('PROJECT_ID')
  LOCATION = os.getenv('LOCATION')
  vertexai.init(project=PROJECT_ID, location=LOCATION)    

  # Load Models
  text_model = GenerativeModel("gemini-1.0-pro")
  multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

  # Specify the PDF folder with multiple PDF
  pdf_folder_path = "gs://docsupport-data/"  # if running in Vertex AI Workbench.

  

  # Specify the image description prompt. Change it
  image_description_prompt = """Explain what is going on in the image.
  If it's a table, extract all elements of the table.
  If it's a graph, explain the findings in the graph.
  Do not include any numbers that are not mentioned in the image.
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

# Triggered by a change in a storage bucket
#@functions_framework.cloud_event
#def hello_gcs(cloud_event):
#    data = cloud_event.data
#
#    event_id = cloud_event["id"]
#    event_type = cloud_event["type"]
#
#    bucket = data["bucket"]
#    name = data["name"]
#    metageneration = data["metageneration"]
#    timeCreated = data["timeCreated"]
#    updated = data["updated"]
#
#    print(f"Event ID: {event_id}")
#    print(f"Event type: {event_type}")
#    print(f"Bucket: {bucket}")
#    print(f"File: {name}")
#    print(f"Metageneration: {metageneration}")
#    print(f"Created: {timeCreated}")
#    print(f"Updated: {updated}")
#