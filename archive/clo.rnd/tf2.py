import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from archive.training_sample import Sample


def load_data():
    (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
    # Scale input in [-1, 1] range
    train_x = tf.expand_dims(train_x, -1)
    train_x = (tf.image.convert_image_dtype(train_x, tf.float32) - 0.5) * 2
    train_y = tf.expand_dims(train_y, -1)
    test_x = test_x / 255. * 2 - 1
    test_x = (tf.image.convert_image_dtype(test_x, tf.float32) - 0.5) * 2
    test_y = tf.expand_dims(test_y, -1)

    return (train_x, train_y), (test_x, test_y)


def make_model(n_classes):
    return tf.keras.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation=tf.nn.relu, input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPool2D((2, 2), (2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
        tf.keras.layers.MaxPool2D((2, 2), (2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(n_classes)
    ])


def propose_syllabus(dataset):
    sorted = []
    for features, labels in dataset:
        features_np = features.numpy()
        labels_np = labels.numpy()
        sample = Sample(features_np, labels)
        entropy = sample.entropy


def train_dataset(batch_size=32, num_epochs=1):
    (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
    input_x, input_y = train_x, train_y

    def scale_fn(image, label):
        return (tf.image.convert_image_dtype(image,
                                             tf.float32) - 0.5) * 2.0, label

    dataset = tf.data.Dataset.from_tensor_slices((tf.expand_dims(input_x, -1),
                                                  tf.expand_dims(input_y, -1))).map(scale_fn)
    propose_syllabus(dataset)
    dataset = dataset.cache().repeat(num_epochs)
    dataset = dataset.shuffle(batch_size)
    batch = dataset.batch(batch_size)

    # TODO - preprocess batch

    tf.print("Fetching batch of size of ", batch_size)

    return batch.prefetch(1)


def train():
    # Define the model
    n_classes = 10
    model = make_model(n_classes)

    # Input data
    dataset = train_dataset(num_epochs=10)

    # Training parameters
    loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)
    step = tf.Variable(1, name="global_step")
    optimizer = tf.optimizers.Adam(1e-3)
    accuracy = tf.metrics.Accuracy()
    loss_value = None

    # Train step function
    @tf.function
    def train_step(inputs, labels):
        with tf.GradientTape() as tape:
            logits = model(inputs)
            loss_value = loss(labels, logits)

        gradients = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        step.assign_add(1)
        accuracy_value = accuracy(labels, tf.argmax(logits, -1))

        return loss_value, accuracy_value

    @tf.function
    def loop():
        for features, labels in dataset:
            lossvalue, accuracy_value = train_step(features, labels)
            if tf.equal(tf.math.mod(step, 10), 0):
                tf.print(step, ": ", lossvalue, " - accuracy: ", accuracy_value)

    loop()


if __name__ == '__main__':
    train()
