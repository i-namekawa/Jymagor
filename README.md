# Jymagor
Fiji plugin version of Pymagor

Feed a stack (calcium imaging data, i.e., time series) and get frame average of raw pixel value (for morphology) and frame averaged dF/F map. Optionally you can get a dF/F movie (slow).


# Installation

1. Copy clut2b.lut into luts folder (typically Fiji.app\luts).
2. Copy the Jymagor folder to Fiji.app\plugins\Scripts\Plugins
3. Fire up Fiji and Help -> Refresh Menus.
4. Jymagor should be available under Plugins menu (reboot Fiji if not)

# Usage

- Open the stack to analyze
- Plugins -> Jymagor -> Panel
- Adjust the frame range for F (basal level) and Res (Response period)
- Click to activate the stack you want to analyze
- Press [Launch/Update]


