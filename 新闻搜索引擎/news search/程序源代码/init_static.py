import segmentation
import tool
import volsunga

word_flag_freq_dic = tool.get_freq_dic("./data/word_flag_freq_dic.txt")
flag_freq_dic = tool.get_freq_dic("./data/flag_freq_dic.txt")
flag_relation_freq_dic = tool.get_freq_dic("./data/flag_relation_freq_dic.txt")
word_flag_dic = tool.get_flag_dic("./data/chineseDic.txt")
v = volsunga.Volsunga(word_flag_freq_dic, flag_freq_dic, flag_relation_freq_dic, word_flag_dic)
s = segmentation.Segmentation()
