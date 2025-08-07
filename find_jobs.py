from jobspy import scrape_jobs
import pandas as pd

def fix_country_name(name):
    valid_countries = [
        "argentina", "australia", "austria", "bahrain", "bangladesh", "belgium",
        "bulgaria", "brazil", "canada", "chile", "china", "colombia", "costa rica",
        "croatia", "cyprus", "czech republic", "czechia", "denmark", "ecuador", "egypt",
        "estonia", "finland", "france", "germany", "greece", "hong kong", "hungary",
        "india", "indonesia", "ireland", "israel", "italy", "japan", "kuwait", "latvia",
        "lithuania", "luxembourg", "malaysia", "malta", "mexico", "morocco", "netherlands",
        "new zealand", "nigeria", "norway", "oman", "pakistan", "panama", "peru",
        "philippines", "poland", "portugal", "qatar", "romania", "saudi arabia",
        "singapore", "slovakia", "slovenia", "south africa", "south korea", "spain",
        "sweden", "switzerland", "taiwan", "thailand", "türkiye", "turkey", "ukraine",
        "united arab emirates", "uk", "united kingdom", "usa", "us", "united states",
        "uruguay", "venezuela", "vietnam", "usa/ca", "worldwide"
    ]
    name = name.lower().strip()
    if name in valid_countries:
        return name
    else:
        print(f"Warning: '{name}' is not a valid country name for jobspy.")
        print("Please use one of the following:")
        print(", ".join(valid_countries))
        return None

def main():
    print("=== JobSpy Job Search ===")
    job_title = input("Enter the job title or keywords to search for: ").strip()
    location = input("Enter the job location (e.g. Morocco): ").strip()
    try:
        results_wanted = int(input("Enter the number of job results you want: ").strip())
    except ValueError:
        print("Invalid input for number of results, using default 10.")
        results_wanted = 10

    country_name = fix_country_name(location)
    if not country_name:
        print("Exiting program due to invalid country name.")
        return

    print(f"\nSearching for '{job_title}' jobs in '{location}' (up to {results_wanted} results)...\n")

    results = scrape_jobs(
        site_name="indeed",
        search_term=job_title,
        location=location,
        results_wanted=results_wanted,
        country_indeed=country_name
    )

    print("✅ Available columns:")
    print(results.columns)

    print("\n📄 Top Job Results:")
    print(results[["title", "company", "location", "date_posted", "job_url"]])

    # حفظ النتائج في ملف Excel
    filename = f"jobs_{job_title.replace(' ', '_')}_{location.replace(' ', '_')}.xlsx"
    results.to_excel(filename, index=False)
    print(f"\n✅ Results saved to '{filename}'")

if __name__ == "__main__":
    main()
