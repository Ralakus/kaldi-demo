
# Directory structure:

experiment  
| tdnn_7b_chain_online => A pretrained neural network trained on the apsire dataset

steps => Kaldi standard directory with helper scripts to Kaldi  

transcriptions => Contains the audio and Kaldi data config to transcribe the audio to text  
| guess.txt => Generated file when `decode.sh` is ran  
| wav.scp => Required Kaldi config file, links utterance id and audio file  
| utt2spk => Required Kaldi config file, links the utterance id and speaker name  
| log_[0..3].wav => Example audio files to decode  

utils => Kaldi standard directory with helper scripts to Kaldi  

decode.sh => Decodes whatever is in `transcriptions` directory and outputs `guess.txt` with the transcriptions in `transcriptions` directory  

path.sh => Kaldi standard file, exports path information for Kaldi for scripts  

readme.md => This file

# More info about transcriptions
`wav.scp` is a list of [utterance id] [audio]  
An utterance id is just name for a sentence said, for example, `mark_0`, `kate_0`, `mark_1`
```
mark_0 marks_question.wav
kate_0 kates_answer.wav
mark_1 marks_reaction.wav
```
`utt2spk` links an utterance id to a speaker [utterance id] [speaker]
```
mark_0 mark
kate_0 kate
mark_1 mark
```
The audio must be a .wav format with a 8000Hz sample frequency as stated in `experiment/tdnn_7b_chain_online/conf/mfcc.conf`  
The [audio] part in `wav.scp` can be a command that generates audio as well as long as it's in the format stated above

# How to run example
0. Install Kaldi docker
1. Clone this repository and [download models](https://drive.google.com/open?id=1MdvtLku_w_nG0VT1qTUfPXNGpjnTlfeo) and paste them into the repo
2. Run `docker run -it -v $(pwd)/demo/:/opt/kaldi/demo kaldiasr/kaldi:latest bash`
3. `cd demo`
4. `./decode.sh`
