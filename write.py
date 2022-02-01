with open('words.txt', 'r') as words:
    old_words = [word[:-1] for word in words]
    new_words = []
    for word in old_words:
        if len(word) == 5:
            new_words.append(word)

with open('wordle_list.txt', 'w') as word_list:
    for word in new_words:
        word_list.write(f"{word}\n")
