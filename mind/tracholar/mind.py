

class Model_ComiRec_SA(tf.keras.Model):
    """
    self-att
    """

    def __init__(self, caps_dim, num_interest, seq_len=256, add_pos=False, hard_readout=True, relu_layer=True):
        super(Model_ComiRec_SA, self).__init__()

        self.caps_dim = caps_dim
        self.caps_num = num_interest
        self.seq_len = seq_len
        self.add_pos = add_pos
        self.hard_readout = hard_readout
        self.relu_layer = relu_layer  #

    def call(self, inputs):
        """
        :param hist_embs:       历史行为emb，shape = (batch_size, seq_len, dim0) # item hist, d-8
        :param item_emb:        正样本emb, shape = (batch_size, dim1)  # item fea, d-32
        :param hist_mask:       shape = (batch_size, len)
        :param other_feas:      shape=(batch_size, dim2)    # user fea, d-32
        :return:
        """
        hist_embs, item_emb, hist_mask, other_feas = inputs
        hist_dim = hist_embs.shape[-1]

        if self.add_pos:
            with tf.variable_scope("position", reuse=tf.AUTO_REUSE):
                position_embedding = tf.get_variable(
                    'position_embedding', [self.seq_len, hist_dim])  # 即建立一个len * dim的矩阵做为位置向量
            position_embedding = tf.expand_dims(position_embedding, axis=0) # (1, len, dim)
            item_list_add_pos = hist_embs + position_embedding
        else:
            item_list_add_pos = hist_embs

        num_heads = self.caps_num
        with tf.variable_scope("self_atten", reuse=tf.AUTO_REUSE) as scope:
            item_list_add_pos = tf.reshape(item_list_add_pos, [-1, hist_dim])   # (batch_sz*len, hist_dim)
            # 1. 历史输入做变换，ComiRec-eq6
            # (batch_sz, seq_len, dim * num_caps)
            item_hidden = add_fc(item_list_add_pos, self.caps_dim * 4, activation=tf.nn.tanh, name='att_w1')
            # (batch_sz, seq_len, num_heads)
            item_att_w = add_fc(item_hidden, num_heads, activation=None, name='att_w2')
            item_att_w = tf.reshape(item_att_w, [-1, self.seq_len, num_heads])
            # (batch_sz, num_heads, seq_len)
            item_att_w = tf.transpose(item_att_w, [0, 2, 1])

            # (batch_sz, num_heads, seq_len)
            atten_mask = tf.tile(tf.expand_dims(hist_mask, axis=1), [1, num_heads, 1])
            paddings = tf.ones_like(atten_mask) * (-2 ** 32 + 1)  # 空位置的权重赋予极小值

            item_att_w = tf.where(tf.equal(atten_mask, 0), paddings, item_att_w)
            item_att_w = tf.nn.softmax(item_att_w)  # 和capsule不同，这个是在seq_len层面上做权重归一

            # 2. 用户多兴趣，ComiRec-eq7
            # (batch_sz, num_heads, dim)
            interest_emb = tf.matmul(item_att_w, hist_embs)

        # 核心：(batch_sz, num_heads, dim), 每个用户的seq_len个历史行为，压缩为num_caps个用户兴趣
        interest_capsule = interest_emb
        with tf.variable_scope('relu_out', reuse=tf.AUTO_REUSE):
            if self.relu_layer:  # relu激活
                other_feas = tf.expand_dims(other_feas, axis=1)             # (batch_size, 1, dim2)
                other_feas = tf.tile(other_feas, [1, num_heads, 1]) # (batch_size, num_caps, dim2)
                interest_capsule = tf.concat([interest_capsule, other_feas], axis=2)    # (batch_sz, num_caps, dim+dim2)
                interest_capsule = tf.reshape(interest_capsule, [-1, interest_capsule.shape[-1]])
                interest_capsule = add_fc(interest_capsule, self.caps_dim, activation=tf.nn.relu, name='proj')
                interest_capsule = tf.reshape(interest_capsule, [-1, num_heads, self.caps_dim])

        # 后续：使用正样本对num_caps个用户兴趣做att， xMIND-3.4节
        # 即num_caps个用户兴趣分到权重后组合，得到最终用户单向量的兴趣表达
        atten = tf.matmul(interest_capsule, tf.reshape(item_emb, [-1, self.caps_dim, 1]))  # (batch_sz, num_caps, 1)
        atten = tf.nn.softmax(tf.pow(tf.reshape(atten, [-1, num_heads]), 1))  # (batch_sz, num_caps)

        # final usr vec, readout.shape=(batch_sz, dim)
        if self.hard_readout:
            # 只取caps权重最大的那个vec
            readout = tf.gather(tf.reshape(interest_capsule, [-1, self.caps_dim]),  # (batch_sz * num_caps, dim)
                                tf.argmax(atten, axis=1, output_type=tf.int32) +  # (batch_sz,)
                                tf.range(tf.shape(hist_embs)[0]) * num_heads)  # (batch_sz,)
        else:
            # 每个caps都做贡献
            readout = tf.matmul(tf.reshape(atten, [-1, 1, num_heads]), interest_capsule)
            readout = tf.reshape(readout, [-1, self.caps_dim])

        return interest_capsule, readout

