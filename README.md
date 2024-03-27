# RotaryGPT

Turn a rotary phone into an AI phone featured by FullyAI. The basic code is forked from [https://github.com/tcz/rotary-gpt](https://github.com/tcz/rotary-gpt).

## Hardware

The rotary phones need to be converted to RJ11 compatibility, for german TAE cables solder them as follows (TAE->RJ11):

- brown -> red
- green -> green
- white -> black (optional)
- yellow -> yellow (optional)

The connect the RJ11 to the Grandstream HT801 and also connect a network and power cable to it.

## Grandstream HT801 Configuration

The HT801 needs to be configured to call our server when the handset is picked up. This can be done on the web interface of the device, 
under FXS PORT. The defaut credentials for the web interface are `admin` and `admin`.

- Offhook Auto-Dial: `*4737*16*9*47*5060` (*47 starts an IP call followed by the IP of the deployed server and the port)
- Offhook Auto-Dial Delay: `2` (wait 2 seconds before the call is placed to allow putting the handset to the ear)

## Local Setup

Install the dependencies with:

```
pip install -r requirements.txt
```

Copy the `.env.template` file to `.env` and adjust the environment variables. Currently only the OPENAI_API_KEY is used.

For a local run you currently need to set the `SERVER` variable in rotarygpt.py to `0.0.0.0`. Please remember to revert before the deployment, as fly.io needs the server to be set to `fly-global-services` to be able to receive UDP packages.

You can now run the server locally with:

```
python3 rotarygpt.py
```

This will start the SIP server on port 5060. You can then connect to it with your rotary phone.

## Deployment

The current deployment runs on fly.io. If you need to adjust the project you can edit the `fly.toml` file. To deploy the project run:

```
flyctl deploy --no-cache
```

If not already, assign a static IP that is then configured in the HT801 offhook auto-dial setting.
