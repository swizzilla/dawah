def main():
    print("=" * 60)
    print("GUIDE: How to create cookies.txt for YouTube authentication")
    print("=" * 60)
    
    print("\nTo fix the 'Sign in to confirm you're not a bot' error, you need to:")
    print()
    
    print("METHOD 1: Using browser extension (Recommended)")
    print("1. Install 'Get CookieTxt' extension for Chrome/Firefox")
    print("   - Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid")
    print("   - Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/")
    print("2. Go to https://youtube.com and make sure you're logged in")
    print("3. Click the extension icon and select 'Export'")
    print("4. Save the file as 'cookies.txt' in the project root directory")
    print()
    
    print("METHOD 2: Using yt-dlp directly")
    print("1. Make sure you're logged into YouTube in your browser")
    print("2. Run this command to extract cookies from your browser:")
    print("   yt-dlp --cookies-from-browser chrome https://www.youtube.com/ -o NUL")
    print("   (Replace 'chrome' with your browser: firefox, edge, safari, etc.)")
    print("3. Export the cookies to a file:")
    print("   yt-dlp --cookies-from-browser chrome --dump-single-json https://www.youtube.com/ > /dev/null")
    print()
    
    print("METHOD 3: Manual extraction (Advanced)")
    print("1. Open YouTube in your browser and log in")
    print("2. Press F12 to open developer tools")
    print("3. Go to Application/Storage tab")
    print("4. Expand Cookies and select 'https://www.youtube.com'")
    print("5. Copy all cookies to a text file in Netscape format")
    print()
    
    print("After creating cookies.txt, place it in the project root directory:")
    print("  c:\\Users\\slfrv\\Downloads\\dawah\\dawah\\")
    print()
    
    print("Then restart the application, and it should be able to download YouTube videos.")
    print()
    
    print("More info: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies")
    print("=" * 60)

if __name__ == "__main__":
    main()