import numpy as np
import pandas as pd
import datetime as dt
import os
import sys

## using GPU:1
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

from keras.models import Sequential, Model
from keras.layers import Input, Reshape, Dense, BatchNormalization, Flatten, UpSampling1D, Conv1D
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import SGD, Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import keras.backend.tensorflow_backend as K
from keras import initializers
from sklearn.preprocessing import StandardScaler


def generator_model():

    '''
    Building generator structure

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''

    generator = Sequential()
    generator.add(Dense(64*6, input_dim=latent_dim, kernel_initializer=initializers.RandomUniform(seed=100)))
    generator.add(LeakyReLU(0.2))
    generator.add(Reshape((6, 64)))
    generator.add(UpSampling1D(size=2))
    generator.add(Conv1D(32, kernel_size=3, padding='same'))
    generator.add(LeakyReLU(0.2))
    generator.add(UpSampling1D(size=2))
    generator.add(Conv1D(1, kernel_size=3, padding='same', activation='sigmoid')) 
    generator.add(Reshape((data_dim,1)))
    return generator


def discriminator_model():

    '''
    Building discriminator structure

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    discriminator = Sequential()
    discriminator.add(Conv1D(32, kernel_size=3, strides=1, input_shape=(data_dim,1), kernel_initializer=initializers.RandomUniform(seed=100)))
    discriminator.add(LeakyReLU(0.2))
    discriminator.add(BatchNormalization())
    discriminator.add(Conv1D(16, kernel_size=3, strides=1))
    discriminator.add(LeakyReLU(0.2))
    discriminator.add(BatchNormalization())
    discriminator.add(Flatten())
    discriminator.add(Dense(1, activation='sigmoid'))
    return discriminator


