#!/usr/bin/env python3

from kaldi.asr import NnetLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.nnet3 import NnetSimpleComputationOptions
from kaldi.util.table import SequentialMatrixReader

class RDK:
    success = "success"
    return_msg = "return_msg"
    debug_data = "debug_data"

class RC:
    failed = False
    success = True
    input_validation = 1001

class KaldiNnetDecoder:

    CV_default_nnet_directory = "experiment/tdnn_7b_chain_online"
    CV_default_transcription_directory = "transcriptions"

    def __init__(self):
        self.IV_asr = None
        self.IV_is_ready = False
        self.IV_feats = ""
        self.IV_ivectors = ""

    def init(self, nnet_directory, transcription_directory):
        return_msg = "KaldiDecoder:init"
        debug_data = []
        feats = ""
        ivectors = ""
        decoder_opts = None
        decodable_opts = None
        asr = None

        ## input validation
        if nnet_directory is not None:
            if type(nnet_directory) is not str:
                return_msg += "nnet_directory is not of type string, is type {}".format(type(nnet_directory))
                return {RDK.success: RC.input_validation, RDK.return_msg: return_msg, RDK.debug_data: debug_data}
        else:
            nnet_directory = KaldiNnetDecoder.CV_default_nnet_directory

        if transcription_directory is not None:
            if type(transcription_directory) is not str:
                return_msg += "transcription_directory is not of type string, is type {}".format(type(transcription_directory))
                return {RDK.success: RC.input_validation, RDK.return_msg: return_msg, RDK.debug_data: debug_data}
        else:
            transcription_directory = KaldiNnetDecoder.CV_default_transcription_directory
        ##</end> input validation

        ## feats and ivector rspec creation
        feats = (
            "ark:compute-mfcc-feats --config={0}/conf/mfcc.conf scp:{1}/wav.scp ark:- |"
        ).format(nnet_directory, transcription_directory)

        ivectors = (
            "ark:compute-mfcc-feats --config={0}/conf/mfcc.conf scp:{1}/wav.scp ark:- |"
            "ivector-extract-online2 --config={0}/conf/ivector_extractor.conf ark:{1}/spk2utt ark:- ark:- |"
        ).format(nnet_directory, transcription_directory)
        ##</end> feats and ivector rspec creation

        ## asr creation
        decoder_opts = LatticeFasterDecoderOptions()
        decoder_opts.beam = 13
        decoder_opts.max_active = 7000

        decodable_opts = NnetSimpleComputationOptions()
        decodable_opts.acoustic_scale = 1.0
        decodable_opts.frame_subsampling_factor = 3
        decodable_opts.frames_per_chunk = 150

        asr = NnetLatticeFasterRecognizer.from_files(
            "{}/final.mdl".format(nnet_directory),
            "{}/graph/HCLG.fst".format(nnet_directory),
            "{}/graph/words.txt".format(nnet_directory),
            decoder_opts=decoder_opts,
            decodable_opts=decodable_opts)
        ##</end> asr creation
        
        self.IV_feats = feats
        self.IV_ivectors = ivectors
        self.IV_asr = asr
        self.IV_is_ready = True

        return {RDK.success: RC.success, RDK.return_msg: return_msg, RDK.debug_data: debug_data}

    def decode(self):
        return_msg = "KaldiDecoder:decode"
        debug_data = []
        transcriptions = []

        ## init check
        if self.IV_is_ready is False:
            return_msg += "KaldiDecoder has not been initialized"
            return {RDK.success: RC.success, RDK.return_msg: return_msg, RDK.debug_data: debug_data, "transcriptions": transcriptions}
        ##</end> init check

        ## decoding
        with SequentialMatrixReader(self.IV_feats) as f_rspec, SequentialMatrixReader(self.IV_ivectors) as iv_rspec:
            for (_, feats), (_, ivectors) in zip(f_rspec, iv_rspec):
                out = self.IV_asr.decode((feats, ivectors))
                transcriptions.append(out["text"])
        ##</end> decoding

        return {RDK.success: RC.success, RDK.return_msg: return_msg, RDK.debug_data: debug_data, "transcriptions": transcriptions}
