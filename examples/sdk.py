# Install the Lightning SDK
# pip install -U lightning-sdk

# login to the platform
# export LIGHTNING_USER_ID=aef62a31-85b3-4c93-9a44-0124278fc3c4
# export LIGHTNING_API_KEY=07774d4b-67e6-4cec-9dd8-06d1237a01b7

from lightning_sdk import Machine, Studio, JobsPlugin, MultiMachineTrainingPlugin

# Start the studio
s = Studio(name="my-sdk-studio", teamspace="language-model", org="vd2298", create_ok=True)
print("starting Studio...")
s.start()

# prints Machine.CPU-4
print(s.machine)

print("switching Studio machine...")
s.switch_machine(Machine.A10G)

# prints Machine.A10G
print(s.machine)

# prints Status.Running
print(s.status)

print(s.run("nvidia-smi"))

print("Stopping Studio")
s.stop()

# duplicates Studio, this will also duplicate the environment and all files in the Studio
duplicate = s.duplicate()

# delete original Studio, duplicated Studio is it's own entity and not related to original anymore
s.delete()

# stop and delete duplicated Studio
duplicate.stop()
duplicate.delete()
    