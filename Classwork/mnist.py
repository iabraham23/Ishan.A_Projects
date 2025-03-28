import sklearn
import tensorflow as tf
import matplotlib
matplotlib.use('TkAgg') #for usage on mac
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist.load_data()

(X_train_full, y_train_full), (X_test, y_test) = mnist
X_train, y_train = X_train_full[:-5000], y_train_full[:-5000]
X_valid, y_valid = X_train_full[-5000:], y_train_full[-5000:]

#print(X_train.shape)
X_train, X_valid, X_test = X_train / 255., X_valid / 255., X_test / 255.

tf.random.set_seed(42)
model = tf.keras.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=[28, 28]))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(300, activation="relu"))
model.add(tf.keras.layers.Dense(100, activation="relu"))
model.add(tf.keras.layers.Dense(10, activation="softmax"))

#model.summary()

hidden1 = model.layers[1]

weights, biases = hidden1.get_weights()
#print(weights.shape)

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=30,
                    validation_data=(X_valid, y_valid))

print(model.evaluate(X_test, y_test)) #gets around 98% on the test set

#fine tune would be page 315 on online textbook 
