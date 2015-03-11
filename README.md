# Jymagor
Fiji plugin version of Pymagor. The functionality is much reduced compared to Pymagor. No trial alignment, averaging, report PDF, mat file export etc are available. Consider Pymagor for advanced analysis. This plugin will be useful for online analysis and you can take advantage of excellent Fiji plugins out there.

Feed a stack (i.e., calcium imaging time series) and get a frame average of raw pixel values for morphology and a dF/F response map (frame averaged). Optionally, you can get a dF/F movie (slow).


# Installation

1. Copy clut2b.lut into luts folder (typically Fiji.app\luts).
2. Copy the Jymagor folder to Fiji.app\plugins\Scripts
3. Fire up Fiji and Help -> Refresh Menus.
4. Jymagor should be available under Plugins menu (reboot Fiji if not)

# Usage

- Open a stack to analyze
- Find Menu next to Help menu and open the main panel (Jymagor -> Panel)
- Adjust the frame range for F (basal level) and Res (Response period)
- Click to activate the stack you want to analyze
- Press [Update] button on the main panel
- You will have morphology and dF/F response map windows as well as Fiji's defaul ROI manager
- define ROIs on any of opened image and add them to the ROI manager
- Press [Plot] button on the main panel to get a plot of dF/F traces
- Save ROIs using ROI manager's interface.

