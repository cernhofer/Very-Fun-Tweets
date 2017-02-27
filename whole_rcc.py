### THIS IS JUST PSEUDO CODE

hashtags = db.tweets.all()
for hashtag in hashtags:
    if len(hashtag.tweets) < 1000: continue

    has_spike = sush_script(hashtag) # returns bool

    if has_spike:
        data = prepare_data(hashtag) # outputs a formatted data object
        data['stories'] = chelsea_script(hashtag)
        push_to_postgres(data)
    elif is_in_list():
        # have this push to postgres if hashtag is on list of previously pushed hashtags
        pass
