# ¿Qué es DataQuality Support?


· DataQuality Support es un chatbot de soporte técnico y respuesta de preguntas con base de conocimiento completamente personalizable.
· Está construido sobre la documentación de otra de nuestras soluciones, DataQuality Platform, pero se puede personalizar para que funcione con documentaciones de otras plataformas.
· Utiliza una arquitectura RAG con IA Generativa para aumentar la veracidad y minimizar las alucinaciones de las respuestas.

# Despliege del chatbot

Primero teines que hacer un clon de este github

<pre>
    <code>
        git clone https://github.com/PixelVolt38/DQSupport.git
    </code>
</pre>

Una vez tienes creado tu repositorio local tienes que hacer un trigger tienes que crear las conexines de google a git


<pre>
    <code>
        gcloud source repos create YOUR-USERNAME/YOUR-REPOSITORY --project=PROYECT-ID
    </code>
</pre>

<!-- <pre>
    <code>
        gcloud beta builds triggers create rmgpgab-dqsupport-europe-west4-PixelVolt38-DQSupport--mabgx \
            --region=europe-west4 \
            --project=PROYECT-ID \
            --repo-name=YOUR-USERNAME/YOUR-REPOSITORY \
            --branch-pattern=master \
            --service-account=dqsupport@ceep-394706.iam.gserviceaccount.com \
            --substitutions=_REGION=europe-west4,_PROJECT_ID=PROYECT-ID,_REPO_NAME=PixelVolt38,_BRANCH_PATTERN=master,_SERVICE_ACCOUNT=dqsupport@ceep-394706.iam.gserviceaccount.com \
            --description="DQSupport trigger for github to creeate " \
            --build-config=cloudbuild.yaml \
            --timeout=3600s
    </code>
</pre> -->




