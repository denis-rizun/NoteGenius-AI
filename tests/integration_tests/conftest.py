# To ensure optimal performance, please avoid running all test functions simultaneously.
# The free-tier of ChatGPT has limitations in handling data summarization.
# Please execute separately (only related to endpoints).


# --------------------------------- endpoint's ---------------------------------
note_skip_create = True
note_skip_get = True
note_skip_gets = True
note_skip_update = True
note_skip_delete = True

skip_total_word_count = True
skip_average_note_length = True
skip_common_words = True
skip_longest_notes = True
skip_shortest_note = True


# --------------------------------- query's ---------------------------------
note_query_skip_create = True
note_query_skip_gets = True
note_query_skip_update = True
note_query_skip_delete = True


# --------------------------------- service's ---------------------------------
openai_skip_send_request = True
openai_skip_get_request = True