import os

PATH_PREFIX = 'Transformer/Learning/Algorithm/DL/NLP/Transformer'

N_LAYERS = 4
WORD_VEC_DIM = 128
N_HEADS = 2
UNITS = 32
DROP = 0.1

EPOCHS = 100000
MAX_SL = 20
MIN_SL = 0

# SAVE_PERIOD
TGT_VOC_SIZE = 1024 * 4
DATA_BUFFER_SIZE = 10240

# TOK_PATH = 'Save/Chat/tokenizer'
# TOK_PATH = 'Save/Chat_CN/tokenizer'
# TOK_PATH = 'Save/Translate/tokenizer'
TOK_PATH = 'Save/StableDiffusion/tokenizer'
# WGT_PATH = 'Save/Chat/bot_4'
# WGT_PATH = 'Save/Chat_CN/bot_4'
# WGT_PATH = 'Save/Translate/bot_4'
WGT_PATH = 'Save/StableDiffusion/bot_4'

TOK_PATH = os.path.join(PATH_PREFIX, TOK_PATH)
WGT_PATH = os.path.join(PATH_PREFIX, WGT_PATH)

SET_TCOUNT = 512
# TCOUNT = TRAIN_COUNT
SET_BS = 128
# BS = BATCH_SIZE
