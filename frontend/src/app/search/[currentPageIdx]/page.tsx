import WebpageComponent from "@/components/WebpageComponent";

const Page = (
  { params } : { params: { currentPageIdx: number } }
) => {
  return <WebpageComponent currentPageIdx={params.currentPageIdx} />;
}

export default Page;
