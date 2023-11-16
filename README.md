# Smart_Home_API_Test
This is a repo for our capstone. This is a Smart home design based on a LLM and designed for elderly. We will update it as we work on it for capstone.

To run this code you will need to install some files. 
To get the credential.json file follow the steps at this link.
https://developers.google.com/calendar/api/quickstart/python

Once that is done, move the credential.json file to the LLM folder and run quikcstart.py to get the token.json file.

you will also need to set up your .env file and set the path for audio and text files. as well as your openai key and serper api key.

python libraries
absl-py                   2.0.0       
accelerate                0.23.0      
aiohttp                   3.8.5       
aiosignal                 1.3.1       
annotated-types           0.5.0       
anyascii                  0.3.2       
appdirs                   1.4.4       
asttokens                 2.4.1       
async-timeout             4.0.3       
attrs                     23.1.0      
audioread                 3.0.0       
av                        10.0.0      
Babel                     2.12.1      
backcall                  0.2.0       
bangla                    0.0.2       
blinker                   1.6.2       
bnnumerizer               0.0.2       
bnunicodenormalizer       0.1.1       
boltons                   23.0.0      
boto3                     1.28.72     
botocore                  1.31.72     
brotlipy                  0.7.0       
cachetools                5.3.1       
certifi                   2021.5.30   
cffi                      1.14.6      
chardet                   4.0.0       
charset-normalizer        3.2.0       
clean-fid                 0.1.35      
click                     8.1.7       
clip-anytorch             2.5.2       
colorama                  0.4.6       
coloredlogs               15.0.1      
conda                     4.10.3      
conda-package-handling    1.7.3       
contourpy                 1.1.1       
coqpit                    0.0.17      
cryptography              3.4.7       
ctranslate2               3.19.0      
cycler                    0.11.0      
Cython                    0.29.28
dataclasses-json          0.5.14
dateparser                1.1.8
decorator                 5.1.1
docker-pycreds            0.4.0
docopt                    0.6.2
einops                    0.6.1
elevenlabs                0.2.26
encodec                   0.1.1
espeakng                  1.0.2
exceptiongroup            1.1.3
executing                 2.0.0
faster-whisper            0.8.0
filelock                  3.12.3
Flask                     2.3.3
flatbuffers               23.5.26
fonttools                 4.42.1
frozenlist                1.4.0
fsspec                    2023.6.0
ftfy                      6.1.1
funcy                     2.0
g2pkk                     0.1.2
gitdb                     4.0.10
GitPython                 3.1.36
google-api-core           2.11.1
google-api-python-client  2.100.0
google-auth               2.23.0
google-auth-httplib2      0.1.1
google-auth-oauthlib      1.0.0
googleapis-common-protos  1.60.0
greenlet                  2.0.2
grpcio                    1.58.0
gruut                     2.2.3
gruut-ipa                 0.13.0
gruut-lang-cs             2.0.0
gruut-lang-de             2.0.0
gruut-lang-en             2.0.0
gruut-lang-es             2.0.0
gruut-lang-fr             2.0.2
gruut-lang-it             2.0.0
gruut-lang-nl             2.0.2
gruut-lang-pt             2.0.0
gruut-lang-ru             2.0.0
gruut-lang-sv             2.0.0
gTTS                      2.4.0
httplib2                  0.22.0
huggingface-hub           0.17.1
humanfriendly             10.0
idna                      2.10
imageio                   2.31.3
importlib-metadata        6.8.0
importlib-resources       6.0.1
inflect                   5.6.0
ipython                   8.16.1
itsdangerous              2.1.2
jamo                      0.4.1
jedi                      0.19.1
jieba                     0.42.1
Jinja2                    3.1.2
jmespath                  1.0.1
joblib                    1.3.2
jsonlines                 1.2.0
jsonmerge                 1.9.2
jsonschema                4.19.0
jsonschema-specifications 2023.7.1
k-diffusion               0.0.16
keyboard                  0.13.5
kiwisolver                1.4.5
kornia                    0.7.0
langchain                 0.0.287
langsmith                 0.0.36
lazy_loader               0.3
librosa                   0.8.0
llvmlite                  0.38.1
Markdown                  3.4.4
MarkupSafe                2.1.3
marshmallow               3.20.1
matplotlib                3.7.3
matplotlib-inline         0.1.6
mecab-python3             1.0.5
menuinst                  1.4.16
mpmath                    1.3.0
msgpack                   1.0.5
multidict                 6.0.4
mypy-extensions           1.0.0
networkx                  2.8.8
nltk                      3.8.1
num2words                 0.5.12
numba                     0.55.1
numexpr                   2.8.6
numpy                     1.26.1
oauthlib                  3.2.2
onnxruntime               1.15.1
openai                    0.28.0
packaging                 23.1
pandas                    1.4.4
parso                     0.8.3
pathtools                 0.1.2
pickleshare               0.7.5
Pillow                    10.0.1
pip                       23.2.1
platformdirs              3.10.0
pooch                     1.6.0
prompt-toolkit            3.0.39
protobuf                  3.19.6
psutil                    5.9.5
pure-eval                 0.2.2
py-marytts                0.1.4
pyasn1                    0.5.0
pyasn1-modules            0.3.0
PyAudio                   0.2.13
pycosat                   0.6.3
pycparser                 2.20
pydantic                  2.4.2
pydantic_core             2.10.1
Pygments                  2.16.1
pynndescent               0.5.10
pyOpenSSL                 20.0.1
pyparsing                 3.1.1
pypinyin                  0.49.0
pyreadline3               3.4.1
pysbd                     0.3.4
PySocks                   1.7.1
python-crfsuite           0.9.9
python-dateutil           2.8.2
python-dotenv             1.0.0
pytz                      2023.3.post1
PyWavelets                1.4.1
pywin32                   228
pyworld                   0.3.0
PyYAML                    6.0.1
referencing               0.30.2
regex                     2023.8.8
requests                  2.31.0
requests-oauthlib         1.3.1
resampy                   0.4.2
resize-right              0.0.2
rpds-py                   0.10.3
ruamel-yaml-conda         0.15.100
s3transfer                0.7.0
safetensors               0.3.3
scikit-image              0.21.0
scikit-learn              1.3.0
scipy                     1.11.3
sentry-sdk                1.31.0
setproctitle              1.3.2
setuptools                68.2.2
six                       1.16.0
smmap                     5.0.1
soundfile                 0.12.1
soxr                      0.3.6
SQLAlchemy                2.0.20
stack-data                0.6.3
suno-bark                 0.0.1a0
sympy                     1.12
tenacity                  8.2.3
tensorboard               2.14.0
tensorboard-data-server   0.7.1
tensorboardX              2.6
threadpoolctl             3.2.0
tifffile                  2023.9.18
tokenizers                0.13.3
torch                     2.0.1
torchaudio                2.0.2
torchdiffeq               0.2.3
torchsde                  0.2.5
torchvision               0.15.2
tqdm                      4.64.1
trainer                   0.0.20
traitlets                 5.12.0
trampoline                0.1.2
transformers              4.33.2
TTS                       0.10.0
typing_extensions         4.7.1
typing-inspect            0.9.0
tzdata                    2023.3
tzlocal                   5.0.1
umap-learn                0.5.1
Unidecode                 1.3.6
unidic-lite               1.0.8
uritemplate               4.1.1
urllib3                   1.26.16
wandb                     0.15.10
watchdog                  3.0.0
wcwidth                   0.2.6
webrtcvad                 2.0.10
websockets                12.0
Werkzeug                  2.3.7
wheel                     0.41.2
win-inet-pton             1.1.0
wincertstore              0.2
yarl                      1.9.2
zipp                      3.17.0
