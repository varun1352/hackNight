from lightning_sdk import AIHub

hub = AIHub()
deployment = hub.run("temp_01jjt2pkg54t138gsx6ryk0gmr",
  teamspace="vision-model",
  user="vd2298"
)
print(deployment)
print(type(deployment))