#!/usr/bin/env python3

from nnet_decoder import KaldiNnetDecoder

class RDK:
    success = "success"
    return_msg = "return_msg"
    debug_data = "debug_data"

class RC:
    failed = False
    success = True
    input_validation = 1001

call_result = None
decoder = KaldiNnetDecoder()

call_result = decoder.init(None, None)
if call_result[RDK.success] is not RC.success:
    print("Error in init", call_result[RDK.return_msg])

call_result = decoder.decode()
if call_result[RDK.success] is not RC.success:
    print("Error in decoding", call_result[RDK.return_msg])

transcriptions = call_result["transcriptions"]

for transcription in transcriptions:
    print("\033[32m", transcription, "\033[37m", sep='')