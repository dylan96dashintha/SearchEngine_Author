from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json,re,os
import advanced_queries
client = Elasticsearch(HOST="http://localhost",PORT=9200)
INDEX = 'book-author-index'


synonym_writer = ['රචකයා','ගත්කතුවරයා','ලියනා','ලියූ','ලියන','ලියපු']
# synonym_lyrics = ['ගත්කරු','රචකයා','ලියන්නා','ලියන','රචිත','ලියපු','ලියව්‌ව','රචනා','රචක','ලියන්','ලියූ']
synonym_writer_eng = ['writer','write','wrote','writer','author']
# synonym_music = ['සංගීත','සංගීතවත්','සංගීතය']
synonym_birth_place_eng = ['birthplace','town','country','place']
synonym_birth_date = ['උපන්දිනය','ජන්ම දිනය','උපන්','උපත ලද','උපත','මෙලොවට ආ','මෙලොව එළිය දුන්','එළිය දුටු','මෙලොවට','ඉපදුන', 'වන දින']
synonym_birth_place = ['තැන','ස්ථානය','ප්‍රදේශය', 'උපන්ගම', 'ගම','ප්‍රාන්තය', 'පළාත','රට']

synonym_list = [ synonym_writer, synonym_writer_eng, synonym_birth_date, synonym_birth_place, synonym_birth_place_eng]



def search(search_query):
    processed_query = ""
    tokens = search_query.split()
    processed_tokens = search_query.split()
    search_fields = []
    sort_num = 0
    field_list = ["author_name", "author_name_english", "date_of_birth", "birth_place", "birth_place_english"]
    all_fields = ["author_name", "date_of_birth", "birth_place", "book_list", "about_author", "category", "language", "author_name_english", "birth_place_english"]
    final_fields = []

    for word in tokens:
        print (word)

        #if (word in sinhala_popularity) or (word in english_popularity):
        # if (word in sinhala_popularity):
        #     processed_tokens.remove(word)
        #     print('Start sort by views')
        #     sort_num = 986

        if word.isdigit():
            sort_num = int(word)
            processed_tokens.remove(word)
            print ('Identified sort number',sort_num)

        for i in range(0, 5):
            if word in synonym_list[i]:
                print('Adding field', field_list[i], 'for ', word, 'search field list')
                search_fields.append(field_list[i])
                if (field_list[i] == "date_of_birth") :
                    search_fields.append(field_list[i-1])
                    
                if (field_list[i] == "author_name_english") :
                    search_fields.append(field_list[i-1])
                
                if (field_list[i] == "author_name") :
                    search_fields.append(field_list[i+1])
                
                if (field_list[i] == "birth_place") :
                    search_fields.append(field_list[i+1])

                if (field_list[i] == "birth_place_english") :
                    search_fields.append(field_list[i-1])
                # if(i%2==0):
                #     search_fields.append(field_list[i+1])
                # else:
                #     search_fields.append(field_list[i -1])
                processed_tokens.remove(word)

    if (len(processed_tokens)==0):
        processed_query = search_query
    else:
        processed_query = " ".join(processed_tokens)

    ###Boosting
    # for field in all_fields:
    #     if (field in search_fields):
    #         final_fields.append(field+"^5")
    #     else:
    #         final_fields.append(field)
    final_fields = search_fields

    #if (sort_num==0):
    print('Faceted Query')
    if(len(search_fields)==0):
        query_es = advanced_queries.multi_match_agg_cross(processed_query, all_fields)
    # elif (len(search_fields) == 2):
    #     query_es = advanced_queries.multi_match_agg_phrase(processed_query, final_fields)
    else:
        query_es = advanced_queries.multi_match_agg_cross(processed_query, final_fields)

    # else:
    #     print('Range Query')
    #     if (len(search_fields) == 0):
    #         query_es = advanced_queries.multi_match_agg_sort_cross(processed_query, sort_num, all_fields)
    #     elif (len(search_fields) == 2):
    #         query_es = advanced_queries.multi_match_agg_sort_phrase(processed_query, sort_num, all_fields)
    #     else:
    #         query_es = advanced_queries.multi_match_agg_sort_cross(processed_query, sort_num, final_fields)

    print("QUERY BODY")
    print(query_es)
    search_result = client.search(index=INDEX, body=query_es)
    return search_result





