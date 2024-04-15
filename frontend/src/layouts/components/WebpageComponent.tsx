"use client";

import { searchApi, useUserReviewNotedMutation } from "@/lib/api";
import { getAppStorage, setAppStorage } from "@/lib/cookies";
import { useAppDispatch, useAppSelector } from "@/lib/store";
import { SearchResult } from "@/types";
import { ErrorBoundary } from "next/dist/client/components/error-boundary";
import Link from "next/link";
import { notFound, redirect, useRouter } from "next/navigation";
import { Suspense, useEffect, useRef, useState } from "react";
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import { ThumbDownAlt } from "@mui/icons-material";
import { toast } from "react-toastify";

const WebpageComponent = (
  { currentPageIdx }: Partial<{
    currentPageIdx: number;
  }>,
) => {

  const router = useRouter();
  (currentPageIdx === 0 || currentPageIdx === undefined) && notFound();
  currentPageIdx -= 1;

  // current Page will set to getCookie('search-results')[currentPageIdx]
  let searchResults = getAppStorage('search-results', { encode: false, storageType: 'localStorage' });
  if (!searchResults) {
    notFound();
  }
  searchResults = JSON.parse(searchResults);

  console.log('searchResults: ', searchResults);
  if (searchResults?.length < currentPageIdx) {
    notFound();
  }

  let currentPage: SearchResult = searchResults[currentPageIdx];
  
  if (!currentPage) {
    notFound();
  }

  // Ref for the span element
  const spanRef = useRef<HTMLSpanElement>(null);
  const [isModalOpen, setModalStatus] = useState<boolean>(false);
  const [feedbackStatus, setFeedbackStatus] = useState<boolean | null>(null);
  
  const query = useAppSelector((state) => state.search.query);

  useEffect(() => {
    const options = {
      root: null,
      rootMargin: "0px",
      threshold: 0.5, // Adjust the threshold as per your requirement
    };

    const callback: IntersectionObserverCallback = (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // let userReview = confirm("Is this page helpful ?");
          // setFeedbackStatus(userReview);
          setModalStatus(true);
        }
      });
    };

    const observer = new IntersectionObserver(callback, options);

    if (spanRef.current) {
      observer.observe(spanRef.current);
    }

    return () => {
      if (spanRef.current) {
        observer.unobserve(spanRef.current);
      }
    };
  }, []);

  const [userReviewNoted] = useUserReviewNotedMutation();
  useEffect(() => {
    const tmp = async () => {
      toast('Thanks for the feedback');
      userReviewNoted({
        userReview: feedbackStatus ?? false,
        currentPage,
        query: query ?? '',
      }).finally(() => {
        toast('please retry here');
        setAppStorage(
          'retry-status', 
          JSON.stringify({
            likeStatus: feedbackStatus,
            linkSite: currentPage?.link,
            q: query
          })
        );
        // set document url to /search
        router.push('/search');
      })
    };
    feedbackStatus != null && tmp();
  }, [feedbackStatus]);
  
  return (
    <Suspense fallback={<div>Loading...</div>}>
      
      <div style={{ height: '90vh' }}>
        <ErrorBoundary errorComponent={
          () => (
            <div style={{ height: '100%', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              Unable to load the page. Please try again later.
              <br />
              <button onClick={() => redirect('/search')}>Go back to search</button>
              <br />
              Still want to visit the page at {<Link href={currentPage?.link ?? "/"}>{currentPage?.link}</Link>}
            </div>
          )
        }>
          <iframe
            src={currentPage?.link}
            title={currentPage?.title}
            width="100%"
            height="100%"
            allowFullScreen
            referrerPolicy="origin-when-cross-origin"
            sandbox="allow-scripts allow-popups allow-forms"
          ></iframe>
        </ErrorBoundary>
        <span onScroll={() => console.log('Scrolled to top')}></span>
      </div>
      <style jsx>{`
        iframe {
          border: 0;
        }
      `}</style>
      <style jsx global>{`
        body {
          margin: 0;
        }
      `}</style>
      <span ref={spanRef}></span>



    {/* <button data-modal-target="default-modal" data-modal-toggle="default-modal" className="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">
      Toggle modal
    </button> */}
    <div className="items-center w-full block text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
      If you're unable to load this page, try visiting this link at <span> </span><Link href={currentPage?.link} target="_blank">
        <b>{currentPage?.title}</b>
      </Link>
      <br/>
      
    </div>

    <div id="default-modal" tabIndex={-1} aria-hidden="true" className={`${!isModalOpen && 'hidden'} overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full`}>
        <div className="relative p-4 w-full max-w-2xl max-h-full">
            <div className="relative bg-white rounded-lg shadow dark:bg-gray-700">
                
                <div className="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                        Feedback & Help
                    </h3>
                    <button onClick={() => setModalStatus(false)} type="button" className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="default-modal">
                        <svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                        </svg>
                        <span className="sr-only">Close modal</span>
                    </button>
                </div>
                
                <div className="p-4 md:p-5 space-y-4">
                    <p className="text-center leading-relaxed text-gray-500 dark:text-gray-400">
                    If you're unable to load this page, try visiting this link at <span> </span><Link href={currentPage?.link} target="_blank">
                      <b className=" text-red-400">{currentPage?.title}</b>
                    </Link>
                    </p>
                    <p className="text-center leading-relaxed text-gray-500 dark:text-gray-400">
                      Have you find this content useful
                    </p>
                </div>
                
                <div className="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                    <button onClick={() => setFeedbackStatus(true)} type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                      <ThumbUpAltIcon /> Yes, I do 
                    </button>
                    <button  onClick={() => setFeedbackStatus(false)} type="button" className="py-2.5 px-5 ms-3 text-sm font-medium text-gray-800 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                     <ThumbDownAlt /> No, find another
                    </button>
                </div>
            </div>
        </div>
    </div>

    </Suspense>
  )
}

export default WebpageComponent;
