import numpy as np
import time

from keras.models import Sequential
from keras.layers import Dense


def make_model():
    model = Sequential()

    model.add(Dense(10, input_shape=(6,)))
    model.add(Dense(1))
    model.compile(optimizer='sgd', loss=['mean_absolute_error'], metrics=['accuracy'])

    return model


def online_training(X, y, chunk_size):
    model = make_model()
    chunks = X.shape[0] // chunk_size

    print ("Chunk size: {}".format(chunk_size))
    for i in range(chunks):
        print("--------------------------------------------------- ")
        print("Chunk: {}/{}".format(i+1, chunks))
        print("--------------------------------------------------- ")

        start = i * chunk_size
        end = start + chunk_size

        X_aux = X[start:end]
        y_aux = y[start:end]
        try:
            model.load_weights("weights/weights_chunks.hdf5")
        except:
            pass

        model.fit(X_aux, y_aux, epochs=20, batch_size=2)
        model.save_weights("weights/weights_chunks.hdf5")

    return model

def offline_training(X, y):
    model = make_model()
    model.fit(X, y, epochs=20, batch_size=2)
    return model


if __name__ == '__main__':
    X = np.loadtxt('data/X_train_right.txt', dtype=float)
    y = np.loadtxt('data/y_train_right.txt', dtype=float)
    chunk_size = 250

    # Offline training
    start_time = time.time()
    model_offline = offline_training(X, y)
    end_time = time.time()
    offline_time = end_time - start_time

    # Online training
    start_time = time.time()
    model_online = online_training(X, y, chunk_size)
    end_time = time.time()
    online_time = end_time - start_time

    print("")
    print("=========================================================")
    print("Online evaluate: {}".format(model_offline.evaluate(X, y)))
    print("Time elapsed: {}".format(online_time))
    print("--------------------------------------------------- ")
    print("Offline evaluate: {}".format(model_online.evaluate(X, y)))
    print("Time elapsed: {}".format(offline_time))
    print("=========================================================")


