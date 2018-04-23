import numpy as np
import tensorflow as tf
import pickle
from konlpy.tag import Twitter
import os
import jpype


class Quence():
    def __init__(self):
        self.BASE = os.path.dirname(os.path.abspath(__file__))
        self.vocab_to_int = self.import_file('data/vocab_to_int.txt')
        self.int_to_vocab = self.import_file('data/int_to_vocab.txt')
        self.result = []

    def import_file(self, fname):
        f = open(os.path.join(self.BASE, fname), 'rb')
        obj = pickle.load(f)
        f.close()

        return obj

    def clean_sentence(self, text):
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()

        Twit = Twitter()
        tagged = []
        for word, tag in Twit.pos(text):
            if (tag != 'Punctuation') and (tag != 'Foreign') and (tag != 'Alpha') and (tag != 'Number') and (
                    tag != 'Unkown') and (tag != 'Hashtag') and (tag != 'ScreenName') and (tag != 'Email') and (
                    tag != 'URL'):
                tagged.append((word, tag))

        return tagged

    def text_to_seq(self, text):

        converted_text = []
        '''Prepare the text for the model'''

        text = self.clean_sentence(text)
        for word in text:
            converted_text.append(self.vocab_to_int.get(word, self.vocab_to_int[('<UNK>', 'Code')]))

        return converted_text

    def pick_answers(self, logits):
        answers = []
        not_allowed = [value for key, value in self.vocab_to_int.items() if key[1] in ('Josa', 'Eomi')]
        pad = self.vocab_to_int[("<PAD>", 'Code')]
        answer_cnt = 3
        threshold = 3

        for logit in logits:
            if len(answers) >= answer_cnt:
                break

            # 문장 맨 첫글자 not_allowed 인지 여부 확인
            if logit[0] not in not_allowed:
                temp = [i for i in logit if i != pad]
                # pad 제외하고 포함된 단어의 개수가 threshold보다 큰 문장만 추출
                if len(temp) > threshold:
                    answers.append(temp)

        return answers

    def print_answer(self, answer):
        prev_vocab, prev_pos = self.int_to_vocab[answer[0]]
        result = prev_vocab

        for i in answer[1:]:
            vocab, pos = self.int_to_vocab[i]

            if pos in ('Josa', 'Eomi'):
                result = result + vocab + ' '
            elif pos == 'Noun' and prev_pos in ('Adjective', 'Adverb', 'Verb'):
                result = result + ' ' + vocab
            elif pos in ('Noun', 'Adjective', 'Adverb', 'Verb') and pos == prev_pos:
                result = result + ' ' + vocab
            elif prev_pos == 'Noun' and pos in ('Adjective', 'Adverb', 'Verb'):
                result = result + ' ' + vocab
            elif prev_pos in ('Adverb', 'Adjective', 'Verb') and pos not in ('Josa', 'PreEomi', 'Eomi'):
                result = result + ' ' + vocab
            else:
                result = result + vocab

            prev_pos = pos

        return result

    def call_tf(self, input):
        batch_size = 64
        checkpoint = os.path.join(self.BASE, "data/rainy_day_lr0.005.ckpt")
        input_text = self.text_to_seq(input)

        loaded_graph = tf.Graph()
        with tf.Session(graph=loaded_graph) as sess:
            # Load saved model
            loader = tf.train.import_meta_graph(checkpoint + '.meta')
            loader.restore(sess, checkpoint)

            input_data = loaded_graph.get_tensor_by_name('input:0')
            logits = loaded_graph.get_tensor_by_name('predictions:0')
            text_length = loaded_graph.get_tensor_by_name('text_length:0')
            summary_length = loaded_graph.get_tensor_by_name('summary_length:0')
            keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')

            # Multiply by batch_size to match the model's input parameters
            answer_logits = sess.run(logits, {input_data: [input_text] * batch_size,
                                              summary_length: [np.random.randint(10, 20)],
                                              text_length: [len(input_text)] * batch_size,
                                              keep_prob: 1.0})

        answers = self.pick_answers(answer_logits)

        for option in answers:
            self.result.append(self.print_answer(option))

        return self.result