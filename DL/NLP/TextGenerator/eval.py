from config import noise_dim, weight_path, num_classes
from model.CGAN import ConditionalGAN
from model.discriminator import spawn_d
from model.generator import spawn_g
from utils import get_noise_with_condition, convert_array

cond_gan = ConditionalGAN(
    discriminator=spawn_d(),
    generator=spawn_g(),
    latent_dim=noise_dim
)
random_vector_labels = get_noise_with_condition(list(range(num_classes)))
cond_gan.load_weights(weight_path)
generated_images = cond_gan.generator.predict(random_vector_labels)
res, w2v = convert_array(generated_images)
print(res)