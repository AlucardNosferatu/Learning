from Model.Transformer import TransformerModel

# Model parameters
d_model = 64  # 512 in the original paper
d_k = 16  # 64 in the original paper
d_v = 16  # 64 in the original paper
n_heads = 4  # 8 in the original paper
n_encoder_layers = 2  # 6 in the original paper
n_decoder_layers = 2  # 6 in the original paper
max_token_length = 20  # 512 in the original paper
dropout = .1
model_spec = {
    'n_heads': n_heads,
    'd_v': d_v,
    'd_k': d_k,
    'd_model': d_model,
    'max_token_length': max_token_length,
    'n_encoder_layers': n_encoder_layers,
    'n_decoder_layers': n_decoder_layers,
    'dropout': dropout
}

instance = TransformerModel(
    n_heads=n_heads,
    d_v=d_v,
    d_k=d_k,
    d_model=d_model,
    max_token_length=max_token_length,
    n_encoder_layers=n_encoder_layers,
    n_decoder_layers=n_decoder_layers,
    dropout=dropout
)
