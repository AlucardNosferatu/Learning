import pickle

import tensorflow as tf

from model_inst import instance, model_spec
from tokenizer import source_data, target_data, target_labels

batch_size = 5
EPOCHS = 200
crossentropy = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)


def calc_loss(targets, logits):
    mask = tf.math.logical_not(tf.math.equal(targets, 0))
    mask = tf.cast(mask, dtype=tf.int64)
    return crossentropy(targets, logits, sample_weight=mask)


@tf.function  # remove this annotation when debugging
def train_step(model2train, src_seq, tgt_seq, tgt_labels):
    with tf.GradientTape() as tape:
        logits = model2train([src_seq, tgt_seq], training=True)  # Set training=True to use dropout in training
        loss = calc_loss(tgt_labels, logits)

    variables = model2train.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))
    return loss


dataset = tf.data.Dataset.from_tensor_slices((source_data, target_data, target_labels)).batch(batch_size)
optimizer = tf.keras.optimizers.Adam()
config_file = open('Save/config.pkl', 'wb')
pickle.dump(model_spec, config_file)
for epoch in range(EPOCHS):
    loss_batch = 999.9
    for batch, (source_seq, target_seq, target_labels) in enumerate(dataset):
        loss_batch = train_step(instance, source_seq, target_seq, target_labels)
    if epoch % 10 == 0:
        print("Epoch #%d, Loss %.4f" % (epoch, loss_batch))
        # input_sent, target_sent, translation = translate()
        # print("Input: %s\nTarget: %s\nTranslation: %s\n" % (input_sent, target_sent, translation))
        instance.save_weights('Save/instance_' + str(epoch) + '.h5')
    if epoch % 100 == 0:
        print('覆盖保存到最新的权重文件，当前epoch', epoch)
        instance.save_weights('Save/instance.h5')
