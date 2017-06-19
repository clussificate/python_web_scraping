sttr = "\" i am a doctor \"     but w" \
       "you are "
print(sttr)
fsttr = sttr.replace('\t', '').replace('\n', '').replace(' ', '').replace('\"', '')
print(fsttr)