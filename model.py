
#################################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the prompt text we want
# to provide as an input. Change these strings to run your own example.
#################################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '1400c09c515d454eb5ef9d0562a081c0'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'stability-ai'
APP_ID = 'stable-diffusion-2'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'stable-diffusion-xl'
MODEL_VERSION_ID = '68eeab068a5e4488a685fc67bc7ba71e'
# To use a hosted text file, assign the URL variable
# TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
# Or, to use a local text file, assign the location variable
# TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def generateimage (prompt):

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    # To use a local text file, uncomment the following lines
    # with open(TEXT_FILE_LOCATION, "rb") as f:
    #    file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                            # url=TEXT_FILE_URL
                            # raw=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0].data.image.base64

    image_filename = f"gen-image.jpg"
    with open(image_filename, 'wb') as f:
        f.write(output)
        
