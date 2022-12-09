This folder contains the different lambdas written, across the different versions. All of these use 128MB and are time limited to 10 seconds -

BlackWhite - Convert to grayscale
Blur - Blur input image
CompressColors - Merge close shades into a single shade for better compression
DetectEdges - Perform edge detection
DotMap - Convert input image to a set of scattered black points on a white background
GrascaleIntermediate - A specialized version of BlackWhite, that saves to an intermediate file name and sets that as the next input, useful in the 'BasicVersion' flow (see stepfunctions) when PipelinedInputSide and PipelinedOutputSide are not used
HelloWorld - A testbed lambda for general experimentation
InputSide - An entry point for the 'BasicVersion' flow (see stepfunctions), capable of decoding a single input command
Monolith - The monolithic code implemented as a single lambda, used in the 'StarterAttempt' flow (see stepfunctions) and as a backup 'default' option in later flows.
PipelinedInputSide - An entry point for the 'PipelinedFlow' step function (see stepfunctions), capable of handling a list of commands to be executed sequentially and setting output file names accordingly
PipelinedOutputSide - An exit check for the 'PipelinedFlow' step function (see stepfunctions), capable of redirecting to PipelinedInputSide if further commands are to be executed, with updated inputs
Thumbnail - Convert input image to a 64*64 pixel thumbnail