from jobspy import scrape_jobs
import pandas as pd
import sys

def fix_country_name(name):
    """Validate and standardize country names with common alternatives"""
    country_mapping = {
        # Common misspellings and alternatives
        "united states": ["usa", "us", "united states of america", "u.s.a.", "u.s."],
        "united kingdom": ["uk", "great britain", "gb", "britain", "england"],
        "czech republic": ["czechia", "czech"],
        "türkiye": ["turkey", "turkie"],
        "uae": ["united arab emirates", "emirates"],
        "hong kong": ["hongkong"],
        "south korea": ["korea", "korea, south"],
        "philippines": ["philipines", "phillipines", "philipines"],
        "worldwide": ["global", "remote worldwide", "world wide", "international"],
        "usa/ca": ["us/ca", "usa or canada", "us or canada"]
    }
    
    # Reverse mapping for easy lookup
    reverse_mapping = {}
    for correct_name, alternatives in country_mapping.items():
        reverse_mapping[correct_name] = correct_name
        for alt in alternatives:
            reverse_mapping[alt] = correct_name
    
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
    
    # Check if input is a known alternative
    if name in reverse_mapping:
        return reverse_mapping[name]
    
    # Check if input is a valid country
    if name in valid_countries:
        return name
    
    # Try to find close matches
    close_matches = [c for c in valid_countries if name in c or c.startswith(name)]
    if len(close_matches) == 1:
        print(f"⚠️  Assuming you meant '{close_matches[0]}' for '{name}'")
        return close_matches[0]
    
    # No match found
    print(f"\n❌ Error: '{name}' is not a valid country name for jobspy.")
    print("Please use one of the following valid countries:")
    print(", ".join(sorted(valid_countries)))
    print("\nCommon alternatives are also accepted (e.g., 'US' for 'United States')")
    return None

def validate_results_wanted(input_str):
    """Validate and parse the number of results wanted"""
    try:
        num = int(input_str)
        if num <= 0:
            print("⚠️  Number must be positive. Using default 10.")
            return 10
        if num > 100:
            print("⚠️  Number is too large (max 100). Using 100.")
            return 100
        return num
    except ValueError:
        print("⚠️  Invalid number. Using default 10.")
        return 10

def display_search_summary(job_title, location, results_wanted):
    """Display the search parameters"""
    print("\n" + "="*50)
    print(f"🔍 Search Parameters:")
    print(f"  Job Title: {job_title}")
    print(f"  Location: {location}")
    print(f"  Results Wanted: {results_wanted}")
    print("="*50 + "\n")

def main():
    print("=== JobSpy Job Search ===")
    print("Enter your job search criteria (press Ctrl+C to quit at any time)\n")
    
    try:
        job_title = input("Enter the job title or keywords to search for: ").strip()
        if not job_title:
            print("❌ Job title cannot be empty. Please try again.")
            return
            
        location = input("Enter the job location (e.g. 'Morocco' or 'Remote'): ").strip()
        if not location:
            print("❌ Location cannot be empty. Please try again.")
            return
            
        results_wanted_input = input("Enter the number of job results you want (default 10, max 100): ").strip()
        results_wanted = validate_results_wanted(results_wanted_input)
        
        country_name = fix_country_name(location)
        if not country_name:
            return
            
        display_search_summary(job_title, location, results_wanted)
        
        print(f"Searching for jobs... This might take a moment...\n")
        
        try:
            results = scrape_jobs(
                site_name="indeed",
                search_term=job_title,
                location=location,
                results_wanted=results_wanted,
                country_indeed=country_name
            )
        except Exception as e:
            print(f"❌ An error occurred during the job search: {str(e)}")
            print("Possible reasons:")
            print("- The location might not be supported by Indeed")
            print("- There might be network issues")
            print("- The jobspy API might have changed")
            return
            
        if results.empty:
            print("❌ No results found. Try different keywords or location.")
            print("Suggestions:")
            print("- Broaden your search terms")
            print("- Try a nearby larger city")
            print("- Check for typos in your location")
        else:
            print("✅ Available columns in results:")
            print(results.columns.tolist())
            
            print("\n📄 Top Job Results:")
            print(results[["title", "company", "location", "date_posted", "job_url"]].head())
            
            # Save results to Excel
            filename = f"jobs_{job_title.replace(' ', '_')}_{location.replace(' ', '_')}.xlsx"
            try:
                results.to_excel(filename, index=False)
                print(f"\n💾 Results saved to '{filename}'")
            except Exception as e:
                print(f"❌ Failed to save results: {str(e)}")
                print("Trying to save as CSV instead...")
                try:
                    csv_filename = filename.replace('.xlsx', '.csv')
                    results.to_csv(csv_filename, index=False)
                    print(f"💾 Results saved to '{csv_filename}'")
                except Exception as e:
                    print(f"❌ Failed to save results in any format: {str(e)}")
                    
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("Please try again later or check your inputs.")

if __name__ == "__main__":
    main()