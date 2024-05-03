
import os
os.environ["KERAS_BACKEND"] = "torch"

import keras
from keras import layers




imageSize = (800,800)
batchSize = 100

f = open("altitues.txt",'r')

lines = f.readlines()
labelList = [int(x) for x in lines]
f.close()


trainData, testData = keras.utils.image_dataset_from_directory(
    "./imgs",
    tuple(labelList),
    "int",
    validation_split=0.2,
    subset="both",
    seed = 25,
    image_size=imageSize,
    batch_size=batchSize
)


def generateMod(inputShape) -> keras.Model:
    inputs = keras.Input(shape=inputShape)

    x = layers.Rescaling(1./255)(inputs)
    x = layers.Conv2D(512, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)

    for size in [128, 256]:
        
        x = layers.SeparableConv2D(size, 3, padding='same')(x)
        x = layers.BatchNormalization()(x)\
        x = layers.Activation('relu')(x)

        x = layers.MaxPool2D(3, strides=2, padding='same')(x)

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dropout(0.18)(x)
    out = layers.Dense(36, activation=None)(x)
    
    return keras.Model(inputs, out)

epochs = 500

callbacks = [keras.callbacks.ModelCheckpoint("save_at_{epoch}.keras")]
model = generateMod(imageSize)

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=keras.losses.CategoricalCrossentropy(from_logits=True),
    metrics = [
                keras.metrics.CategoricalAccuracy(name='acc'), 
                keras.metrics.F1Score(name='F1')
               ]
)

model.fit(
    trainData,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=testData
)
