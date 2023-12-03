import subprocess
import re
import time


def set_pulseaudio_volume(sink_name, volume_level):
    subprocess.run(["pactl", "set-sink-volume", sink_name, f"{volume_level}%"])


def parse_running_sources():
    result = subprocess.run(["pacmd", "list-sources"], capture_output=True, text=True)
    output = result.stdout

    # Regular expression to capture source blocks
    source_blocks = re.findall(r'index: \d+.*?(?=index: \d+|\Z)', output, re.DOTALL)

    running_sources = []
    for block in source_blocks:
        if "state: RUNNING" in block:
            source = {}
            lines = block.split('\n')
            for line in lines:
                key_value_match = re.match(r'\s*(\S.*?):\s*(.*)', line)
                if key_value_match:
                    key = key_value_match.group(1).strip()
                    value = key_value_match.group(2).strip()

                    # Special handling for certain keys
                    if key in ['volume', 'channel map']:
                        value = value.split(',')
                    elif key in ['muted', 'corked']:
                        value = value == 'yes'

                    source[key] = value

            running_sources.append(source)

    return running_sources


def parse_sink_inputs():
    result = subprocess.run(["pacmd", "list-sink-inputs"], capture_output=True, text=True)
    output = result.stdout
    if "0 sink input(s) available." in output:
        return []
    # Regular expression to capture sink input blocks
    sink_input_blocks = re.findall(r'index: \d+.*?(?=index: \d+|\Z)', output, re.DOTALL)
    sink_inputs = []
    for block in sink_input_blocks:
        # Parsing each sink input block
        sink_input = {}
        lines = block.split('\n')
        for line in lines:
            key_value_match = re.match(r'\s*(\S.*?):\s*(.*)', line)
            if key_value_match:
                key = key_value_match.group(1).strip()
                value = key_value_match.group(2).strip()
                # Special handling for certain keys
                if key in ['volume', 'channel map']:
                    value = value.split(',')
                elif key in ['muted', 'corked']:
                    value = value == 'yes'
                sink_input[key] = value
        sink_inputs.append(sink_input)
    return sink_inputs


# Usage
inputs = parse_sink_inputs()
for i in inputs:
    print(i)
    
sources = parse_running_sources()
for s in sources:
    print(s)
