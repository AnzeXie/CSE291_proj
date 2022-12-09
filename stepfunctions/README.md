This folder contains the exported JSON versions of the three step function flows implemented, as described below -

StarterAttempt - This version simply triggers the lambda version of the monolithic code. This was used as an initial testing point for step functions.
BasicVersion - This version uses an input handler to decide which lambda to trigger, then triggers that lambda. Only a single command can be executed.
PipelinedFlow - This version improves on BasicVersion by introducing an exit check that redirects to the input handler if there are more commands to be executed, i.e. the flow is no longer acyclic.