from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response
from rest_framework.permissions             import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm
from .lib import get_search_results, get_page_content
from .models import User
from .helper    import custom_render, extract_keywords

results = {
    "items": [
        {
            "kind": "customsearch#result",
            "title": "Adele - Hello (Official Music Video) - YouTube",
            "htmlTitle": "Adele - <b>Hello</b> (Official Music Video) - YouTube",
            "link": "https://www.youtube.com/watch?v=YQHsXMglC9A",
            "displayLink": "www.youtube.com",
            "snippet": "Oct 22, 2015 ... Listen to \"Easy On Me\" here: http://Adele.lnk.to/EOM Pre-order Adele's new album \"30\" before its release on November 19: ...",
            "htmlSnippet": "Oct 22, 2015 <b>...</b> Listen to &quot;Easy On Me&quot; here: http://Adele.lnk.to/EOM Pre-order Adele&#39;s new album &quot;30&quot; before its release on November 19:&nbsp;...",
            "cacheId": "hisqDBlSEToJ",
            "formattedUrl": "https://www.youtube.com/watch?v=YQHsXMglC9A",
            "htmlFormattedUrl": "https://www.youtube.com/watch?v=YQHsXMglC9A",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQAbT0ytVabEjpCm5SRO4L4WuwwWrkUVahS9Yv8Jrf3XuCu4yxvPNLpmwab",
                        "width": "299",
                        "height": "168"
                    },
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQAbT0ytVabEjpCm5SRO4L4WuwwWrkUVahS9Yv8Jrf3XuCu4yxvPNLpmwab",
                        "width": "299",
                        "height": "168"
                    },
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQAbT0ytVabEjpCm5SRO4L4WuwwWrkUVahS9Yv8Jrf3XuCu4yxvPNLpmwab",
                        "width": "299",
                        "height": "168"
                    }
                ],
                "metatags": [
                    {
                        "apple-itunes-app": "app-id=544007664, app-argument=https://m.youtube.com/watch?v=YQHsXMglC9A&referring_app=com.apple.mobilesafari-smartbanner, affiliate-data=ct=smart_app_banner_polymer&pt=9008",
                        "theme-color": "rgba(0, 0, 0, 0)",
                        "viewport": "width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no,",
                        "twitter:url": "https://www.youtube.com/watch?v=YQHsXMglC9A",
                        "og:url": "https://www.youtube.com/watch?v=YQHsXMglC9A"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://i.ytimg.com/vi/ExDXLKFWTBM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBkzpMqEd5GfavRLcnUSBlZzNuhyQ"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "hello | naturally friendly products, vegan + never tested on animals",
            "htmlTitle": "<b>hello</b> | naturally friendly products, vegan + never tested on animals",
            "link": "https://www.hello-products.com/",
            "displayLink": "www.hello-products.com",
            "snippet": "Hello antiplaque and whitening toothpaste is free from dyes, SLS sulfates, parabens, microbeads, triclosan, and gluten. hello toothpastes also contain no ...",
            "htmlSnippet": "<b>Hello</b> antiplaque and whitening toothpaste is free from dyes, SLS sulfates, parabens, microbeads, triclosan, and gluten. <b>hello</b> toothpastes also contain no&nbsp;...",
            "cacheId": "lcA_2yf_mQgJ",
            "formattedUrl": "https://www.hello-products.com/",
            "htmlFormattedUrl": "https://www.<b>hello</b>-products.com/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS49LpojT3gru71Lz17BGAr1J27k-oxw8YS5S9-FP5SOfnlZLCRuYqnO-Bu",
                        "width": "312",
                        "height": "161"
                    }
                ],
                "metatags": [
                    {
                        "msapplication-tilecolor": "#ffffff",
                        "og:image": "https://www.hello-products.com/wp-content/uploads/2020/01/HELLO_Strangely_Likeable_Mobile_Header_580x300.png",
                        "theme-color": "#ffffff",
                        "og:type": "website",
                        "og:image:width": "580",
                        "twitter:card": "summary_large_image",
                        "og:site_name": "Hello Products",
                        "msvalidate.01": "782AB2D27CB855D9F86E2B56FBC572DA",
                        "og:title": "hello | naturally friendly products, vegan + never tested on animals",
                        "og:image:height": "300",
                        "og:image:type": "image/png",
                        "msapplication-tileimage": "/ms-icon-144x144.png",
                        "og:description": "naturally friendly products for naturally friendly people. vegan, cruelty free, and thoughtfully formulated for everyone.",
                        "facebook-domain-verification": "5g2asge0sadcgj8wwh8380fkrcka91",
                        "article:modified_time": "2023-08-10T18:07:02+00:00",
                        "viewport": "width=device-width, initial-scale=1.0",
                        "og:locale": "en_US",
                        "og:url": "https://www.hello-products.com/",
                        "format-detection": "telephone=no"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://www.hello-products.com/wp-content/uploads/2020/01/HELLO_Strangely_Likeable_Mobile_Header_580x300.png"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "Lionel Richie - Hello (Official Music Video) - YouTube",
            "htmlTitle": "Lionel Richie - <b>Hello</b> (Official Music Video) - YouTube",
            "link": "https://www.youtube.com/watch?v=mHONNcZbwDY",
            "displayLink": "www.youtube.com",
            "snippet": "Nov 20, 2020 ... REMASTERED IN HD! Explore the music of Lionel Richie: https://lnk.to/LionelBestOf Watch more Lionel videos: https://lnk.to/LionelVevo Get ...",
            "htmlSnippet": "Nov 20, 2020 <b>...</b> REMASTERED IN HD! Explore the music of Lionel Richie: https://lnk.to/LionelBestOf Watch more Lionel videos: https://lnk.to/LionelVevo Get&nbsp;...",
            "cacheId": "Iol1aRwBp-8J",
            "formattedUrl": "https://www.youtube.com/watch?v=mHONNcZbwDY",
            "htmlFormattedUrl": "https://www.youtube.com/watch?v=mHONNcZbwDY",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSalvu7lX6SJ-wx4lNp-0GyGGzDEN14AlDGFtuJ_bhP3sLydQm-o4IYDiD_",
                        "width": "299",
                        "height": "168"
                    }
                ],
                "metatags": [
                    {
                        "apple-itunes-app": "app-id=544007664, app-argument=https://m.youtube.com/watch?v=mHONNcZbwDY&referring_app=com.apple.mobilesafari-smartbanner, affiliate-data=ct=smart_app_banner_polymer&pt=9008",
                        "theme-color": "rgba(0, 0, 0, 0)",
                        "viewport": "width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no,",
                        "twitter:url": "https://www.youtube.com/watch?v=mHONNcZbwDY",
                        "og:url": "https://www.youtube.com/watch?v=mHONNcZbwDY"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://i.ytimg.com/vi/76fAfFcY_Tc/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGH8gNCgaMA8=&rs=AOn4CLDvrkscRXQ5Rd9_QNzSz-lZFoMi1A"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "HelloFresh®: 16 Free Meals - Free Breakfast Item For Life",
            "htmlTitle": "HelloFresh®: 16 Free Meals - Free Breakfast Item For Life",
            "link": "https://www.hellofresh.com/",
            "displayLink": "www.hellofresh.com",
            "snippet": "Hello Healthy Routine · Why HelloFresh? · What's inside each box? · Over 45+ fresh recipes every week · Cook it. Love it. Tag it #HelloFreshPics.",
            "htmlSnippet": "<b>Hello</b> Healthy Routine &middot; Why HelloFresh? &middot; What&#39;s inside each box? &middot; Over 45+ fresh recipes every week &middot; Cook it. Love it. Tag it #HelloFreshPics.",
            "formattedUrl": "https://www.hellofresh.com/",
            "htmlFormattedUrl": "https://www.<b>hello</b>fresh.com/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLNWa3seKdWzcL2xrcSULLZ7zrkKB9KegM9CwZAu8QV-t2khvFWr4wI-s",
                        "width": "200",
                        "height": "200"
                    }
                ],
                "thumbnail": [
                    {
                        "src": "https://cdn.hellofresh.com/de/cms/raf/hellofresh-logo.png"
                    }
                ],
                "metatags": [
                    {
                        "p:domain_verify": "5aea915e1ac0b408298cfb02478eb3b2",
                        "country": "US",
                        "og:image": "https://cdn.hellofresh.com/de/cms/raf/hellofresh-logo.png",
                        "theme-color": "#FFF",
                        "twitter:card": "summary_large_image",
                        "og:image:width": "1140",
                        "og:site_name": "HelloFresh",
                        "twitter:url": "https://www.hellofresh.com/",
                        "apple-mobile-web-app-title": "Home",
                        "og:description": "Enjoy Free Breakfast for Life - Limited Time Only! 16 Free Meals Offer is for new subscriptions only across 9 boxes and varies by plan. First box ships free.",
                        "twitter:image": "https://cdn.hellofresh.com/de/cms/raf/hellofresh-logo.png",
                        "next-head-count": "71",
                        "twitter:site": "@hellofresh",
                        "msapplication-tilecolor": "#FFF",
                        "og:type": "product",
                        "thumbnail": "https://cdn.hellofresh.com/de/cms/raf/hellofresh-logo.png",
                        "twitter:title": "HelloFresh®: 16 Free Meals - Free Breakfast Item For Life",
                        "og:image:alt": "HelloFresh",
                        "twitter:domain": "https://www.hellofresh.com/",
                        "author": "HelloFresh",
                        "og:title": "HelloFresh®: 16 Free Meals - Free Breakfast Item For Life",
                        "og:image:height": "600",
                        "version": "7.98.1874",
                        "url": "https://www.hellofresh.com/",
                        "site:name": "HelloFresh",
                        "viewport": "width=device-width, initial-scale=1.0",
                        "twitter:description": "Enjoy Free Breakfast for Life - Limited Time Only! 16 Free Meals Offer is for new subscriptions only across 9 boxes and varies by plan. First box ships free.",
                        "og:locale": "en-US",
                        "og:url": "https://www.hellofresh.com/"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://cdn.hellofresh.com/de/cms/raf/hellofresh-logo.png"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "Hello Definition & Meaning - Merriam-Webster",
            "htmlTitle": "<b>Hello</b> Definition &amp; Meaning - Merriam-Webster",
            "link": "https://www.merriam-webster.com/dictionary/hello",
            "displayLink": "www.merriam-webster.com",
            "snippet": "The meaning of HELLO is an expression or gesture of greeting —used interjectionally in greeting, in answering the telephone, or to express surprise.",
            "htmlSnippet": "The meaning of <b>HELLO</b> is an expression or gesture of greeting —used interjectionally in greeting, in answering the telephone, or to express surprise.",
            "cacheId": "X-3FVcOvM5gJ",
            "formattedUrl": "https://www.merriam-webster.com/dictionary/hello",
            "htmlFormattedUrl": "https://www.merriam-webster.com/dictionary/<b>hello</b>",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSKksTSKYwpW8It403nrjw5t1_a8pLO2PI6ImEG7uvFrNfacgiziPZgG-_O",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "msapplication-tilecolor": "#2b5797",
                        "og:image": "https://merriam-webster.com/assets/mw/static/social-media-share/mw-logo-245x245@1x.png",
                        "twitter:title": "Definition of HELLO",
                        "twitter:card": "summary",
                        "theme-color": "#ffffff",
                        "twitter:url": "https://www.merriam-webster.com/dictionary/hello",
                        "og:title": "Definition of HELLO",
                        "twitter:aria-text": "Share the Definition of hello on Twitter",
                        "og:aria-text": "Post the Definition of hello to Facebook",
                        "og:description": "an expression or gesture of greeting —used interjectionally in greeting, in answering the telephone, or to express surprise… See the full definition",
                        "twitter:image": "https://merriam-webster.com/assets/mw/static/social-media-share/mw-logo-245x245@1x.png",
                        "referrer": "unsafe-url",
                        "fb:app_id": "178450008855735",
                        "twitter:site": "@MerriamWebster",
                        "viewport": "width=device-width, initial-scale=1.0",
                        "twitter:description": "an expression or gesture of greeting —used interjectionally in greeting, in answering the telephone, or to express surprise… See the full definition",
                        "og:url": "https://www.merriam-webster.com/dictionary/hello"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://merriam-webster.com/assets/mw/static/social-media-share/mw-logo-245x245@1x.png"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "HELLO! - Daily royal, celebrity, fashion, beauty & lifestyle news",
            "htmlTitle": "<b>HELLO</b>! - Daily royal, celebrity, fashion, beauty &amp; lifestyle news",
            "link": "https://www.hellomagazine.com/",
            "displayLink": "www.hellomagazine.com",
            "snippet": "HELLO! brings you the latest celebrity & royal news from the UK & around the world, magazine exclusives, fashion, beauty, lifestyle news, celeb babies, ...",
            "htmlSnippet": "<b>HELLO</b>! brings you the latest celebrity &amp; royal news from the UK &amp; around the world, magazine exclusives, fashion, beauty, lifestyle news, celeb babies,&nbsp;...",
            "cacheId": "hxjkDmKHGvIJ",
            "formattedUrl": "https://www.hellomagazine.com/",
            "htmlFormattedUrl": "https://www.<b>hello</b>magazine.com/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSrRsSM_cW7sp0Kzq_AhpJHP0rk8sIHX50XQDeT3jLEjVMVJXhDZGd6Erf6",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "p:domain_verify": "2e0d0d07c9164557a351ff28f09074ef",
                        "og:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "twitter:card": "summary",
                        "theme-color": "#ffffff",
                        "og:site_name": "HELLO!",
                        "origin": "https://www.hellomagazine.com/",
                        "title": "HELLO! - Daily royal, celebrity, fashion, beauty & lifestyle news",
                        "og:description": "HELLO! brings you the latest celebrity & royal news from the UK & around the world, magazine exclusives, fashion, beauty, lifestyle news, celeb babies, weddings, pregnancies and more!",
                        "twitter:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "article:publisher": "https://www.facebook.com/hello",
                        "next-head-count": "31",
                        "twitter:site": "@hellomag",
                        "fb:admins": "89982930077",
                        "botify-site-verification": "rAorMmkbfzd6yOwJ3PITFmdyCjOzGLug",
                        "msapplication-tilecolor": "#cc0000",
                        "twitter:title": "HELLO! - Daily royal, celebrity, fashion, beauty & lifestyle news",
                        "og:type": "website",
                        "msvalidate.01": "802E2A1202224ED23A9EF77A39836CEC",
                        "og:title": "HELLO! - Daily royal, celebrity, fashion, beauty & lifestyle news",
                        "og:updated_time": "2024-01-24T12:40:53.174Z",
                        "fb:pages": "89982930077",
                        "fb:app_id": "115281558857295",
                        "viewport": "width=device-width",
                        "twitter:description": "HELLO! brings you the latest celebrity & royal news from the UK & around the world, magazine exclusives, fashion, beauty, lifestyle news, celeb babies, weddings, pregnancies and more!",
                        "og:url": "https://www.hellomagazine.com/"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://www.hellomagazine.com/hello-fb-logo.png"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "The Official Home of Hello Kitty & Friends",
            "htmlTitle": "The Official Home of <b>Hello</b> Kitty &amp; Friends",
            "link": "https://www.sanrio.com/",
            "displayLink": "www.sanrio.com",
            "snippet": "Explore the supercute world of Sanrio, home to Hello Kitty, My Melody, Kuromi, Aggretsuko, Gudetama, and more!",
            "htmlSnippet": "Explore the supercute world of Sanrio, home to <b>Hello</b> Kitty, My Melody, Kuromi, Aggretsuko, Gudetama, and more!",
            "formattedUrl": "https://www.sanrio.com/",
            "htmlFormattedUrl": "https://www.sanrio.com/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTLXw_T6vP2U2yvPT9_1zZv2lPTIX4mwegGIycPvgnk2e_367emfZMtUuk",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "og:image": "https://www.sanrio.com/cdn/shop/files/HK_AND_Friends_cream_600x600.png?v=1614311113",
                        "theme-color": "#ffffff",
                        "og:type": "website",
                        "og:image:width": "1200",
                        "twitter:card": "summary",
                        "og:site_name": "Sanrio",
                        "author": "Sanrio",
                        "og:title": "The Official Home of Hello Kitty & Friends",
                        "shopify-checkout-api-token": "16940c0cea93e91348c277a0eafbe76d",
                        "og:image:height": "1200",
                        "og:description": "Explore the supercute world of Sanrio, home to Hello Kitty, My Melody, Kuromi, Aggretsuko, Gudetama, and more!",
                        "og:image:secure_url": "https://www.sanrio.com/cdn/shop/files/HK_AND_Friends_cream_600x600.png?v=1614311113",
                        "twitter:site": "@sanrio/",
                        "viewport": "width=device-width,initial-scale=1",
                        "shopify-digital-wallet": "/41680830620/digital_wallets/dialog",
                        "og:url": "https://www.sanrio.com/"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://www.sanrio.com/cdn/shop/files/HK_AND_Friends_cream_600x600.png?v=1614311113"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "HELLO! Canada edition: Daily news, Celebrity, fashion and beauty",
            "htmlTitle": "<b>HELLO</b>! Canada edition: Daily news, Celebrity, fashion and beauty",
            "link": "https://www.hellomagazine.com/ca/",
            "displayLink": "www.hellomagazine.com",
            "snippet": "HELLO! Canada brings you the latest celebrity & royal news from around the world, magazine exclusives, celeb babies, weddings, pregnancies and more.",
            "htmlSnippet": "<b>HELLO</b>! Canada brings you the latest celebrity &amp; royal news from around the world, magazine exclusives, celeb babies, weddings, pregnancies and more.",
            "cacheId": "_edcASA2CiQJ",
            "formattedUrl": "https://www.hellomagazine.com/ca/",
            "htmlFormattedUrl": "https://www.<b>hello</b>magazine.com/ca/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSrRsSM_cW7sp0Kzq_AhpJHP0rk8sIHX50XQDeT3jLEjVMVJXhDZGd6Erf6",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "p:domain_verify": "2e0d0d07c9164557a351ff28f09074ef",
                        "og:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "twitter:card": "summary",
                        "theme-color": "#ffffff",
                        "og:site_name": "HELLO!",
                        "origin": "https://www.hellomagazine.com/ca/",
                        "title": "HELLO! Canada edition: Daily news, Celebrity, fashion and beauty",
                        "og:description": "HELLO! Canada brings you the latest celebrity & royal news from around the world, magazine exclusives, celeb babies, weddings, pregnancies and more",
                        "twitter:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "article:publisher": "https://www.facebook.com/hello",
                        "next-head-count": "31",
                        "twitter:site": "@hellomag",
                        "fb:admins": "89982930077",
                        "botify-site-verification": "rAorMmkbfzd6yOwJ3PITFmdyCjOzGLug",
                        "msapplication-tilecolor": "#cc0000",
                        "twitter:title": "HELLO! Canada edition: Daily news, Celebrity, fashion and beauty",
                        "og:type": "website",
                        "msvalidate.01": "802E2A1202224ED23A9EF77A39836CEC",
                        "og:title": "HELLO! Canada edition: Daily news, Celebrity, fashion and beauty",
                        "og:updated_time": "2024-01-24T12:49:35.901Z",
                        "fb:pages": "89982930077",
                        "fb:app_id": "115281558857295",
                        "viewport": "width=device-width",
                        "twitter:description": "HELLO! Canada brings you the latest celebrity & royal news from around the world, magazine exclusives, celeb babies, weddings, pregnancies and more",
                        "og:url": "https://www.hellomagazine.com/ca/"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://www.hellomagazine.com/hello-fb-logo.png"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "no hello",
            "htmlTitle": "no <b>hello</b>",
            "link": "https://nohello.net/en",
            "displayLink": "nohello.net",
            "snippet": "please don't say just hello in chat.",
            "htmlSnippet": "please don&#39;t say just <b>hello</b> in chat.",
            "cacheId": "bxe5YCwk69MJ",
            "formattedUrl": "https://nohello.net/en",
            "htmlFormattedUrl": "https://no<b>hello</b>.net/en",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQeoeulfqmB-Z8gxhO22a1bhZM1AHKLGZJZFAjgYm9LJBHn8pTdeyg7ZSk",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "og:image": "https://nohello.net/img/XzfE_FYNGc-500.webp",
                        "og:type": "website",
                        "twitter:card": "summary",
                        "twitter:title": "no hello",
                        "viewport": "width=device-width, initial-scale=1.0",
                        "twitter:url": "https://nohello.net/",
                        "twitter:description": "please don't say just hello in chat",
                        "og:title": "no hello",
                        "title": "no hello",
                        "og:url": "https://nohello.net/",
                        "og:description": "please don't say just hello in chat",
                        "twitter:image": "https://nohello.net/img/XzfE_FYNGc-500.webp"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://nohello.net/img/XzfE_FYNGc-500.webp"
                    }
                ]
            }
        },
        {
            "kind": "customsearch#result",
            "title": "HELLO! US Edition - Latest news and Photos",
            "htmlTitle": "<b>HELLO</b>! US Edition - Latest news and Photos",
            "link": "https://www.hellomagazine.com/us/",
            "displayLink": "www.hellomagazine.com",
            "snippet": "HELLO! US edition brings you the latest celebrity & royal news from the US & around the world, magazine exclusives, celeb babies, weddings, pregnancies and ...",
            "htmlSnippet": "<b>HELLO</b>! US edition brings you the latest celebrity &amp; royal news from the US &amp; around the world, magazine exclusives, celeb babies, weddings, pregnancies and&nbsp;...",
            "cacheId": "75KX4ku9N7oJ",
            "formattedUrl": "https://www.hellomagazine.com/us/",
            "htmlFormattedUrl": "https://www.<b>hello</b>magazine.com/us/",
            "pagemap": {
                "cse_thumbnail": [
                    {
                        "src": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSrRsSM_cW7sp0Kzq_AhpJHP0rk8sIHX50XQDeT3jLEjVMVJXhDZGd6Erf6",
                        "width": "225",
                        "height": "225"
                    }
                ],
                "metatags": [
                    {
                        "p:domain_verify": "2e0d0d07c9164557a351ff28f09074ef",
                        "og:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "twitter:card": "summary",
                        "theme-color": "#ffffff",
                        "og:site_name": "HELLO!",
                        "origin": "https://www.hellomagazine.com/us/",
                        "title": "HELLO! US Edition - Latest news and Photos",
                        "og:description": "HELLO! US edition brings you the latest celebrity & royal news from the US & around the world, magazine exclusives, celeb babies, weddings, pregnancies and more",
                        "twitter:image": "https://www.hellomagazine.com/hello-fb-logo.png",
                        "article:publisher": "https://www.facebook.com/hello",
                        "next-head-count": "32",
                        "twitter:site": "@hellomag",
                        "fb:admins": "108802182109385",
                        "botify-site-verification": "rAorMmkbfzd6yOwJ3PITFmdyCjOzGLug",
                        "msapplication-tilecolor": "#cc0000",
                        "twitter:title": "HELLO! US Edition - Latest news and Photos",
                        "og:type": "website",
                        "msvalidate.01": "802E2A1202224ED23A9EF77A39836CEC",
                        "og:title": "HELLO! US Edition - Latest news and Photos",
                        "og:updated_time": "2024-01-24T14:23:14.623Z",
                        "fb:pages": "108802182109385",
                        "fb:app_id": "115281558857295",
                        "viewport": "width=device-width",
                        "ir-site-verification-token": "-513407988",
                        "twitter:description": "HELLO! US edition brings you the latest celebrity & royal news from the US & around the world, magazine exclusives, celeb babies, weddings, pregnancies and more",
                        "og:url": "https://www.hellomagazine.com/us/"
                    }
                ],
                "cse_image": [
                    {
                        "src": "https://www.hellomagazine.com/hello-fb-logo.png"
                    }
                ]
            }
        }
    ]
}

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':    
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {
        'form' : form,
    })

