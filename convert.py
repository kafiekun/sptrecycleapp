import tensorflow as tf
model = tf.keras.models.load_model('./Model/keras_model.h5')
tf.saved_model.save(model, 'saved_model_dir/variables')