from flask import Blueprint
from src import db
from src.services.chatgpt_service import chat_gpt
from src.models.document_model import Document
from src.models.user_model import User
from src.models.subscription_model import Subscription
import random
import re
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from src.utils import *
from src.services.pinecone_service import recommend_references
import ast

# essay controller blueprint to be registered with api blueprint
essays = Blueprint("essays", __name__)

"""
Params
- essay_title (String)
- num_of_words (int) [500, 750, 1000, 1500, 2000, 3000, 5000]
- citation (String) ["No Citation", "MLA", "APA", "Harvard", "Oxford"]
- level (String) ["High School", "College", "Master", "Doctoral"]
- essay_type (String) ["Generic", "Research", "Admission", "Analytical", "Argumentive", "Biography"]
- language (String) ["English", "French", "Spanish", "Slovenian", "German", "Portugese"]
- instructions (String)
"""                  
# Generate Eassy
def generate_essay(socketio, user_id, data, sid):
    try:
        num_of_words = int(data["num_of_words"])
        if num_of_words == 500:
            num_of_references = 5
            num_of_sections = 5
            num_per_subsection = 100
        if num_of_words == 1000:
            num_of_references = 7
            num_of_sections = 5
            num_per_subsection = 66
        if num_of_words == 1500:
            num_of_references = 10
            num_of_sections = 5
            num_per_subsection = 100
        if num_of_words == 2000:
            num_of_references = random.randint(13, 15)
            num_of_sections = 5
            num_per_subsection = 100
        if num_of_words == 3000:
            num_of_references = random.randint(20,25)
            num_of_sections = 7
            num_per_subsection = 107
        if num_of_words == 5000:
            num_of_references = random.randint(33,37)
            num_of_sections = 12
            num_per_subsection = 104
            
        essay_title = data['essay_title']
        citation = data['citation']
        instructions = data['instructions']
        language = data['language']
        level = data['level']
        essay_type = data['essay_type']
        
        generated_essay = {}
        generated_essay['title'] = essay_title
        generated_essay['sections'] = []        
        
        user_obj = User.query.get(user_id)
        subscription_obj = Subscription.query.filter_by(user_id = user_id).first()
        
        document_obj = Document(
                    title = essay_title,
                    available_sentences = 0,
                    content = generated_essay,
                    user = user_obj
                )
        db.session.add(document_obj)
        db.session.commit()
        
        generated_essay['id'] = document_obj.id
        
        socketio.emit("get-essay", {
            'status': 0,
            'quotaUsage': subscription_obj.quota_usage,
            'essay': generated_essay
        }, to=sid)
        
        socketio.sleep(1)
        # reference_prompt = f"Write {num_of_references} references for an essay with the title \"{essay_title}\" in {citation} citation format then each reference must include only Author, Title, Publisher and Year of Publication. Don't number and don't include any symbol at first of each reference. Don't include your unnecessary descriptions. {instructions}."
        # references = chat_gpt(reference_prompt, model="gpt-4")
        references = recommend_references(essay_title, num_of_references)
        print(references)
        reference_array = []
        references_result = []
        for reference in references:
            parsed_data = ast.literal_eval(reference["authors_parsed"])
            authors = []
            for author in parsed_data:
                authors.append(f"{author[1]} {author[0]}")
            author_str = ', '.join(authors)
            references_result.append({
                # "link": f"https://arxiv.org/abs/{reference["id"]}",
                "link": f"https://arxiv.org/abs/{reference['id']}",
                "title": reference["title"],
                "year": reference["update_date"],
                "author": author_str
            })
            reference_array.append(f"{author_str}. {reference['title']}, {reference['update_date']}")
            
        # references = [item.strip() for item in re.split(r'\\|\n', references) if item]
        # references_result = []
        # for reference in references:
        #     if len(reference) == 0:
        #         continue
        #     else:
        #         if citation == "APA":
        #             res = extract_info_apa(reference)
        #             if res is not None:
        #                 references_result.append(res)
        #         elif citation == "MLA":
        #             res = extract_info_mla(reference)
        #             if res is not None:
        #                 references_result.append(res)
        #         elif citation == "Harvard":
        #             res = extract_info_harvard(reference)
        #             if res is not None:
        #                 references_result.append(res)
        #         elif citation == "Oxford":
        #             res = extract_info_oxford(reference)
        #             if res is not None:
        #                 references_result.append(res)
                        
        generated_essay['reference_result'] = references_result
        outline_prompt = f"Generate the outline of the essay with the title \"{essay_title}\" excluding references. Do include exactly {num_of_sections} sections and 3 subsections under each section. Generate in {language}. Academic level is {level} and essay type is {essay_type}. Include only sections and subsections. Don't include sub-subsections. {instructions}. Don't include your unnecessary descriptions."
        outline = chat_gpt(prompt=outline_prompt, model="gpt-4")
        
        line_list = [item.strip() for item in outline.splitlines() if item]
        section_count = 0
        is_limited = False
        socketio.sleep(1)
        
        for line_index, line in enumerate(line_list):
            if line_index % 4 == 0:
                section_title = line
                section_content_array = []
                summarize_content= ''
                if num_of_words >= 2000 or num_of_words == 500:
                    section_prompt = f"Write around {num_per_subsection} words of content for the section with the title \'{essay_title}\' and the subtitle \'{section_title}\'.\n\n Write in {language}.\n - Academic level is {level} and essay type is {essay_type}.\n - Don't include title and subtitle.\n - Don't include your description and unnecessary content. {instructions}."
                    section_content = chat_gpt(prompt=section_prompt)
                    summarize_prompt = f"Write key insights of below content in 2 or 3 sentences.\n\n Content: {section_content}"
                    summarize_content = chat_gpt(prompt=summarize_prompt)
                    
                    section_content_sentences = sent_tokenize(section_content)
                    section_content_length = len(section_content_sentences)
                    citation_count = random.randint(1, 2)
                    selected_values = random.sample(list(range(section_content_length)), citation_count)
                    for index in range(section_content_length):
                        if section_count == 0:
                            section_content_array.append({
                                "sentence": section_content_sentences[index],
                                "citation": -1
                            })                  
                        else:
                            if index in selected_values:
                                citiation_index = random.randint(0, len(references_result) - 1)
                                section_content_array.append({
                                    "sentence": section_content_sentences[index],
                                    "citation": citiation_index
                                })
                            else:
                                section_content_array.append({
                                    "sentence": section_content_sentences[index],
                                    "citation": -1
                                })                  
                    
                    if subscription_obj.type == "FREE" and is_limited == False:
                        if subscription_obj.quota_usage >= int(os.environ.get('WORDS_LIMITATION')):
                            socketio.emit("get-essay", {
                                'status': 1,
                                'quotaUsage': subscription_obj.quota_usage,
                                'essay': generated_essay
                            }, to=sid)
                            is_limited = True
                        else:
                            document_obj.available_sentences = document_obj.available_sentences + section_content_length
                            if (subscription_obj.quota_usage + len(word_tokenize(section_content))) > int(os.environ.get('WORDS_LIMITATION')):
                                subscription_obj.quota_usage = int(os.environ.get('WORDS_LIMITATION'))
                            else:
                                subscription_obj.quota_usage = subscription_obj.quota_usage + len(word_tokenize(section_content))
                            db.session.commit()
                    section_count = section_count + 1
                        
                    # humanized_section_content, score = get_humanized_text(section_content)
                generated_essay['sections'].append({
                    'section_title': section_title,
                    'section_content': section_content_array,
                    'subsections': [],
                    'summarize_content': summarize_content
                })
                    
                if subscription_obj.type == "UNLIMITED" or (subscription_obj.type == "FREE" and is_limited == False):
                    socketio.emit("get-essay", {
                        'status': 0,
                        'quotaUsage': subscription_obj.quota_usage,
                        'essay': generated_essay
                    }, to=sid)
                            
            elif num_of_words > 500:
                subsection_title = line
                subsection_prompt = f"Write around {num_per_subsection} words of content for the subsection with the title \'{essay_title}\' and section \'{section_title}\' and subsection \'{subsection_title}\'. \n\n - Write in {language}.\n - Academic level is {level} and essay type is {essay_type}.\n - Don't include title, section titile and subsection title. \n - Don't include your description and unnecessary content. {instructions}"
                subsection_content = chat_gpt(prompt=subsection_prompt)
                summarize_prompt = f"Write key insights of below content in 2 or 3 sentences.\n\n Content: {subsection_content}"
                summarize_content = chat_gpt(prompt=summarize_prompt)
                # humanized_subsection_content, score = get_humanized_text(subsection_content)
                subsection_content_array = []
                subsection_content_sentences = sent_tokenize(subsection_content)
                subsection_content_length = len(subsection_content_sentences)
                citation_count = random.randint(1, 2)
                selected_values = random.sample(list(range(subsection_content_length)), citation_count)
                
                for index in range(subsection_content_length):
                    if section_count == 1:
                        subsection_content_array.append({
                            "sentence": subsection_content_sentences[index],
                            "citation": -1
                        })
                    else:
                        if index in selected_values:
                            citiation_index = random.randint(0, len(references_result) - 1)
                            subsection_content_array.append({
                                "sentence": subsection_content_sentences[index],
                                "citation": citiation_index
                            })
                        else:
                            subsection_content_array.append({
                                "sentence": subsection_content_sentences[index],
                                "citation": -1
                            })
                        
                if subscription_obj.type == "FREE" and is_limited == False:
                    if subscription_obj.quota_usage >= int(os.environ.get('WORDS_LIMITATION')):
                        socketio.emit("get-essay", {
                            'status': 1,
                            'quotaUsage': subscription_obj.quota_usage,
                            'essay': generated_essay
                        }, to=sid)
                        is_limited = True
                    else:
                        document_obj.available_sentences = document_obj.available_sentences + len(sent_tokenize(section_content))
                        if (subscription_obj.quota_usage + len(word_tokenize(section_content))) > int(os.environ.get('WORDS_LIMITATION')):
                            subscription_obj.quota_usage = int(os.environ.get('WORDS_LIMITATION'))
                        else:
                            subscription_obj.quota_usage = subscription_obj.quota_usage + len(word_tokenize(section_content))
                        db.session.commit()
                        
                generated_essay['sections'][section_count - 1]['subsections'].append({
                    'subsection_title': subsection_title,
                    'subsection_content': subsection_content_array,
                    'summarize_content': summarize_content
                })
                
                if subscription_obj.type == "UNLIMITED" or (subscription_obj.type == "FREE" and is_limited == False):
                    socketio.emit("get-essay", {
                        'status': 0,
                        'quotaUsage': subscription_obj.quota_usage,
                        'essay': generated_essay
                    }, to=sid)
                    
            document_obj.content = generated_essay
            db.session.commit()
            socketio.sleep(1)
            
        generated_essay['references'] = reference_array
        document_obj.content = generated_essay
        document_obj.status = True
        db.session.commit()
        socketio.sleep(1)
        
        if subscription_obj.type == "UNLIMITED" or (subscription_obj.type == "FREE" and is_limited == False):
            socketio.emit("get-essay", {
                'status': 2,
                'quotaUsage': subscription_obj.quota_usage,
                'essay': generated_essay
            }, to=sid)
        
    except Exception as e:
        print(e)
