#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from six.moves.urllib import parse
import urllib
import requests
from lxml import html
import re
import json
from gglsbl import SafeBrowsingList
from wordcloud import WordCloud
import io
import matplotlib.pyplot as plt
import tldextract
import base64

def scrapper(url):
    
    if "www" in url:
        url = url.replace("www.","")
        print(url)
    else:
        pass

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    final_report = []
    final_score = 0
    from result_dict import result_dict

    domain =tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    subdomain = tldextract.extract(url).subdomain
    pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'


    # row 15 HTTPS test

    result = {
                'name':'https_test',
                'message':'',
                'marks':''
            }

    if "https" in url or "http" in url:
        print("if worked")
        
        try:
            a = url.split(":")
            a[0]  = "https:"
            web = "".join(a)
        except:
            pass 

        print("This is web  ",web)

        try:
            print("try of if worked")
            r = requests.get(web,headers=headers)
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = 'Félicitations. Votre site les données transitants par votre site sont sécurisées avec un certificat SSL'
            result['marks'] = 4
        except:
            try:
                a = url.split(":")
                a[0]  = "http:"
                url3 = "".join(a)
            except:
                pass 

            print("try of except worked")
            r = requests.get(url3,headers=headers,verify=False)
            url = url3
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = '''
            Votre site ne dispose pas de certificat SSL. Les données qui y transitent peuvent donc être récupérés par des parties malveillantes. Google donne une grande importance à la sécurité des visiteurs.
            '''
            result['marks'] = 0
            print("HTTPS didn't worked")

    else:
        print("else worked")
        try:
            url2 = 'https://'+url
            r = requests.get(url2,headers=headers)
            url = url2
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = 'Félicitations. Votre site les données transitants par votre site sont sécurisées avec un certificat SSL'
            result['marks'] = 4
            
            
        except:
            url1 = 'http://'+url
            print ("from else except ", url1)
            r = requests.get(url1,headers=headers,verify=False)
            url = url1
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = '''
                Votre site ne dispose pas de certificat SSL. Les données qui y transitent peuvent donc être récupérés par des parties malveillantes. Google donne une grande importance à la sécurité des visiteurs.
                '''
            result['marks'] = 0
            
            result_dict['https_test'] = result
            final_score = final_score + result['marks']

    soup = BeautifulSoup(r.text, "lxml")



    # This is for row 1 (title)
    try:
        title_content = soup.find('title').text
        title_ln =  len(title_content)
         
        if title_ln < 70:
            result = {
                'name':'title',
                'message':'Félicitations votre site dispose d’un titre avec un nombre de caractères optimale soit moins de 70 caractères',
                'title_length': title_ln,
                'title_content':title_content,
                'marks':5
            }
            final_score = final_score + 5
            result_dict['title'] = result
        elif title_ln > 70:
            result = {
                'name':'title',
                'message':'Votre titre est trop long, le nombre de caractères optimal est de 70 caractères, essayez de le raccourcir',
                'title_length': title_ln,
                'title_content':title_content,
                'marks':2
            }
            final_score = final_score + 2
            result_dict['title'] = result
    except:
        result = {
            'name':'title',
            'message':'Votre site ne dispose pas de balise meta title. La balise <title> correspond au titre de votre page web. Il s’agit d’un champ essentiel à ne pas négliger dans le cadre d’une bonne stratégie d’optimisation du référencement naturel puisqu’elle est l’un des critères les plus importants pour les moteurs de recherche (Google, Bing...)',
            'title_length': 0,
            'marks':0
        }
        final_score = final_score + 0
        result_dict['title'] = result



    # This is for row 2 (meta @description)
    name = 'meta_description'
    length_var_name = 'meta_desc_len'
    try:
        meta_tag  = soup.find("meta", {"name" : "description"})
        desc_content = meta_tag['content']
        desc_text_ln = len(desc_content)
        #desc_text_ln = int(desc_text_ln)
    
        
        if desc_text_ln < 150:
            result = {
                'name':name,
                'message':'Votre méta-description est trop courte, le nombre de caractère optimale doit être entre 150 et 250 caractères.',
                length_var_name: desc_text_ln,
                'desc_content':desc_content,
                'marks':1
            }
            final_score = final_score + result['marks']
            result_dict['meta_description'] = result
            print('try worked1')

        elif desc_text_ln > 150 and desc_text_ln < 250:
            result = {
                'name':name,
                'message':'Félicitations votre site dispose d’une méta-description avec un nombre de caractère optimal entre 150 et 155 caractères',
                length_var_name: desc_text_ln,
                'desc_content':desc_content,
                'marks':3
            }
            final_score = final_score + result['marks']
            result_dict['meta_description'] = result
            print('try worked2')
            
        elif desc_text_ln > 250 :
            result = {
                'name':name,
                'message':' Votre méta-description est trop longue, essayez de la raccourcir, le nombre optimal est entre 150 et 250 caractères, le reste risque d’être tronqué sur l’affichage du résultat sur les moteurs de recherche.',
                length_var_name: desc_text_ln,
                'desc_content':desc_content,
                'marks':2
            }
            final_score = final_score + result['marks']
            result_dict['meta_description'] = result
            print('try worked3')
    except:
        result1 = {
            'name':name,
            'message':'Votre site ne dispose pas de méta-description, La balise meta description manque sur votre page. Vous devez inclure cette balise afin de fournir une brève description de votre page pouvant être utilisée par les moteurs de recherche. Des méta-descriptions bien écrites et attrayantes peuvent également aider les taux de clics sur votre site dans les résultats de moteur de recherche.',
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['meta_description'] = result1
        print('except worked')



    # This is for row 3 (meta @keywords)
    name = 'meta_keywords'
    length_var_name = 'meta_key_len'
    try:
        meta_tag  = soup.find("meta", {"name" : "keywords"})
        meta_key_content_ln = len(meta_tag['content'])
        #title_ln = int(meta_key_content_ln)
    
        
        if meta_key_content_ln:
            result = {
                'name':name,
                'message':'Bravo vous avez spécifié des meta keywords . Vos mots-clés principaux doivent apparaître dans vos méta-tags pour vous aider à identifier le sujet de votre page Web dans les moteurs de recherche.',
                length_var_name: meta_key_content_ln,
                'marks':1
            }
            final_score = final_score + result['marks']
            result_dict['meta_keywords'] = result
            print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'Vos mots-clés principaux doivent apparaître dans vos méta-tags pour vous aider à identifier le sujet de votre page Web dans les moteurs de recherche.',
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['meta_keywords'] = result
        print('except worked')



    # This is for row 4 (meta @robots)
    name = 'meta_robots'
    length_var_name = 'meta_robots_len'
    try:
        meta_tag  = soup.find("meta", {"name" : "robots"})
        meta_robots_content = len(meta_tag['content'])
       # title_ln = int(desc_text_ln)
        
        if meta_robots_content:
            result = {
                'name':name,
                'message':"Votre site dispose d'un fichier robots.txt",
                length_var_name: meta_robots_content,
                'marks':4
            }
            final_score = final_score + result['marks']
            result_dict['meta_robots'] = result
            print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'''
                        Votre site n’a pas de robot.txt
                        Le robots.txt est un fichier texte utilisant un format précis qui permet à un Webmaster de contrôler quelles zones de son site un robot d'indexation est autorisé à analyser. Ce fichier texte sera disponible à une URL bien précise pour un site donné, par exemple http://www.monsite.com/robots.txt
                        Pour bien comprendre à quoi sert un robots.txt, il faut comprendre la manière dont fonctionnent les robots d'indexation des moteurs de recherche (appelés aussi Web spiders, Web crawlers ou Bots) tels que Google, Yahoo ou Bing. Voici leurs actions lorsqu'ils analysent un site tel que www.monsite.com : ils commencent par télécharger et analyser le fichier http://www.monsite.com/robots.txt.
            ''',
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['meta_robots'] = result1
        print('except worked')




    # This is for row 5 (html lang)
    name = 'html_lang'
    length_var_name = 'html_lang'
    try:
        meta_tag  = soup.find("html", {"lang" : True})
        lang_text = meta_tag['lang']
        

        result = {
            'name':name,
            'message':"Félicitations. Vous avez spécifié une langue à votre page.",
            length_var_name: lang_text,
            'marks':3
        }
        final_score = final_score + result['marks']
        result_dict['html_lang'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'''
            Vous devriez spécifier une langue pour votre site, les moteurs de recherches ne comprennent pas quand un site dispose de plusieurs langues par exemple ayant des mots techniques en anglais et un contenu texte en français. Il faut donc bien spécifier la langue.
            ''',
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['html_lang'] = result1
        print('except worked')




    # This is for row 6 (sitemap)
    url = url.strip()
    sitemap_url =  url+'/sitemap.xml'
    print("Sitemap url ",sitemap_url)
    try:

        code = requests.get(sitemap_url,headers=headers).status_code

        name = 'sitemap'

        if code == 200:
            result = {
                'name':name,
                'message':"Félicitations, votre site dispose d’un fichier sitemap",
                'marks':2
            }
            final_score = final_score + result['marks']
            result_dict['sitemap'] = result
            
        else:
            result = {
                'name':name,
                'message':"Votre site Web ne dispose pas d'un fichier sitemap. Les sitemaps peuvent aider les robots à indexer votre contenu de manière plus complète et plus rapide. ",
                'marks':0
            }
            final_score = final_score + result['marks']
            result_dict['sitemap'] = result
    except:
            result = {
                'name':name,
                'message':"Votre site Web ne dispose pas d'un fichier sitemap. Les sitemaps peuvent aider les robots à indexer votre contenu de manière plus complète et plus rapide. ",
                'marks':0
            }
            final_score = final_score + result['marks']
            result_dict['sitemap'] = result


    # This is for row 7 (google Analytics)
    searched_word = 'google-analytics'

    name = 'google_analytics'
    if searched_word in str(soup):
        print("Google analytics found")
        result = {
            'name':name,
            'message':"Félicitations, votre site dispose de l'outil Google Analytics",
            'marks':2
        }
        final_score = final_score + result['marks']
        result_dict['google_analytics'] = result
        
    else:
        result = {
            'name':name,
            'message':"Votre site ne dispose pas de l'outil Google Analytics.",
            'marks':0
        }
        final_score = final_score + result['marks']
        result_dict['google_analytics'] = result



    # This is for row 8 (page_cache)
    name = 'page_cache'
    length_var_name = 'page_cache_desc'
    try:
        meta_tag  = soup.find("meta", {"http-equiv" : "Cache-control"})
        lang_text = meta_tag['content']
        

        result = {
            'name':name,
            'message':"Vous avez activé le cache sur votre page, c'est très bien.",
            length_var_name: lang_text,
            'marks':3
        }
        final_score = final_score + result['marks']
        result_dict['page_cache'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':"Vous n'avez pas activé la mise en cache sur vos pages. La mise en cache permet un chargement plus rapide des pages.",
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['page_cache'] = result1
        print('except worked')



    # API_KEY = AIzaSyD_RLUOcTN1JAq8PL8zJ79X6-kmHIDy_uM
    # This is for row 9 (Google safe browsing api)



    api_key = 'AIzaSyCVylpWnsOwzUoeTGg7akZRod-4YbhXoPU'
    sbl = SafeBrowsingList(api_key)
    bl = sbl.lookup_url(url)

    name = 'google_safe_browsing'
    print("google_safe_browsing ",url )
    if bl is None:
        print("Website is safe")
        result = {
            'name':name,
            'message':"Votre site est considéré comme sécurisé.",
            'marks':2
        }
        final_score = final_score + result['marks']
        result_dict['google_safe_browsing'] = result
        
    else:
        result = {
            'name':name,
            'message':"Votre site n'est pas considéré comme sécurisé. Google et les autres moteurs de recherche prennent en compte le niveau de sécurité de votre site pour garantir la sécurité des visiteurs.",
            'marks':0,
            'threats':bl
        }
        final_score = final_score + result['marks']
        result_dict['google_safe_browsing'] = result




    # This is for row 10 (responsive website test)
    name = 'responsive_test'
    length_var_name = 'responsive_test_desc'
    try:
        meta_tag  = soup.find("meta", {"name" : "viewport"})
        lang_text = meta_tag['content']
        

        result = {
            'name':name,
            'message':"Félicitations. Votre site est responsive.",
            length_var_name: lang_text,
            'marks':4
        }
        final_score = final_score + result['marks']
        result_dict['responsive_test'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'''
            Nous n'avons pas détécté que votre site internet était responsive, soit adapté au mobile. Google prend énormément en compte ce critère pour un bon référencement.
            ''',
            length_var_name: 0,
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['responsive_test'] = result1
        print('except worked')


    # Html page size



    # mobile_friendliness_test
    print("mobile friendly ", url)
    data = {
    "url": url,
    "requestScreenshot": True,
    }
    
    r1 = requests.post('https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key=AIzaSyDExRwe7TNEgHa_JLogOVjccqWNVoaH-EQ',data).json()
    
    
    # a = json.loads(r1.text)
    a = r1
    imgstring = a['screenshot']['data']
    if imgstring:
        print("image of mobile returned")
    else:
        print("image of mobile NOT returned")

    # import base64
    # imgdata = base64.b64decode(imgstring)
    # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)

    name = 'mobile_friendliness_test'

    if a['mobileFriendliness'] == 'MOBILE_FRIENDLY':
        print("Website is mobile friendly")
        result = {
            'name':name,
            'message':"Félicitations. Votre site est Mobile friendly.",
            'result': a['mobileFriendliness'],
            'img_string':'data:image/png;base64,' + urllib.parse.quote(imgstring),
            'marks':4
        }
        final_score = final_score + result['marks']
        result_dict['mobile_friendliness_test'] = result
        
    else:
        result = {
            'name':name,
            'message':"Votre site n'est pas optimisé pour le mobile. Les moteurs de recherches donnent une très grande importance à la compatibilité mobile.",
            'marks':0,
            'result': a['mobileFriendliness'],
            'img_string':'data:image/png;base64,' + urllib.parse.quote(imgstring)
        }
        final_score = final_score + result['marks']
        result_dict['mobile_friendliness_test'] = result

    # except:
    #         result = {
    #             'name':name,
    #             'message':"Votre site n'est pas optimisé pour le mobile. Les moteurs de recherches donnent une très grande importance à la compatibilité mobile.",
    #             'marks':0,
    #             'result': "Not Mobile Friendly"
    #         }
    #         final_score = final_score + result['marks']
    #         result_dict['mobile_friendliness_test'] = result
    #     #  "mobileFriendlyIssues": [
    # #   {
    # #    "rule": "TAP_TARGETS_TOO_CLOSE"
    # #   },
    # #   {
    # #    "rule": "USE_LEGIBLE_FONT_SIZES"
    # #   },
    # #   {
    # #    "rule": "CONFIGURE_VIEWPORT"
    # #   }
    # #  ],




    # # google page speed
    # print("Google page speed ",url)
    # r2 = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}?key=AIzaSyAXf3ILJpeIs1nfDvvmLk0MsQDsuIsG5gM'.format(url))
    # b = json.loads(r2.text)
    # name = "page_speed"

    # # speed_index =  b['lighthouse']['audits']['speed-index']['.displayValue']
    # #print("this is speed index",speed_index)

    # # final_report.append({
    # #     "google_page_speed_data":b
    # # })
    # result_dict['page_speed'] = b



    # This is for row 13 (img alt attribute)
    name = 'img_alt'
    img_tags  = soup.findAll("img")

    no_alt = []
    empty_alt = []
    alt_ok = []
    empty_check = []

    name = "img_alt"

    
    for img_tag in img_tags:
        try:
            if not img_tag['alt'].strip():
                empty_alt.append(img_tag['src'])
            elif img_tag['alt'].strip():
                alt_ok.append(img_tag['src'])
        except:
            no_alt.append(img_tag)
                
    total_alt_num = len(empty_alt)+len(alt_ok)

    img_alt_result = {
        'name':name,
        'message':'',
        'marks': '',
        'no_alt':no_alt,
        'empty_altm':empty_alt
    }

    if len(img_tags) == len(alt_ok):
        img_alt_result['message'] = 'Félicitations. Toutes vos images disposent de balises alt attributs'
        img_alt_result['marks'] = 3
        print("every image tag contains alt and all have values")
        
    elif empty_alt and len(img_tags) == total_alt_num :
        img_alt_result['message'] = 'Certaines de vos images manquent de balises alt attributs. Voir la liste complète'
        img_alt_result['marks'] = 1
        print("Every img have alt tag but some have empty alt")
        
    elif len(img_tags) == len(no_alt):
        img_alt_result['message'] = "Aucune de vos images n'a de balises alt attributs, elles sont essentielles pour permettre aux moteurs de recherche de comprendre ce que représente votre image."
        img_alt_result['marks'] = 0
        print("No images have alt tag")
        
    if no_alt:
        img_alt_result['message'] = "Aucune de vos images n'a de balises alt attributs, elles sont essentielles pour permettre aux moteurs de recherche de comprendre ce que représente votre image."
        img_alt_result['marks'] = 0
        print("Some images have no  alt tag")
        

    final_score = final_score + img_alt_result['marks']
    result_dict['img_alt'] = img_alt_result





    # This is for row 14 (favicon test)
    name = 'favicon_test'
    length_var_name = 'favicon_link'

    favicon_list = []
    link_tags  = soup.findAll("link") 
    for link in link_tags:
        if "favicon" in link['href']:
            favicon_list.append(link['href'])
    if favicon_list:

        result = {
            'name':name,
            'message':"Félicitations. Votre site dispose d'une favicon.",
            length_var_name: favicon_list,
            'marks':1
        }
        final_score = final_score + result['marks']
        result_dict['favicon_test'] = result
        print('if worked1')
    else:
        result1 = {
            'name':name,
            'message':"Votre site ne dispose pas de favicon. La favicon est la petite icone qui apparait en haut du navigateur à côté du titre de votre site. Au delà de l'aspect SEO, elle permet de donner une identité visuelle à votre site.",
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['favicon_test'] = result1
        print('else worked')



    # This is for strong tag test
    name = 'strong_tag'
    length_var_name = 'strong_text'
    try:
        strong_tags  = soup.findAll("strong")
        
        if strong_tags:
            result = {
                'name':name,
                'message':'Félicitations. Vous avez spécifié des balises strong dans votre texte',
                length_var_name: strong_tags,
                'marks':2
            }
        else:
            result = {
            'name':name,
            'message':" Vous n'avez spécifié aucune balise strong dans votre texte. Les balises strong permettent aux moteurs de recherche de savoir quel contenu est intéressant et pertinent dans votre texte.",
            'marks':0
        }
        final_score = final_score + result['marks']
        result_dict['strong_tag'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':" Vous n'avez spécifié aucune balise strong dans votre texte. Les balises strong permettent aux moteurs de recherche de savoir quel contenu est intéressant et pertinent dans votre texte.",
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['strong_tag'] = result1
        print('except worked')



    # This is for Microdata test (itemscope , itemtype)
    name = 'micro_data_test'
    try:
        soup.find(True,{'itemscope':True}) or soup.find(True,{'itemtype':True})

        result = {
            'name':name,
            'message':"Félicitations. Votre site utilise des Microdonnées Schema.org",
            'marks':3
        }
        final_score = final_score + result['marks']
        result_dict['micro_data_test'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'''
            Vos visiteurs aiment les beadcrumbs, mais Google aussi. Les beadcrumbs donnent à Google un autre moyen de comprendre la structure de votre site Web. Toutefois, comme indiqué précédemment, Google peut également utiliser vos beadcrumbs dans les résultats de recherche, ce qui rend votre résultat beaucoup plus attrayant pour les utilisateurs.
            ''',
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['micro_data_test'] = result1
        print('except worked')



    # This is for AMP Version
    name = 'amp_html_test'
    try:
        tag = soup.find('link',{'rel':"amphtml"})

        result = {
            'name':name,
            'message':" Félicitations. Votre site dispose d'une version AMP",
            'amp_html_link':tag['href'],
            'marks': 3
        }
        final_score = final_score + result['marks']
        result_dict['amp_html_test'] = result
        print('try worked1')
    except:
        result1 = {
            'name':name,
            'message':'''L’objectif est que les pages AMP s’affichent presque de façon instantannée, c’est-à-dire généralement 90% plus rapidement que d’habitude.
    Grâce à cette grande vitesse, l’expérience utilisateur sur mobile se trouve largement améliorée, ce qui d’après des études fait chuter le taux de rebo
    ''',
            'marks':0
        }
        final_score = final_score + result1['marks']
        result_dict['amp_html_test'] = result1
        print('except worked')




    # This is for Breadcrumps
    searched_word = 'breadcrumb'

    name = 'breadcrumb'
    if searched_word in str(soup).lower():
        print("Breadcrum found")
        result = {
            'name':name,
            'message':"Félicitations, nous avons détécté l'utilisation de beadcrumbs sur votre site.",
            'marks':2
        }
        final_score = final_score + result['marks']
        result_dict['breadcrumb'] = result
        
    else:
        result = {
            'name':name,
            'message':"Nous n'avons pas détécté de Beadcrumb sur votre site. Les Beadcrumbs sont une partie importante de presque tous les bons sites Web. Ces petites aides à la navigation ne permettent pas seulement aux internautes de savoir où elles se trouvent sur votre site, elles aident également Google à déterminer la structure de votre site.",
            'marks':0
        }
        final_score = final_score + result['marks']
        result_dict['breadcrumb'] = result



    # Open graph Test
    name = 'open_graph_test'
    open_graph_tags = []

    og_tags = soup.findAll('meta',{"property":True})
    for og in og_tags:
        if "og" in str(og):
            open_graph_tags.append(og['property']) 
            
    result = {
            'name':name,
            'message':"",
            'marks':"",
            'og_tags':open_graph_tags
        }        

    if open_graph_tags:
        result['message'] = 'Félicitations nous avons détécté des balises Open Graph.'
        result['marks'] = 1
        print("If worked")
    else:
        result['message'] = '''
        Les balises méta Open Graph sont conçues pour communiquer des informations sur votre site Web aux réseaux sociaux lorsque des liens vers votre site Web sont partagés. Ces balises vous permettent de créer des titres, des descriptions et des images personnalisés à utiliser lorsque vos pages sont partagées sur Facebook, LinkedIn et Google+.

    Ainsi, tout comme lorsque Google ou un autre moteur de recherche visite votre site et recherche les données (ou balises) appropriées afin d'afficher correctement votre site Web dans les résultats de recherche, les réseaux sociaux agissent de la même manière. La seule différence est que les réseaux sociaux recherchent ces tags spécifiques Open Graph (ou tags Twitter).
        '''
        result['marks'] = 0
        print("else worked")
    result_dict['open_graph_test'] = result
    final_score=final_score+result['marks']



    # Twitter Test
    name = 'twitter_test'
    twitter_tags = []

    og_tags = soup.findAll('meta',{"property":True})
    for twitter in twitter_tags:
        if "twitter" in str(og_tags):
            twitter_tags.append(og['property']) 
            
    result = {
            'name':name,
            'message':"",
            'marks':"",
            'og_tags':twitter_tags
        }        

    if twitter_tags:
        result['message'] = ' Parfait. Vous avez spécifié des Twitter Cards'
        result['marks'] = 2
        print("If worked")
    else:
        result['message'] = "Twitter via les twitter Cards vous permet d'identifier l'auteur de la publication / de la page ainsi que l'éditeur, qui est généralement le nom du site Web. Ces deux valeurs ne sont pas obligatoires, mais permettent d’ajouter des données supplémentaires à ceux qui souhaiteraient l’ajouter."
        result['marks'] = 0
        print("else worked")
    result_dict['twitter_test'] = result
    final_score=final_score+result['marks']




    # This is for Social Media test
    fb = 'facebook.com'
    linkedin = 'linkedin.com'
    twitter = 'twitter.com'

    name = 'social_media_test'
    social_sites_found = []
    if fb in str(soup):
        social_sites_found.append('facebook')
        print("facebook.com found")
    elif linkedin in str(soup):
        social_sites_found.append('linkedin')
        print("linkedin.com found")
    elif twitter in str(soup):
        social_sites_found.append('twitter')
        print("twitter.com found")

    result = {
            'name':name,
            'message':"",
            'marks':'',
            'social_sites_found':social_sites_found
        }
    if social_sites_found:
        result['message'] = 'Nous avons détécté une liaison vers les réseaux sociaux sur votre site.'
        result['marks'] = 2
        
    else:
        result['message'] = " Nous n'avons pas détécté de lien vers vos réseaux sociaux sur votre site. Même si ça n'impacte pas grandement votre SEO, avoir des liens vers les réseaux sociaux de sa marque est plus agréable et utile pour les utilisateurs."
        result['marks'] = 0

    final_score = final_score + result['marks']
    result_dict['social_media_test'] = result




    # for H1/h2/h3
    h1_tag = soup.findAll('h5')
    h_tags = []
    for i in range(1,6):
        h_tag = soup.find_all('h'+str(i))
        result =  {"tag":'h'+str(i),
                "total_num":len(h_tag)
                
                }
        h_tags.append(result)
        
    result = {
        "name":"heading_tags_test",
        "message":"",
        "marks":"",
        "total_num _tags":h_tags
    }
    if h_tags[0] and h_tags[1] and h_tags[2]:
        result['message'] = "Félicitations vos en en-têtes sont structurées"
        result['marks'] = 3
        
    elif h_tags[0] or h_tags[1] or h_tags[2] or h_tags[3] or h_tags[4]:
        result['message'] = "FVos en-têtes ne sont pas structurés, il faut d'abord spécifier des en-têtes H1 puis H2 puis H3 etc.."
        result['marks'] = 1

    else:
        result['message'] = "Vous n'avez pas spécifié d'en têtes, c'est un élément essentiel du SEO, ça permet aux moteurs de recherche de savoir de quoi le chapitre ou la section va discuter."
        result['marks'] = 0

    final_score = final_score + result['marks']
    result_dict['heading_tags_test'] = result
        



    # This is for page characters
    name = 'page_characters'
    try:
        tags1 = soup.findAll('p')
        tags2 = soup.findAll('h1')
        tags3 = soup.findAll('h2')
        tags4 = soup.findAll('h3')
        tags5 = soup.findAll('h4')
        tags6 = soup.findAll('h5')
        tags = tags1 +tags2 +tags3 +tags4 +tags5 +tags6
        text = ""
        for tag in tags:
            text = text+tag.text
            
        num_words = len(text.split(' '))
        
        result = {
            'name':name,
            'message':"",
            'marks': "",
            'num_words':num_words
        }
        
        if num_words > 300:
            result['message'] = "Félicitations, la quantité de texte est supérieur à 300 mots."
            result['marks'] = 5
        else:
            result['message'] = "La quantité de texte est insuffisante, il faut que vos pages contiennent plus de 300 mots pour que le contenu soit intéressant pour les moteurs de recherche."
            result['marks'] = 0
            
        print('try worked1')
    except:
        result = {
            'name':name,
            'message':'''
            
    La quantité de texte est insuffisante, il faut que vos pages contiennent plus de 300 mots pour que le contenu soit intéressant pour les moteurs de recherche.
    ''',
            'marks':0
        }

        print('except worked')
    final_score = final_score + result['marks']
    result_dict['page_characters'] = result




    # page = requests.get(url,headers=headers).text

    # collecting all urls in website


    domain =tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    subdomain = tldextract.extract(url).subdomain
    pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'


    link_levels = []
    found_links = re.findall(pattern, r.text)
    links = []
    external_links = []

    web = domain+'.'+suffix

    for link in found_links:
        if url not in link and "." not in link and "#" not in link:
            links.append(url+link)
            
        elif url not in link and "#" not in link and web not in link:
            external_links.append(link)
            
    links = list(dict.fromkeys(links))


    # keywords in URL test &&  levels in url

    keywords_in_url = []
    directories_in_url = []

    for url in links:    
        if 'https' in url:
            if subdomain:
                url1 = "https://"+subdomain+'.'+domain+'.'+suffix
            else:
                url1 = "https://"+domain+'.'+suffix    
            
        elif 'http' in url:
            if subdomain:
                url1 = "http://"+subdomain+'.'+domain+'.'+suffix
            else:
                url1 = "http://"+domain+'.'+suffix    
                
        a = url
        t=set(url1.split('/'))
        p = set(a.split('/'))
        e = p-t
        keywords = list(e)

        if keywords:
            for item in keywords:
                keywords_in_url.append(item)
            directories_in_url.append(len(keywords))

            keywords_in_url = list(dict.fromkeys(keywords_in_url))
        else:
            pass

    

    result = {
        "name":"keywords_in_url",
        "keywords":keywords_in_url,
        "message":"",
        "marks":''
    }
    if keywords_in_url:
        result['message'] = "Vos urls disposent de keywords, Veuillez vérifier qu'elles correspondent bien à ce que vous voulez mettre en avant sur votre site."
        result['marks'] = 1
    else:
        result['message'] = "Vos urls ne semblent pas avoir de keywords."
        result['marks'] = 0

    result_dict['keywords_in_url'] = result
    final_score = final_score + result['marks']

    if directories_in_url:
        directories = max(directories_in_url)
    else:
        directories = 0
    result = {
        "name":"directories_in_url",
        "directories":directories,
        "message":"",
        "marks":''
    }
    if directories < 5:
        result['message'] = "Félicitations, votre URL est composée de moins de 5 dossiers",
        result['marks'] = 2
    else:
        result['message'] = "Vos url sont composées de plus de 5 dossiers, veuillez en diminuer le nombre",
        result['marks'] = 0

    result_dict['directories_in_url'] = result
    final_score = final_score + result['marks']




    # # broken_link test
    # broken_links = []
    # all_links = links + external_links
    # for link in all_links:
    #     try:
    #         print("Checking link health of ",link)
    #         r1 = requests.get(url,headers = headers)
    #     except:
    #         broken_links.append(link)
    # result = {
    #     "name":"broken_links_test",
    #     "message":"",
    #     "marks":'',
    #     "broken_links":broken_links
    # }
    # if broken_links:
    #     result['message'] = "Nous avons détécté un ou plusieurs liens qui ne fonctionnent plus sur votre site internet. Voir la liste complète"
    #     result['marks'] = 0
    # else:
    #     result['message'] = "Félicitations, vous n'avez pas de brokenlinks."
    #     result['marks'] = 3 
        
    # final_score = final_score + result['marks']
    # result_dict['broken_links_test'] = result



    # external links test
    result = {
        "name":"external_links_test",
        "message":"",
        "marks":'',
        "external_links":external_links
    }
    if external_links:
        result['message'] = "Félicitations, vous avez plusieurs external links. Voir la liste complète"
        result['marks'] = 9
    else:
        result['message'] = "Nous n'avons pas détécté de external links pour votre site internet. Les liens retour (external internal links) de qualité, sont primordiaux pour une bon référencement."
        result['marks'] = 0
        
    final_score = final_score + result['marks']
    result_dict['external_links_test'] = result



    #word cloud
    if text:
        cloud = WordCloud(background_color="white").generate(text)
        plt.imshow(cloud)
        plt.axis('off')




        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        result = {
            "name":"word_cloud",
            "img":image_64,
            "message":"Nuage des mots les plus présents sur votre page"
        }
        result_dict['word_cloud'] = result
    else:
        result = {
            "name":"word_cloud",
            "img":"",
            "message":"Aucun contenu texte n'a été détécté"
        }




    # Internal links test
    result = {
        "name":"internal_links_test",
        "message":"",
        "marks":'',
        "internal_links":links
    }
    if links:
        result['message'] = "Félicitations. Nous avons détécté l'utilisation de liens internes sur votre page."
        result['marks'] = 4
    else:
        result['message'] = "Nous n'avons pas détécté de liens internes sur votre page. En plus de faire la liaison entre vos différentes pages, les liens internes permettent de mieux guider les robots Google et mettent en évidence le lien entre vos différentes pages."
        result['marks'] = 0
        
    final_score = final_score + result['marks']
    result_dict['internal_links_test'] = result

    test_count = {
        "test_passed":"",
        "test_failed":"",
        "without_marks":""
    } 
    passed = 0
    failed = 0
    without_marks = 0
    for k,v in result_dict.items():
        try:
            if v['marks'] == 0:
                failed = failed+1
            elif v['marks'] > 0:
                passed = passed+1
            else:
                pass
        except:
            without_marks = without_marks+1

    test_count['test_passed'] = passed
    test_count['test_failed'] = failed
    test_count['without_marks'] = without_marks
    result_dict['test_count'] = test_count

    return (final_score, result_dict)




score,final_dict= scrapper("lemarrakech-nancy.fr")

print(score)
print(final_dict)