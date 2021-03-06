
# Directory structure:

experiment  
| tdnn_7b_chain_online => A pretrained neural network trained on the apsire dataset

transcriptions => Contains the audio and Kaldi data config to transcribe the audio to text  
| guess.txt => Generated file when `decode.sh` is ran  
| wav.scp => Required Kaldi config file, links utterance id and audio file  
| spk2utt => Required Kaldi config file, links a speaker name to it's utterances  
| log_[0..3].wav => Example audio files to decode  

aspire_decoder.py => A wrapper for kaldi that uses the nnet network

decode.py => Decodes whatever is in `transcriptions` directory and outputs it to stdio  

path.sh => Sets PATH environment variable to include Kaldi's python library  

# How to run example
0. Install Kaldi docker
1. Clone this repository and [download the models](https://drive.google.com/open?id=1MdvtLku_w_nG0VT1qTUfPXNGpjnTlfeo) and paste them into the repo
2. Run `docker run -it -v $(pwd)/kaldi-demo/:/demo pykaldi/pykaldi:latest bash`
3. `cd demo`
4. `source path.sh`
5. `./decode.py`

# More info about transcriptions
`wav.scp` is a list of [utterance id] [audio]  
An utterance id is just name for a sentence said, for example, `mark_0`, `kate_0`, `mark_1`
```
mark_0 marks_question.wav
kate_0 kates_answer.wav
mark_1 marks_reaction.wav
```
`spk2utt` links a speaker name to it's utterances [speaker] [utterance id]
```
mark mark_0
kate kate_0
mark mark_1
```
The audio must be a .wav format with a 8000Hz sample frequency as stated in `experiment/tdnn_7b_chain_online/conf/mfcc.conf`  
The [audio] part in `wav.scp` can be a command that generates audio as well as long as it's in the format stated above

# How I made this demo
0. I downloaded the [aspire models from Kaldi's site](kaldi-asr.org/models/1/0001_aspire_chain_model.tar.gz)
1. Placed them in this demo folder
2. Ran `cd ..; docker run -it -v $(pwd)/demo/:/opt/kaldi/demo kaldiasr/kaldi:latest bash`
3. `cd egs/aspire/s5`
4. `cp -r /opt/kaldi/demo/0001_aspire_chain_model/exp /opt/kaldi/demo/0001_aspire_chain_model/data .`
5. `steps/online/nnet3/prepare_online_decoding.sh --mfcc-config conf/mfcc_hires.conf data/lang_chain exp/nnet3/extractor exp/chain/tdnn_7b exp/tdnn_7b_chain_online`
6. `utils/mkgraph.sh --self-loop-scale 1.0 data/lang_pp_test exp/tdnn_7b_chain_online exp/tdnn_7b_chain_online/graph`
7. Copied `exp/tdnn_7b_chain_online` to `experiments/tdnn_7b_chain_online` here
8. `cp -r /opt/kaldi/egs/aspire/s5/path.sh /opt/kaldi/egs/wsj/s5/steps /opt/kaldi/egs/wsj/s5/utils /opt/kaldi/demo`
9. Changed all instances of `/opt/kaldi/egs/aspire/s5` in `experiment/tdnn_7b_chain_online/conf/ivector_extractor.conf` and  `experiment/tdnn_7b_chain_online/conf/online.conf` to `/opt/kaldi/demo/experiment/` to point to this directory
10. Created `transcriptions`, `nnet_decoder.py`, `decode.py`, `clean.sh`, `readme.md`, and `.gitignore`