def generator_containing_discriminator(g, d):

    '''
    Building anoGAN structure
    - combining generator and discriminator

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    d.trainable = False
    ganInput = Input(shape=(latent_dim,))
    x = g(ganInput)
    ganOutput = d(x)
    gan = Model(inputs=ganInput, outputs=ganOutput)
    return gan
""" 
def train(epoch, BATCH_SIZE, X_train, sensor_type):

    '''
    Training anoGAN

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    d = discriminator_model()
    weights_file = '/daegu/weights/discriminator_' + sensor_type + '.h5'
    if os.path.exists(weights_file):
        d.load_weights(weights_file)
        print("Model loaded.")
    print("####### discriminator #######")
    d.summary()
    g = generator_model()
    weights_file = '/daegu/weights/generator_' + sensor_type + '.h5'
    if os.path.exists(weights_file):
        g.load_weights(weights_file)
        print("Model loaded.")
    print("####### generator #######")
    g.summary()
    
    d_on_g = generator_containing_discriminator(g, d)
    d_on_g.compile(loss='binary_crossentropy', optimizer='adam')
    d.compile(loss='binary_crossentropy', optimizer='adam')
    begin = dt.datetime.now()
    for epoch in range(epoch):
        print("Epoch is", epoch)
        e_begin = dt.datetime.now()
        for index in range(int(X_train.shape[0]/BATCH_SIZE)):
            noise = np.random.uniform(0, 1, size=(BATCH_SIZE, latent_dim))
            image_batch = X_train[index*BATCH_SIZE:(index+1)*BATCH_SIZE]
            generated_images = g.predict(noise, verbose=0)
            X = np.concatenate((image_batch, generated_images))
            y = np.array([1] * BATCH_SIZE + [0] * BATCH_SIZE)
            d_loss = d.train_on_batch(X, y)
            noise = np.random.uniform(0, 1, (BATCH_SIZE, latent_dim))
            d.trainable = False
            g_loss = d_on_g.train_on_batch(noise, np.array([1] * BATCH_SIZE))
            d.trainable = True
        print("   time :", dt.datetime.now() - e_begin, "discriminator loss : ", d_loss, "generator loss : ", g_loss)
        g.save_weights('/daegu/weights/generator_' + sensor_type + '.h5', True)
        d.save_weights('/daegu/weights/discriminator_' + sensor_type + '.h5', True)
    print("### training time : ", dt.datetime.now() - begin)
    return d, g """



def sum_of_residual(y_true, y_pred):
    '''
    RMSE loss

    '''
    return K.tf.reduce_sum(abs(y_true - y_pred))

def feature_extractor(sensor_type):
    '''
    Loading discriminator to extract intermediate layer's feature map.

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    d = discriminator_model()
    d.load_weights(os.getcwd() + "/resources/weight/discriminator_' + sensor_type + '.h5') 
    intermidiate_model = Model(inputs=d.layers[0].input, outputs=d.layers[-5].output)
    return intermidiate_model

def anomaly_detector(sensor_type):
    '''
    Building anomaly detector model to compute anomaly score.

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    g = generator_model()
    g.load_weights(os.getcwd() + "/resources/weight/generator_' + sensor_type + '.h5')
    g.trainable = False
    intermidiate_model = feature_extractor(sensor_type)
    intermidiate_model.trainable = False
    
    aInput = Input(shape=(data_dim,))
    gInput = Dense((latent_dim))(aInput)
    G_out = g(gInput)
    D_out= intermidiate_model(G_out)    
    model = Model(inputs=aInput, outputs=[G_out, D_out])
    adam = Adam(lr=0.1)

    model.compile(loss=sum_of_residual, loss_weights= [0.9, 0.1], optimizer=adam)
    return model

def compute_anomaly_score(x, sensor_type):
    model = anomaly_detector(sensor_type = sensor_type) 
    return _compute_anomaly_score(model, x, sensor_type)

def _compute_anomaly_score(model, x, sensor_type):
    '''
    Computing anomaly score.

    reference : https://arxiv.org/abs/1511.06434 - DCGAN 
    https://arxiv.org/abs/1703.05921 - anoGAN

    '''
    z = np.random.uniform(0, 1, size=(1, latent_dim))
    intermidiate_model = feature_extractor(sensor_type)
    d_x = intermidiate_model.predict(x)
    loss = model.fit(z, [x, d_x], epochs=500, verbose=0)
    similar_data, _ = model.predict(z)
    return loss.history['loss'][-1], similar_data


def mutiple_anomaly_score(data, sensor_type):
    '''
    1. standardizing data - mean : 0 , variance : 1

    2. building anomaly detector model and compute anomaly socre using the model
    - compute score for each sample
    - it takes a few seconds.

    return anomaly scores and gennerated data
    
    '''
    data = np.array(data)
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    
    anomaly_score_list = []
    gen_x_list = []
    for i in range(data.shape[0]):
        model = anomaly_detector(sensor_type = sensor_type) 
        x = data[i].reshape(1,24,1)
        loss, gen_x = compute_anomaly_score(model, x, sensor_type=sensor_type)  
        anomaly_score_list.append(loss)
        gen_x = np.reshape(np.array(gen_x), (-1,24))
        gen_x = scaler.inverse_transform(gen_x)
        gen_x_list.append(gen_x) 
        K.clear_session()
    return anomaly_score_list, gen_x_list

if __name__ == '__main__':
    if len(sys.argv) == 3:
        sensor_type_ = str(sys.argv[1])
        input_path = str(sys.argv[2])
        latent_dim = 24
        data_dim = 24

        dataX = pd.read_csv(input_path, sep=',', index_col=0, header=None, 
            names=('sensor_id', '0hr', '1hr', '2hr', '3hr', '4hr', '5hr', '6hr', '7hr', '8hr', '9hr', '10hr',
            '11hr', '12hr', '13hr', '14hr', '15hr', '16hr', '17hr', '18hr', '19hr', '20hr',
            '21hr', '22hr', '23hr'), na_values=[-999, -995, -991])
        sensors = (np.array(dataX.index)).reshape(-1, 1)

        ## -999, -995, -991 missing value 처리 
        dataX[dataX.isnull().all(axis=1)] = 0  # when a sensor's all values are nan.
        dataX = dataX.interpolate(axis=1)
        dataX = dataX.bfill(axis=1) 
        dataX = dataX.ffill(axis=1)
        dataX = np.array(dataX)

        anomaly_scores, gen_x = mutiple_anomaly_score(dataX, sensor_type= sensor_type_)
        anomaly_scores = np.array(anomaly_scores).reshape(-1, 1)
        anomaly_scores = np.concatenate((sensors, anomaly_scores), axis=1)
        gen_x = np.vstack(gen_x)
        gen_x = np.concatenate((sensors, gen_x), axis=1)
        print("score : ", anomaly_scores, " y_pred : ",gen_x)
        print("completed!")
    else :
        print("Error! Number of argv is not 3. ")