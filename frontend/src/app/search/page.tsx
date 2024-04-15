import SearchComponent from "@/components/SearchComponent";
import { getListPage } from "@/lib/contentParser";
import SeoMeta from "@/partials/SeoMeta";
import { RegularPage } from "@/types";

export default async function SearchPage() {
    const data: RegularPage = getListPage("search/_index.md");
    const { frontmatter } = data;
    const { title, description, meta_title, image } = frontmatter;
    return (
    <>
      <SeoMeta
        title={title}
        meta_title={meta_title}
        description={description}
        image={image}
      />
      <section className="section-sm">
        <div className="container">
          <div className="row">
            <div className="mx-auto md:col-10 lg:col-8">
              <SearchComponent />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}