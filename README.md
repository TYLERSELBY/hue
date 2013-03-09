
# Requirements:
 * Requests library (http://docs.python-requests.org/en/latest/user/install/#install)

# First Use
 1. Run findhub.py with your local IP address: (e.g. ./findhub.py 10.0.1.200).  It will return the IP of the Hue controller
 1. Create a plaintext file called "hue.cfg" (or copy the hue.cfg.example) and replace the IP with the Hue controller's IP
 1. Run register.py, it will read the IP from the config file.  It will prompt you to push the button on the Hue controller, do it.
 1. register.py will write the secret into your hue.cfg; this acts as an API key from the python scripts to your specific Hue controller.
 1. You can now run scripts like setlight.py or pulse.py, or write your own.


# Existing scripts
 * fadeon.py fades lights on over 600 seconds
 * pulse.py pulses lights on and off with 1 second sleep between
 * setlight.py takes light number and brightness parameters and sets light(s) on and to that brightness

# Misc
All the info on the API I got from http://www.nerdblog.com/2012/10/a-day-with-philips-hue.html


