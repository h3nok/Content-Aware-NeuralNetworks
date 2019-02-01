
import numpy as np
import tensorflow as tf
try:
    from cc.ITT import itt as itt
except(Exception, ImportError) as error:
    from ITT import itt as itt


def JointEntropyTF(patch_1, patch_2):

    assert patch_1.shape == patch_2.shape, "Patches must have similar tensor shapes of [p_w, p_h, c]"
    assert patch_1 != patch_2, "Patches are binary equivalent, Distance = 0"

    sess = tf.get_default_session()

    # combine the two tensors into one
    patch_data = sess.run(
        tf.concat([patch_1,
                   patch_2], 0))
    # flatten the tensor into a sigle dimensinoal array
    patch_data = sess.run(tf.reshape(patch_data, [-1]))

    je = round(itt.entropy_joint(patch_data), 4)  # result x.xxxx

    return je


def JointEntropy(patch_1, patch_2):

    assert isinstance(patch_1, np.ndarray), "Patch data must be a numpy array."
    assert isinstance(patch_2, np.ndarray), "Patch data must be a numpy array."
    assert patch_1.shape == patch_2.shape, "Patches must have similar tensor shapes of [p_w, p_h, c]"
    assert not np.array_equal(
        patch_1, patch_2), "Patches are binary equivalent, Distance = 0"

    # combine the two tensors into one
    # and flatten the tensor into a sigle dimensinoal array
    patch_data = np.concatenate((patch_1, patch_2)).flatten()

    je = round(itt.entropy_joint(patch_data), 4)  # result x.xxxx

    return je