def search(request):
    context = {
        key : val for key, val in request.GET.items()
    }
    
    get_search = get_search_results
    if request.user.is_authenticated:
        get_search = request.user.get_user_specific_search_results
    
    results = get_search(context)
    
    return custom_render(request, 'search', {
        **context,
        **results,
    })

class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        if request.GET.get('q', '') == '':
            return Response(status = 400)
        
        context = {
            key : val for key, val in request.GET.items()
        }
        
        get_search = get_search_results
        if request.user.is_authenticated:
            get_search = request.user.get_user_specific_search_results
        
        results = get_search(context)
        
        return Response(results)

def search_page(request):
    context = request.data if request.method != 'GET' else request.GET
    link = request.GET.get('link')

    return render(request, 'show_page.html', {
        **context,
        'link'  : link,
    })

@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback') == 'true'
        query = request.POST.get('q')
        print(query, type(query))
        context = {
            'user'  : request.user,
            'query' : request.POST.get('q'),
            'query_keys' : extract_keywords(request.POST.get('q')),
            'interested_keys' : extract_keywords(request.POST.get('snippet')) if feedback else None,
            'not_interested_keys' : extract_keywords(request.POST.get('snippet')) if not feedback else None,
            'site' : request.POST.get('link'),
        }

        request.user.update_search_profile(context)

        return HttpResponse(status=200)